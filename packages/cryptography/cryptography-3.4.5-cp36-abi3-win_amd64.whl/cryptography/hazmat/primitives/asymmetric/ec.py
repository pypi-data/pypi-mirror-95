# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.


import abc
import typing
import warnings

from cryptography import utils
from cryptography.hazmat._oid import ObjectIdentifier
from cryptography.hazmat.backends import _get_backend
from cryptography.hazmat.primitives import _serialization, hashes
from cryptography.hazmat.primitives.asymmetric import (
    AsymmetricSignatureContext,
    AsymmetricVerificationContext,
    utils as asym_utils,
)


class EllipticCurveOID(object):
    SECP192R1 = ObjectIdentifier("1.2.840.10045.3.1.1")
    SECP224R1 = ObjectIdentifier("1.3.132.0.33")
    SECP256K1 = ObjectIdentifier("1.3.132.0.10")
    SECP256R1 = ObjectIdentifier("1.2.840.10045.3.1.7")
    SECP384R1 = ObjectIdentifier("1.3.132.0.34")
    SECP521R1 = ObjectIdentifier("1.3.132.0.35")
    BRAINPOOLP256R1 = ObjectIdentifier("1.3.36.3.3.2.8.1.1.7")
    BRAINPOOLP384R1 = ObjectIdentifier("1.3.36.3.3.2.8.1.1.11")
    BRAINPOOLP512R1 = ObjectIdentifier("1.3.36.3.3.2.8.1.1.13")
    SECT163K1 = ObjectIdentifier("1.3.132.0.1")
    SECT163R2 = ObjectIdentifier("1.3.132.0.15")
    SECT233K1 = ObjectIdentifier("1.3.132.0.26")
    SECT233R1 = ObjectIdentifier("1.3.132.0.27")
    SECT283K1 = ObjectIdentifier("1.3.132.0.16")
    SECT283R1 = ObjectIdentifier("1.3.132.0.17")
    SECT409K1 = ObjectIdentifier("1.3.132.0.36")
    SECT409R1 = ObjectIdentifier("1.3.132.0.37")
    SECT571K1 = ObjectIdentifier("1.3.132.0.38")
    SECT571R1 = ObjectIdentifier("1.3.132.0.39")


