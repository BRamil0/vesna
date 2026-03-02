class MetaDefaultObject(type):
    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.default_object = None

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        if cls.default_object is None:
            cls.default_object = instance

        return instance