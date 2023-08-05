# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.


import abc
import inspect
import sys
import typing
import warnings


# We use a UserWarning subclass, instead of DeprecationWarning, because CPython
# decided deprecation warnings should be invisble by default.
class CryptographyDeprecationWarning(UserWarning):
    pass


# Several APIs were deprecated with no specific end-of-life date because of the
# ubiquity of their use. They should not be removed until we agree on when that
# cycle ends.
PersistentlyDeprecated2017 = CryptographyDeprecationWarning
PersistentlyDeprecated2019 = CryptographyDeprecationWarning
DeprecatedIn34 = CryptographyDeprecationWarning


def _check_bytes(name: str, value: bytes):
    if not isinstance(value, bytes):
        raise TypeError("{} must be bytes".format(name))


def _check_byteslike(name: str, value: bytes):
    try:
        memoryview(value)
    except TypeError:
        raise TypeError("{} must be bytes-like".format(name))


def read_only_property(name: str):
    return property(lambda self: getattr(self, name))


def register_interface(iface):
    def register_decorator(klass, *, check_annotations=False):
        verify_interface(iface, klass, check_annotations=check_annotations)
        iface.register(klass)
        return klass

    return register_decorator


def register_interface_if(predicate, iface):
    def register_decorator(klass, *, check_annotations=False):
        if predicate:
            verify_interface(iface, klass, check_annotations=check_annotations)
            iface.register(klass)
        return klass

    return register_decorator


def int_to_bytes(integer: int, length: typing.Optional[int] = None) -> bytes:
    return integer.to_bytes(
        length or (integer.bit_length() + 7) // 8 or 1, "big"
    )


class InterfaceNotImplemented(Exception):
    pass


def strip_annotation(signature):
    return inspect.Signature(
        [
            param.replace(annotation=inspect.Parameter.empty)
            for param in signature.parameters.values()
        ]
    )


def verify_interface(iface, klass, *, check_annotations=False):
    for method in iface.__abstractmethods__:
        if not hasattr(klass, method):
            raise InterfaceNotImplemented(
                "{} is missing a {!r} method".format(klass, method)
            )
        if isinstance(getattr(iface, method), abc.abstractproperty):
            # Can't properly verify these yet.
            continue
        sig = inspect.signature(getattr(iface, method))
        actual = inspect.signature(getattr(klass, method))
        if check_annotations:
            ok = sig == actual
        else:
            ok = strip_annotation(sig) == strip_annotation(actual)
        if not ok:
            raise InterfaceNotImplemented(
                "{}.{}'s signature differs from the expected. Expected: "
                "{!r}. Received: {!r}".format(klass, method, sig, actual)
            )


class _DeprecatedValue(object):
    def __init__(self, value, message, warning_class):
        self.value = value
        self.message = message
        self.warning_class = warning_class


class _ModuleWithDeprecations(object):
    def __init__(self, module):
        self.__dict__["_module"] = module

    def __getattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn(obj.message, obj.warning_class, stacklevel=2)
            obj = obj.value
        return obj

    def __setattr__(self, attr, value):
        setattr(self._module, attr, value)

    def __delattr__(self, attr):
        obj = getattr(self._module, attr)
        if isinstance(obj, _DeprecatedValue):
            warnings.warn(obj.message, obj.warning_class, stacklevel=2)

        delattr(self._module, attr)

    def __dir__(self):
        return ["_module"] + dir(self._module)


def deprecated(value, module_name, message, warning_class):
    module = sys.modules[module_name]
    if not isinstance(module, _ModuleWithDeprecations):
        sys.modules[module_name] = _ModuleWithDeprecations(
            module
        )  # type: ignore[assignment]
    return _DeprecatedValue(value, message, warning_class)


def cached_property(func):
    cached_name = "_cached_{}".format(func)
    sentinel = object()

    def inner(instance):
        cache = getattr(instance, cached_name, sentinel)
        if cache is not sentinel:
            return cache
        result = func(instance)
        setattr(instance, cached_name, result)
        return result

    return property(inner)


int_from_bytes = deprecated(
    int.from_bytes,
    __name__,
    "int_from_bytes is deprecated, use int.from_bytes instead",
    DeprecatedIn34,
)