class EllipticCurve(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def name(self) -> str:
        """
        The name of the curve. e.g. secp256r1.
        """

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        Bit size of a secret scalar for the curve.
        """


class EllipticCurveSignatureAlgorithm(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def algorithm(
        self,
    ) -> typing.Union[asym_utils.Prehashed, hashes.HashAlgorithm]:
        """
        The digest algorithm used with this signature.
        """


class EllipticCurvePrivateKey(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def signer(
        self,
        signature_algorithm: EllipticCurveSignatureAlgorithm,
    ) -> AsymmetricSignatureContext:
        """
        Returns an AsymmetricSignatureContext used for signing data.
        """

    @abc.abstractmethod
    def exchange(
        self, algorithm: "ECDH", peer_public_key: "EllipticCurvePublicKey"
    ) -> bytes:
        """
        Performs a key exchange operation using the provided algorithm with the
        provided peer's public key.
        """

    @abc.abstractmethod
    def public_key(self) -> "EllipticCurvePublicKey":
        """
        The EllipticCurvePublicKey for this private key.
        """

    @abc.abstractproperty
    def curve(self) -> EllipticCurve:
        """
        The EllipticCurve that this key is on.
        """

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        Bit size of a secret scalar for the curve.
        """

    @abc.abstractmethod
    def sign(
        self,
        data,
        signature_algorithm: EllipticCurveSignatureAlgorithm,
    ) -> bytes:
        """
        Signs the data
        """

    @abc.abstractmethod
    def private_numbers(self) -> "EllipticCurvePrivateNumbers":
        """
        Returns an EllipticCurvePrivateNumbers.
        """

    @abc.abstractmethod
    def private_bytes(
        self,
        encoding: _serialization.Encoding,
        format: _serialization.PrivateFormat,
        encryption_algorithm: _serialization.KeySerializationEncryption,
    ) -> bytes:
        """
        Returns the key serialized as bytes.
        """


EllipticCurvePrivateKeyWithSerialization = EllipticCurvePrivateKey


class EllipticCurvePublicKey(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def verifier(
        self,
        signature: bytes,
        signature_algorithm: EllipticCurveSignatureAlgorithm,
    ) -> AsymmetricVerificationContext:
        """
        Returns an AsymmetricVerificationContext used for signing data.
        """

    @abc.abstractproperty
    def curve(self) -> EllipticCurve:
        """
        The EllipticCurve that this key is on.
        """

    @abc.abstractproperty
    def key_size(self) -> int:
        """
        Bit size of a secret scalar for the curve.
        """

    @abc.abstractmethod
    def public_numbers(self) -> "EllipticCurvePublicNumbers":
        """
        Returns an EllipticCurvePublicNumbers.
        """

    @abc.abstractmethod
    def public_bytes(
        self,
        encoding: _serialization.Encoding,
        format: _serialization.PublicFormat,
    ) -> bytes:
        """
        Returns the key serialized as bytes.
        """

    @abc.abstractmethod
    def verify(
        self,
        signature: bytes,
        data: bytes,
        signature_algorithm: EllipticCurveSignatureAlgorithm,
    ) -> None:
        """
        Verifies the signature of the data.
        """

    @classmethod
    def from_encoded_point(
        cls, curve: EllipticCurve, data: bytes
    ) -> "EllipticCurvePublicKey":
        utils._check_bytes("data", data)

        if not isinstance(curve, EllipticCurve):
            raise TypeError("curve must be an EllipticCurve instance")

        if len(data) == 0:
            raise ValueError("data must not be an empty byte string")

        if data[0] not in [0x02, 0x03, 0x04]:
            raise ValueError("Unsupported elliptic curve point type")

        from cryptography.hazmat.backends.openssl.backend import backend

        return backend.load_elliptic_curve_public_bytes(curve, data)


EllipticCurvePublicKeyWithSerialization = EllipticCurvePublicKey


class SECT571R1(EllipticCurve):
    name = "sect571r1"
    key_size = 570


class SECT409R1(EllipticCurve):
    name = "sect409r1"
    key_size = 409


class SECT283R1(EllipticCurve):
    name = "sect283r1"
    key_size = 283


class SECT233R1(EllipticCurve):
    name = "sect233r1"
    key_size = 233


class SECT163R2(EllipticCurve):
    name = "sect163r2"
    key_size = 163


class SECT571K1(EllipticCurve):
    name = "sect571k1"
    key_size = 571


class SECT409K1(EllipticCurve):
    name = "sect409k1"
    key_size = 409


class SECT283K1(EllipticCurve):
    name = "sect283k1"
    key_size = 283


class SECT233K1(EllipticCurve):
    name = "sect233k1"
    key_size = 233


class SECT163K1(EllipticCurve):
    name = "sect163k1"
    key_size = 163


class SECP521R1(EllipticCurve):
    name = "secp521r1"
    key_size = 521


class SECP384R1(EllipticCurve):
    name = "secp384r1"
    key_size = 384


class SECP256R1(EllipticCurve):
    name = "secp256r1"
    key_size = 256


class SECP256K1(EllipticCurve):
    name = "secp256k1"
    key_size = 256


class SECP224R1(EllipticCurve):
    name = "secp224r1"
    key_size = 224


class SECP192R1(EllipticCurve):
    name = "secp192r1"
    key_size = 192


class BrainpoolP256R1(EllipticCurve):
    name = "brainpoolP256r1"
    key_size = 256


class BrainpoolP384R1(EllipticCurve):
    name = "brainpoolP384r1"
    key_size = 384


class BrainpoolP512R1(EllipticCurve):
    name = "brainpoolP512r1"
    key_size = 512


_CURVE_TYPES: typing.Dict[str, typing.Type[EllipticCurve]] = {
    "prime192v1": SECP192R1,
    "prime256v1": SECP256R1,
    "secp192r1": SECP192R1,
    "secp224r1": SECP224R1,
    "secp256r1": SECP256R1,
    "secp384r1": SECP384R1,
    "secp521r1": SECP521R1,
    "secp256k1": SECP256K1,
    "sect163k1": SECT163K1,
    "sect233k1": SECT233K1,
    "sect283k1": SECT283K1,
    "sect409k1": SECT409K1,
    "sect571k1": SECT571K1,
    "sect163r2": SECT163R2,
    "sect233r1": SECT233R1,
    "sect283r1": SECT283R1,
    "sect409r1": SECT409R1,
    "sect571r1": SECT571R1,
    "brainpoolP256r1": BrainpoolP256R1,
    "brainpoolP384r1": BrainpoolP384R1,
    "brainpoolP512r1": BrainpoolP512R1,
}


class ECDSA(EllipticCurveSignatureAlgorithm):
    def __init__(self, algorithm):
        self._algorithm = algorithm

    algorithm = utils.read_only_property("_algorithm")


def generate_private_key(
    curve: EllipticCurve, backend=None
) -> EllipticCurvePrivateKey:
    backend = _get_backend(backend)
    return backend.generate_elliptic_curve_private_key(curve)


def derive_private_key(
    private_value: int, curve: EllipticCurve, backend=None
) -> EllipticCurvePrivateKey:
    backend = _get_backend(backend)
    if not isinstance(private_value, int):
        raise TypeError("private_value must be an integer type.")

    if private_value <= 0:
        raise ValueError("private_value must be a positive integer.")

    if not isinstance(curve, EllipticCurve):
        raise TypeError("curve must provide the EllipticCurve interface.")

    return backend.derive_elliptic_curve_private_key(private_value, curve)


class EllipticCurvePublicNumbers(object):
    def __init__(self, x: int, y: int, curve: EllipticCurve):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x and y must be integers.")

        if not isinstance(curve, EllipticCurve):
            raise TypeError("curve must provide the EllipticCurve interface.")

        self._y = y
        self._x = x
        self._curve = curve

    def public_key(self, backend=None) -> EllipticCurvePublicKey:
        backend = _get_backend(backend)
        return backend.load_elliptic_curve_public_numbers(self)

    def encode_point(self) -> bytes:
        warnings.warn(
            "encode_point has been deprecated on EllipticCurvePublicNumbers"
            " and will be removed in a future version. Please use "
            "EllipticCurvePublicKey.public_bytes to obtain both "
            "compressed and uncompressed point encoding.",
            utils.PersistentlyDeprecated2019,
            stacklevel=2,
        )
        # key_size is in bits. Convert to bytes and round up
        byte_length = (self.curve.key_size + 7) // 8
        return (
            b"\x04"
            + utils.int_to_bytes(self.x, byte_length)
            + utils.int_to_bytes(self.y, byte_length)
        )

    @classmethod
    def from_encoded_point(
        cls, curve: EllipticCurve, data: bytes
    ) -> "EllipticCurvePublicNumbers":
        if not isinstance(curve, EllipticCurve):
            raise TypeError("curve must be an EllipticCurve instance")

        warnings.warn(
            "Support for unsafe construction of public numbers from "
            "encoded data will be removed in a future version. "
            "Please use EllipticCurvePublicKey.from_encoded_point",
            utils.PersistentlyDeprecated2019,
            stacklevel=2,
        )

        if data.startswith(b"\x04"):
            # key_size is in bits. Convert to bytes and round up
            byte_length = (curve.key_size + 7) // 8
            if len(data) == 2 * byte_length + 1:
                x = int.from_bytes(data[1 : byte_length + 1], "big")
                y = int.from_bytes(data[byte_length + 1 :], "big")
                return cls(x, y, curve)
            else:
                raise ValueError("Invalid elliptic curve point data length")
        else:
            raise ValueError("Unsupported elliptic curve point type")

    curve = utils.read_only_property("_curve")
    x = utils.read_only_property("_x")
    y = utils.read_only_property("_y")

    def __eq__(self, other):
        if not isinstance(other, EllipticCurvePublicNumbers):
            return NotImplemented

        return (
            self.x == other.x
            and self.y == other.y
            and self.curve.name == other.curve.name
            and self.curve.key_size == other.curve.key_size
        )

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.x, self.y, self.curve.name, self.curve.key_size))

    def __repr__(self):
        return (
            "<EllipticCurvePublicNumbers(curve={0.curve.name}, x={0.x}, "
            "y={0.y}>".format(self)
        )


