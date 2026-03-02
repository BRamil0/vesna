import typing

class MetaCache(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls._meta_cache: typing.Dict[typing.Any, typing.Any] = dict()

    def __call__(cls, *args, **kwargs):
        cache_key = (args, tuple(sorted(kwargs.items())))
        if cache_key not in cls._meta_cache:
            instance = super().__call__(*args, **kwargs)
            cls._meta_cache[cache_key] = instance

        return cls._meta_cache[cache_key]