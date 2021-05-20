from typing import Optional

from .common import BaseModel
from .location import NormalizedLocation


class ImportMatchAction(BaseModel):
    """Match action to take when importing a source location"""

    id: Optional[str]
    action: str


class ImportSourceLocation(BaseModel):
    """Import source location record"""

    source_uid: str
    source_name: str
    name: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    import_json: NormalizedLocation
    content_hash: Optional[str]
    match: Optional[ImportMatchAction]
