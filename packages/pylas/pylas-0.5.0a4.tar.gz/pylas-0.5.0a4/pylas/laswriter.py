import abc
import io
import logging
from copy import copy
from typing import BinaryIO, Optional, Union, Iterable

import numpy as np

from .compression import LazBackend
from .errors import PylasError
from .header import LasHeader
from .point import dims
from .point.format import PointFormat
from .point.record import PackedPointRecord
from .vlrs.known import LasZipVlr
from .vlrs.vlrlist import VLRList

logger = logging.getLogger(__name__)

try:
    import lazrs
except ModuleNotFoundError:
    pass

try:
    import laszip
except ModuleNotFoundError:
    pass


class LasWriter:
    """
    Allows to write a complete LAS/LAZ file to the destination.
    """

    def __init__(
        self,
        dest: BinaryIO,
        header: LasHeader,
        do_compress: Optional[bool] = None,
        laz_backend: Optional[Union[LazBackend, Iterable[LazBackend]]] = None,
        closefd: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        dest:
            file object where the LAS/LAZ will be written

        header:
            The header of the file to be written

        do_compress: optional bool
            whether the file data should be written as LAS (uncompressed)
            or LAZ (compressed).
            If None, the file won't be compressed, unless a laz_backend is provided

        laz_backend: optional LazBackend or sequence of LazBackend
            The LazBackend to use (or if it is a sequence the LazBackend to try)
            for the compression

        closefd: default True
            should the `dest` be closed when the writer is closed
        """
        self.closefd = closefd
        self.header = copy(header)
        self.header.partial_reset()
        self.header.maxs = [np.finfo("f8").min] * 3
        self.header.mins = [np.finfo("f8").max] * 3

        self.dest = dest
        self.done = False

        dims.raise_if_version_not_compatible_with_fmt(
            header.point_format.id, str(self.header.version)
        )

        if laz_backend is not None:
            if do_compress is None:
                do_compress = True
            self.laz_backend = laz_backend
        else:
            if do_compress is None:
                do_compress = False
            self.laz_backend = LazBackend.detect_available()
        self.header.are_points_compressed = do_compress

        if do_compress:
            self.point_writer: IPointWriter = self._create_laz_backend(self.laz_backend)
        else:
            self.point_writer: IPointWriter = UncompressedPointWriter(self.dest)

        self.point_writer.write_initial_header_and_vlrs(self.header)

    def write_points(self, points: PackedPointRecord) -> None:
        if not points:
            return

        if self.done:
            raise PylasError("Cannot write points anymore")

        if points.point_format != self.header.point_format:
            raise PylasError("Incompatible point formats")

        self.header.update(points)
        self.point_writer.write_points(points)

    def write_evlrs(self, evlrs: VLRList) -> None:
        if self.header.version.minor < 4:
            raise PylasError(
                "EVLRs are not supported on files with version less than 1.4"
            )

        if len(evlrs) > 0:
            self.point_writer.done()
            self.done = True
            self.header.number_of_evlrs = len(evlrs)
            self.header.start_of_first_evlr = self.dest.tell()
            evlrs.write_to(self.dest, as_extended=True)

    def close(self) -> None:
        if self.point_writer is not None:
            if not self.done:
                self.point_writer.done()
            self.point_writer.write_updated_header(self.header)
        if self.closefd:
            self.dest.close()

    def _create_laz_backend(
        self, laz_backends: Union[LazBackend, Iterable[LazBackend]]
    ) -> "IPointWriter":
        try:
            laz_backends = iter(laz_backends)
        except TypeError:
            laz_backends = (laz_backends,)

        last_error: Optional[Exception] = None
        for backend in laz_backends:
            try:
                if not backend.is_available():
                    raise PylasError(f"The '{backend}' is not available")

                if backend == LazBackend.Laszip:
                    return LaszipPointWriter(self.dest, self.header)
                elif backend == LazBackend.LazrsParallel:
                    return LazrsPointWriter(
                        self.dest, self.header.point_format, parallel=True
                    )
                elif backend == LazBackend.Lazrs:
                    return LazrsPointWriter(
                        self.dest, self.header.point_format, parallel=False
                    )
                else:
                    raise PylasError("Unknown LazBacked: {}".format(backend))
            except Exception as e:
                logger.error(e)
                last_error = e

        if last_error is not None:
            raise PylasError("No LazBackend selected, cannot compress")
        else:
            raise PylasError(f"No LazBackend could be initialized: {last_error}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class IPointWriter(abc.ABC):
    """Interface to be implemented by the actual
    PointWriter backend

    """

    @property
    @abc.abstractmethod
    def destination(self) -> BinaryIO:
        ...

    def write_initial_header_and_vlrs(self, header: LasHeader) -> None:
        header.write_to(self.destination)

    @abc.abstractmethod
    def write_points(self, points: PackedPointRecord) -> None:
        ...

    @abc.abstractmethod
    def done(self) -> None:
        ...

    def write_updated_header(self, header):
        self.destination.seek(0, io.SEEK_SET)
        header.write_to(self.destination)


class UncompressedPointWriter(IPointWriter):
    """
    Writing points in the simple uncompressed case.
    """

    def __init__(self, dest: BinaryIO) -> None:
        self.dest = dest

    @property
    def destination(self) -> BinaryIO:
        return self.dest

    def write_points(self, points: PackedPointRecord) -> None:
        self.dest.write(points.memoryview())

    def done(self) -> None:
        pass


class LaszipPointWriter(IPointWriter):
    """
    Compressed point writer using laszip backend
    """

    def __init__(self, dest: BinaryIO, header: LasHeader) -> None:
        self.dest = dest
        header.set_compressed(False)
        with io.BytesIO() as tmp:
            header.write_to(tmp)
            header_bytes = tmp.getvalue()

        self.zipper = laszip.LasZipper(self.dest, header_bytes)
        zipper_header = self.zipper.header
        assert zipper_header.point_data_format == header.point_format.id
        assert zipper_header.point_data_record_length == header.point_format.size

        header.set_compressed(True)

    @property
    def destination(self) -> BinaryIO:
        return self.dest

    def write_points(self, points: PackedPointRecord) -> None:
        points_bytes = np.frombuffer(points.array, np.uint8)
        self.zipper.compress(points_bytes)

    def done(self) -> None:
        self.zipper.done()

    def write_initial_header_and_vlrs(self, header: LasHeader) -> None:
        # Do nothing as creating the laszip zipper writes the header and vlrs
        pass

    def write_updated_header(self, header: LasHeader) -> None:
        if header.number_of_evlrs != 0:
            # We wrote some evlrs, we have to update the header
            self.dest.seek(0, io.SEEK_SET)
            file_header = LasHeader.read_from(self.dest)
            end_of_header_pos = self.dest.tell()
            file_header.number_of_evlrs = header.number_of_evlrs
            file_header.start_of_first_evlr = header.start_of_first_evlr
            self.dest.seek(0, io.SEEK_SET)
            file_header.write_to(self.dest)
            assert self.dest.tell() == end_of_header_pos


class LazrsPointWriter(IPointWriter):
    """
    Compressed point writer using lazrs backend
    """

    def __init__(
        self, dest: BinaryIO, point_format: PointFormat, parallel: bool
    ) -> None:
        self.dest = dest
        self.vlr = lazrs.LazVlr.new_for_compression(
            point_format.id, point_format.num_extra_bytes
        )
        self.parallel = parallel
        self.compressor: Optional[
            Union[lazrs.ParLasZipCompressor, lazrs.LasZipCompressor]
        ] = None

    def write_initial_header_and_vlrs(self, header: LasHeader) -> None:
        laszip_vlr = LasZipVlr(self.vlr.record_data())
        header.vlrs.append(laszip_vlr)
        super().write_initial_header_and_vlrs(header)
        # We have to initialize our compressor here
        # because on init, it writes the offset to chunk table
        # so the header and vlrs have to be written
        if self.parallel:
            self.compressor = lazrs.ParLasZipCompressor(self.dest, self.vlr)
        else:
            self.compressor = lazrs.LasZipCompressor(self.dest, self.vlr)

    @property
    def destination(self) -> BinaryIO:
        return self.dest

    def write_points(self, points: PackedPointRecord) -> None:
        assert (
            self.compressor is not None
        ), "Trying to write points without having written header"
        points_bytes = np.frombuffer(points.array, np.uint8)
        self.compressor.compress_many(points_bytes)

    def done(self) -> None:
        if self.compressor is not None:
            self.compressor.done()
