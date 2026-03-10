import typing
import weakref


class MetaCache(type):
    """
    A metaclass that provides object caching
    if identical arguments are passed when creating an object.
    """

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._meta_cache: dict[typing.Any, typing.Any] = weakref.WeakValueDictionary()

    def __call__(cls, *args, **kwargs):
        cache_key = (args, tuple(sorted(kwargs.items())))
        instance = cls._meta_cache.get(cache_key)
        if instance is None:
            instance = super().__call__(*args, **kwargs)
            cls._meta_cache[cache_key] = instance

        return instance
