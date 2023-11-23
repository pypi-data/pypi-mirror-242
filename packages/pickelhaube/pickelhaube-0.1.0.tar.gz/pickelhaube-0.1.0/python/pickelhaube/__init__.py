#!/usr/bin/env python3
import logging
from dataclasses import dataclass
import typing

import hashlib
import pickle
import hmac
import lzma


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Digest:
    name: str
    fn: typing.Callable[[], typing.Any]
    size: int


@dataclass(frozen=True)
class CoDec:
    name: str
    compress: typing.Callable
    decompress: typing.Callable


DEFAULT_DIGEST = Digest(
    'BLAKE2b, with 64 bytes',
    lambda: hashlib.blake2b(digest_size=64),
    size=64,
)
# TODO: Abandon LZMA, use Zstandard (pyzstd)
CODEC_LZMA = CoDec(
    'LZMA in XZ, with SHA256 checksums',
    compress=lambda fobj: lzma.open(fobj, 'wb', format=lzma.FORMAT_XZ, check=lzma.CHECK_SHA256),
    decompress=lambda fobj: lzma.open(fobj, 'rb', format=lzma.FORMAT_XZ),
)


def dump(obj, file, *, hmac_key: bytes,
         pickle_protocol: int = pickle.HIGHEST_PROTOCOL,
         digest: Digest = DEFAULT_DIGEST,
         codec: CoDec = CODEC_LZMA) -> None:
    logger.debug('# Saving Object')
    logger.debug('- HMAC Digest: %s', digest.name)
    logger.debug('-       CoDec: %s', codec.name)
    # # Pickle
    obj_pickled = pickle.dumps(obj, protocol=pickle_protocol)
    logger.debug('Pickle: %d bytes', len(obj_pickled))
    # # HMAC
    hmac_obj = hmac.new(hmac_key, digestmod=digest.fn)
    hmac_obj.update(obj_pickled)
    obj_hmac = hmac_obj.digest()
    logger.debug('HMAC [%s]: "0x%s"', hmac_obj.name, hmac_obj.hexdigest())
    # # Compress
    size_uncompressed = 0
    if file.seekable():
        tell_before = file.tell()
    else:
        tell_before = None
    # Write HMAC (uncompressed)
    size_uncompressed += file.write(obj_hmac)
    with codec.compress(file) as compress_obj:
        # Write Pickled Object (compressed)
        size_uncompressed += compress_obj.write(obj_pickled)
    # TODO: Use Zstandard
    # | See https://github.com/facebook/zstd/blob/release/doc/zstd_compression_format.md#skippable-frames
    # |     to include the HMAC as a skippable frame (not as uncompressed data)
    logger.debug('| Size HMAC: %d bytes', digest.size)
    logger.debug('| Size Uncompressed: %d bytes', size_uncompressed)
    if tell_before is not None:
        size_compressed = file.tell() - tell_before
        logger.debug('| Size Compressed: %d bytes', size_compressed)
        compress_ratio = size_compressed / size_uncompressed
        logger.debug('| Compression Ratio: %.2f%%', compress_ratio * 100)


def dumps(obj, *, hmac_key: bytes,
          pickle_protocol: int = pickle.HIGHEST_PROTOCOL,
          digest: Digest = DEFAULT_DIGEST,
          codec: CoDec = CODEC_LZMA) -> None:
    # TODO: Move `dump` in here, switch the implementation around
    raise NotImplementedError


def load(file, *, hmac_key: bytes,
         digest: Digest = DEFAULT_DIGEST,
         codec: CoDec = CODEC_LZMA) -> typing.Any:
    logger.debug('# Loading Object')
    logger.debug('- HMAC Digest: %s', digest.name)
    logger.debug('-       CoDec: %s', codec.name)
    if file.seekable():
        tell_before = file.tell()
    else:
        tell_before = None
    # Read HMAC
    logger.debug('| Size HMAC: %d bytes', digest.size)
    hmac_at_header = file.read(digest.size)
    assert len(hmac_at_header) == digest.size
    # Read Compressed Pickle
    pickle_bytes = None
    with codec.decompress(file) as uncompress_obj:
        pickle_bytes = uncompress_obj.read()
    assert pickle_bytes is not None
    size_uncompressed = len(pickle_bytes) + digest.size
    logger.debug('| Size Uncompressed: %d bytes', size_uncompressed)
    if tell_before is not None:
        size_compressed = file.tell() - tell_before
        logger.debug('| Size Compressed: %d bytes', size_compressed)
        compress_ratio = size_compressed / size_uncompressed
        logger.debug('| Compression Ratio: %.2f%%', compress_ratio * 100)

    # # HMAC
    hmac_obj = hmac.new(hmac_key, digestmod=digest.fn)
    hmac_obj.update(pickle_bytes)
    hmac_at_pickle = hmac_obj.digest()
    if not hmac.compare_digest(hmac_at_pickle, hmac_at_header):
        raise ValueError('Invalid HMAC')  # TODO: raise a custom exception
    logger.debug('HMAC [%s]: "0x%s"', hmac_obj.name, hmac_obj.hexdigest())
    logger.debug('Pickle: %d bytes', len(pickle_bytes))
    # Valid, read the pickle
    return pickle.loads(pickle_bytes)


def loads(data, *, hmac_key: bytes,
          digest: Digest = DEFAULT_DIGEST,
          codec: CoDec = CODEC_LZMA) -> typing.Any:
    # TODO: Move `load` in here, switch the implementation around
    raise NotImplementedError


__all__ = [
    # Classes
    'Digest', 'CoDec',
    # Default Values
    'DEFAULT_DIGEST', 'CODEC_LZMA',
    # Functions
    'dump', 'dumps',
    'load', 'loads',
]
