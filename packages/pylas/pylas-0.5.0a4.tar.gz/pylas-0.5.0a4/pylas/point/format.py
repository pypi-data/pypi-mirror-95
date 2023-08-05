from itertools import zip_longest
from typing import Optional, Iterable

import numpy as np

from . import dims
from ..errors import PylasError


class ExtraBytesParams:
    """All parameters needed to create extra bytes"""

    def __init__(
        self,
        name: str,
        type: str,
        description: str = "",
        offsets: Optional[np.ndarray] = None,
        scales: Optional[np.ndarray] = None,
    ) -> None:
        self.name = name
        """ The name of the extra dimension """
        self.type = type
        """ The type of the extra dimension """
        self.description = description
        """ A description of the extra dimension """
        self.offsets = offsets
        """ The offsets to use if its a 'scaled dimension', can be none """
        self.scales = scales
        """ The scales to use if its a 'scaled dimension', can be none """


class PointFormat:
    """Class that contains the informations about the dimensions that forms a PointFormat.

    A PointFormat has 'standard' dimensions (dimensions defined in the LAS standard, each
    point format has its set of dimensions), but it can also have extra (non-standard) dimensions
    defined by the user)

    >>> fmt = PointFormat(3)
    >>> all(dim.is_standard for dim in fmt.dimensions)
    True
    >>> dim = fmt.dimension_by_name("classification") # or fmt["classification"]
    >>> dim.max
    31
    >>> dim.min
    0
    >>> dim.num_bits
    5

    """

    def __init__(
        self,
        point_format_id: int,
    ):
        """
        Parameters
        ----------
        point_format_id: int
            point format id
        """
        self.id = point_format_id
        self.dimensions = []
        composed_dims = dims.COMPOSED_FIELDS[self.id]
        for dim_name in dims.ALL_POINT_FORMATS_DIMENSIONS[self.id]:
            try:
                sub_fields = composed_dims[dim_name]
            except KeyError:
                dimension = dims.DimensionInfo.from_type_str(
                    dim_name, dims.DIMENSIONS_TO_TYPE[dim_name], is_standard=True
                )
                self.dimensions.append(dimension)
            else:
                for sub_field in sub_fields:
                    dimension = dims.DimensionInfo.from_bitmask(
                        sub_field.name, sub_field.mask, is_standard=True
                    )
                    self.dimensions.append(dimension)

    @property
    def standard_dimensions(self) -> Iterable[dims.DimensionInfo]:
        """Returns an iterable of the standard dimensions

        >>> fmt = PointFormat(0)
        >>> standard_dims = list(fmt.standard_dimensions)
        >>> len(standard_dims)
        15
        >>> standard_dims[4].name
        'return_number'


        """
        return (dim for dim in self.dimensions if dim.is_standard)

    @property
    def extra_dimensions(self) -> Iterable[dims.DimensionInfo]:
        return (dim for dim in self.dimensions if dim.is_standard is False)

    @property
    def dimension_names(self) -> Iterable[str]:
        """Returns the names of the dimensions contained in the point format"""
        return (dim.name for dim in self.dimensions)

    @property
    def standard_dimension_names(self) -> Iterable[str]:
        """Returns the names of the extra dimensions in this point format"""
        return (dim.name for dim in self.standard_dimensions)

    @property
    def extra_dimension_names(self) -> Iterable[str]:
        """Returns the names of the extra dimensions in this point format"""
        return (dim.name for dim in self.extra_dimensions)

    @property
    def size(self) -> int:
        """Returns the number of bytes (standard + extra) a point takes

        >>> PointFormat(3).size
        34

        >>> fmt = PointFormat(3)
        >>> fmt.add_extra_dimension(ExtraBytesParams("codification", "uint64"))
        >>> fmt.size
        42
        """
        return int(sum(dim.num_bits for dim in self.dimensions) // 8)

    @property
    def num_standard_bytes(self) -> int:
        """Returns the number of bytes used by standard dims

        >>> fmt = PointFormat(3)
        >>> fmt.add_extra_dimension(ExtraBytesParams("codification", "uint64"))
        >>> fmt.num_standard_bytes
        34
        """
        return int(sum(dim.num_bits for dim in self.standard_dimensions) // 8)

    @property
    def num_extra_bytes(self) -> int:
        """Returns the number of extra bytes

        >>> fmt = PointFormat(3)
        >>> fmt.add_extra_dimension(ExtraBytesParams("codification", "uint64"))
        >>> fmt.num_extra_bytes
        8
        """
        return int(sum(dim.num_bits for dim in self.extra_dimensions) // 8)

    @property
    def has_waveform_packet(self):
        """Returns True if the point format has waveform packet dimensions"""
        dimensions = set(self.dimension_names)
        return all(name in dimensions for name in dims.WAVEFORM_FIELDS_NAMES)

    def dimension_by_name(self, name: str) -> dims.DimensionInfo:
        """Returns the dimension info for the dimension by name

        ValueError is raised if the dimension does not exist un the point format

        >>> info = PointFormat(2).dimension_by_name('number_of_returns')
        >>> info.name == 'number_of_returns'
        True
        >>> info.num_bits == 3
        True


        >>> info = PointFormat(2).dimension_by_name('gps_time')
        Traceback (most recent call last):
        ...
        ValueError: Dimension 'gps_time' does not exist
        """
        for dim in self.dimensions:
            if dim.name == name:
                return dim
        raise ValueError(f"Dimension '{name}' does not exist")

    def add_extra_dimension(self, param: ExtraBytesParams) -> None:
        """Add an extra, user-defined dimension"""
        dim_info = dims.DimensionInfo.from_type_str(
            param.name,
            param.type,
            is_standard=False,
            description=param.description,
            offsets=param.offsets,
            scales=param.scales,
        )
        if (
            dim_info.num_elements > 3
            and dim_info.kind != dims.DimensionKind.UnsignedInteger
        ):
            raise PylasError("Extra Dimensions do not support more than 3 elements")
        self.dimensions.append(dim_info)

    def dtype(self):
        """Returns the numpy.dtype used to store the point records in a numpy array

        .. note::

            The dtype corresponds to the dtype with sub_fields *packed* into their
            composed fields

        """
        dtype = dims.ALL_POINT_FORMATS_DTYPE[self.id]
        descr = dtype.descr
        for extra_dim in self.extra_dimensions:
            descr.append((extra_dim.name, extra_dim.type_str()))
        return np.dtype(descr)

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.dimension_by_name(item)
        return self.dimensions[item]

    def __eq__(self, other):
        if self.id != other.id:
            return False

        for my_eb, ot_eb in zip_longest(self.extra_dimensions, other.extra_dimensions):
            if my_eb != ot_eb:
                return False

        return True

    def __repr__(self):
        return "<PointFormat({}, {} bytes of extra dims)>".format(
            self.id, self.num_extra_bytes
        )


def lost_dimensions(point_fmt_in, point_fmt_out):
    """Returns a list of the names of the dimensions that will be lost
    when converting from point_fmt_in to point_fmt_out
    """

    dimensions_in = set(PointFormat(point_fmt_in).dimension_names)
    dimensions_out = set(PointFormat(point_fmt_out).dimension_names)

    completely_lost = []
    for dim_name in dimensions_in:
        if dim_name not in dimensions_out:
            completely_lost.append(dim_name)
    return completely_lost
