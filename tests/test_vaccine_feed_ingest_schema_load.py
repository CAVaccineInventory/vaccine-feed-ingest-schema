import inspect

from vaccine_feed_ingest_schema import load


def test_has_expected_classes():
    class_tuples = inspect.getmembers(load, inspect.isclass)
    classes = list(map(lambda class_tuple: class_tuple[0], class_tuples))

    expected_classes = [
        "BaseModel",
        "NormalizedLocation",
        "ImportMatchAction",
        "ImportSourceLocation",
    ]

    for expected_class in expected_classes:
        if expected_class not in classes:
            raise KeyError(f"Expected class {expected_class} is not defined.")

    for klass in classes:
        if klass not in expected_classes:
            raise KeyError(f"Extra class {klass} defined. Did you update your tests?")
