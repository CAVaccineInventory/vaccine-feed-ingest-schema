import os

from setuptools import setup

VERSION = "1.2.5"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="vaccine-feed-ingest-schema",
    description="Normalized data schema for the output of the vaccine-feed-ingest pipeline.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Vaccinate The States",
    url="https://github.com/CAVaccineInventory/vaccine-feed-ingest-schema",
    project_urls={
        "Issues": "https://github.com/CAVaccineInventory/vaccine-feed-ingest-schema/issues",
        "CI": "https://github.com/CAVaccineInventory/vaccine-feed-ingest-schema/actions",
        "Changelog": "https://github.com/CAVaccineInventory/vaccine-feed-ingest-schema/releases",
    },
    license="MIT",
    version=VERSION,
    packages=["vaccine_feed_ingest_schema"],
    install_requires=["pydantic[email]"],
    extras_require={"test": ["pytest"], "lint": ["flake8", "black", "mypy", "isort"]},
    tests_require=["vaccine-feed-ingest-schema[test]"],
    python_requires=">=3.8",
)
