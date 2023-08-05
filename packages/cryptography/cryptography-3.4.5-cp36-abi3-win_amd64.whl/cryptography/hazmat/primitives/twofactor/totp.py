# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.

import typing

from cryptography.exceptions import UnsupportedAlgorithm, _Reasons
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.backends.interfaces import HMACBackend
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import (
    HOTP,
    _ALLOWED_HASH_TYPES,
)
from cryptography.hazmat.primitives.twofactor.utils import _generate_uri


class TOTP(object):
    def __init__(
        self,
        key: bytes,
        length: int,
        algorithm: _ALLOWED_HASH_TYPES,
        time_step: int,
        backend=None,
        enforce_key_length: bool = True,
    ):
        backend = _get_backend(backend)
        if not isinstance(backend, HMACBackend):
            raise UnsupportedAlgorithm(
                "Backend object does not implement HMACBackend.",
                _Reasons.BACKEND_MISSING_INTERFACE,
            )

        self._time_step = time_step
        self._hotp = HOTP(key, length, algorithm, backend, enforce_key_length)

    def generate(self, time: typing.Union[int, float]) -> bytes:
        counter = int(time / self._time_step)
        return self._hotp.generate(counter)

    def verify(self, totp: bytes, time: int) -> None:
        if not constant_time.bytes_eq(self.generate(time), totp):
            raise InvalidToken("Supplied TOTP value does not match.")

    def get_provisioning_uri(
        self, account_name: str, issuer: typing.Optional[str]
    ) -> str:
        return _generate_uri(
            self._hotp,
            "totp",
            account_name,
            issuer,
            [("period", int(self._time_step))],
        )
