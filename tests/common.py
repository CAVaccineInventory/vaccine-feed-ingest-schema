"""Common test utils"""
import inspect


def collect_existing_subclasses(module, base_class):
    """Collect a set of class names in module that are subclasses of base_class"""
    class_tuples = inspect.getmembers(module, inspect.isclass)
    return set(
        [
            class_tuple[0]
            for class_tuple in class_tuples
            if issubclass(class_tuple[1], base_class)
        ]
    )
