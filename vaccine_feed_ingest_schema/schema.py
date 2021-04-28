"""Deprecated import location for schema"""

import warnings

from .load import ImportMatchAction, ImportSourceLocation  # noqa: F401
from .location import (  # noqa: F401
    Access,
    Address,
    Availability,
    Contact,
    LatLng,
    Link,
    NormalizedLocation,
    OpenDate,
    OpenHour,
    Organization,
    Source,
    Vaccine,
)

"""
DEPRECATION NOTICE
vaccine_feed_ingest_schema/schema.py is DEPRECATED. Instead of using this file,
import the file that you care about:

from vaccine_feed_ingest_schema import location
~or~
from vaccine_feed_ingest_schema import load

This may be removed in a future major version bump.
"""
warnings.warn(
    "vaccine_feed_ingest_schema.schema is deprecated. "
    + "Use vaccine_feed_ingest_schema.location or vaccine_feed_ingest_schema.load instead",
    DeprecationWarning,
    stacklevel=2,
)