class EllipticCurvePrivateNumbers(object):
    def __init__(
        self, private_value: int, public_numbers: EllipticCurvePublicNumbers
    ):
        if not isinstance(private_value, int):
            raise TypeError("private_value must be an integer.")

        if not isinstance(public_numbers, EllipticCurvePublicNumbers):
            raise TypeError(
                "public_numbers must be an EllipticCurvePublicNumbers "
                "instance."
            )

        self._private_value = private_value
        self._public_numbers = public_numbers

    def private_key(self, backend=None) -> EllipticCurvePrivateKey:
        backend = _get_backend(backend)
        return backend.load_elliptic_curve_private_numbers(self)

    private_value = utils.read_only_property("_private_value")
    public_numbers = utils.read_only_property("_public_numbers")

    def __eq__(self, other):
        if not isinstance(other, EllipticCurvePrivateNumbers):
            return NotImplemented

        return (
            self.private_value == other.private_value
            and self.public_numbers == other.public_numbers
        )

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.private_value, self.public_numbers))


class ECDH(object):
    pass


_OID_TO_CURVE = {
    EllipticCurveOID.SECP192R1: SECP192R1,
    EllipticCurveOID.SECP224R1: SECP224R1,
    EllipticCurveOID.SECP256K1: SECP256K1,
    EllipticCurveOID.SECP256R1: SECP256R1,
    EllipticCurveOID.SECP384R1: SECP384R1,
    EllipticCurveOID.SECP521R1: SECP521R1,
    EllipticCurveOID.BRAINPOOLP256R1: BrainpoolP256R1,
    EllipticCurveOID.BRAINPOOLP384R1: BrainpoolP384R1,
    EllipticCurveOID.BRAINPOOLP512R1: BrainpoolP512R1,
    EllipticCurveOID.SECT163K1: SECT163K1,
    EllipticCurveOID.SECT163R2: SECT163R2,
    EllipticCurveOID.SECT233K1: SECT233K1,
    EllipticCurveOID.SECT233R1: SECT233R1,
    EllipticCurveOID.SECT283K1: SECT283K1,
    EllipticCurveOID.SECT283R1: SECT283R1,
    EllipticCurveOID.SECT409K1: SECT409K1,
    EllipticCurveOID.SECT409R1: SECT409R1,
    EllipticCurveOID.SECT571K1: SECT571K1,
    EllipticCurveOID.SECT571R1: SECT571R1,
}


def get_curve_for_oid(oid: ObjectIdentifier) -> typing.Type[EllipticCurve]:
    try:
        return _OID_TO_CURVE[oid]
    except KeyError:
        raise LookupError(
            "The provided object identifier has no matching elliptic "
            "curve class"
        )
