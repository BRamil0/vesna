import inspect
import typing
import weakref
from functools import wraps


class MetaDefaultObject(type):
    """
    A metaclass that provides basic DI tools can simulate global objects.
    """

    _meta_objects: dict[type, object] = weakref.WeakValueDictionary()

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        cls.default_object = None

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        if cls.default_object is None:
            cls.default_object = instance
            MetaDefaultObject._meta_objects[cls] = instance

        return instance

    def __setattr__(cls, name, value):
        super().__setattr__(name, value)

        if name == "default_object":
            if value is not None:
                MetaDefaultObject._meta_objects[cls] = value
            else:
                MetaDefaultObject._meta_objects.pop(cls, None)

    @classmethod
    def meta_get_instance(mcs, cls_type):
        return mcs._meta_objects.get(cls_type)

    @staticmethod
    def meta_inject(auto_creation: bool = False):
        def decorator(func: typing.Callable) -> typing.Any:
            sig = inspect.signature(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound_args = sig.bind_partial(*args, **kwargs)

                for name, param in sig.parameters.items():
                    if name not in bound_args.arguments:
                        instance = MetaDefaultObject.meta_get_instance(param.annotation)

                        if instance:
                            bound_args.arguments[name] = instance
                        elif param.default is inspect.Parameter.empty:
                            if auto_creation and inspect.isclass(param.annotation):
                                instance = param.annotation()
                                bound_args.arguments[name] = instance
                            else:
                                raise TypeError(
                                    f"Missing required argument: '{name}' ({param.annotation}). \
                                No instance found in registry."
                                )

                bound_args.apply_defaults()
                return func(*bound_args.args, **bound_args.kwargs)

            return wrapper

        return decorator
