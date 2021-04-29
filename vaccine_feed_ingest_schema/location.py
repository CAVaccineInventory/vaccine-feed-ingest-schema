"""Normalized Location Schema

Spec defined here:
https://github.com/CAVaccineInventory/vaccine-feed-ingest/wiki/Normalized-Location-Schema
"""

import datetime
import enum
import re
from typing import List, Optional, Union

from pydantic import (
    AnyUrl,
    EmailStr,
    Field,
    HttpUrl,
    datetime_parse,
    root_validator,
)

from .common import BaseModel

# Validate zipcode is in 5 digit or 5 digit + 4 digit format
# e.g. 94612, 94612-1234
ZIPCODE_RE = re.compile(r"^[0-9]{5}(?:-[0-9]{4})?$")

# Validate that phone number is a valid US phone number.
# Less strict than spec so normalizers don't need to encode phone numbers exactly
# e.g. (444) 444-4444, +1 (444) 444-4444
US_PHONE_RE = re.compile(
    r"^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:\#|x\.?|ext\.?|extension)\s*(\d+))?$"  # noqa: E501
)

# Lowercase alpha-numeric and underscores
# e.g. google_places
ENUM_VALUE_RE = re.compile(r"^[a-z0-9_]+$")

# Lowercase alpha-numeric and underscores with one colon
# e.g. az_arcgis:hsdg46sj
LOCATION_ID_RE = re.compile(r"^[a-z0-9_]+\:[a-z0-9_]+$")

# Source ids can have anything but a space or a colon. Those must be replaced with another character (like a dash).
SOURCE_ID_RE = re.compile(r"^[^\s\:]+$")


class StringDatetime(datetime.datetime):
    @classmethod
    def __get_validators__(cls):
        yield datetime_parse.parse_datetime
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime.datetime) -> str:
        return v.isoformat()


class StringDate(datetime.date):
    @classmethod
    def __get_validators__(cls):
        yield datetime_parse.parse_date
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime.date) -> str:
        return v.isoformat()


class StringTime(datetime.date):
    @classmethod
    def __get_validators__(cls):
        yield datetime_parse.parse_time
        yield cls.validate

    @classmethod
    def validate(cls, v: datetime.time) -> str:
        return v.isoformat("minutes")


@enum.unique
class State(str, enum.Enum):
    ALABAMA = "AL"
    ALASKA = "AK"
    AMERICAN_SAMOA = "AS"
    ARIZONA = "AZ"
    ARKANSAS = "AR"
    CALIFORNIA = "CA"
    COLORADO = "CO"
    CONNECTICUT = "CT"
    DELAWARE = "DE"
    DISTRICT_OF_COLUMBIA = "DC"
    FLORIDA = "FL"
    GEORGIA = "GA"
    GUAM = "GU"
    HAWAII = "HI"
    IDAHO = "ID"
    ILLINOIS = "IL"
    INDIANA = "IN"
    IOWA = "IA"
    KANSAS = "KS"
    KENTUCKY = "KY"
    LOUISIANA = "LA"
    MAINE = "ME"
    MARYLAND = "MD"
    MASSACHUSETTS = "MA"
    MICHIGAN = "MI"
    MINNESOTA = "MN"
    MISSISSIPPI = "MS"
    MISSOURI = "MO"
    MONTANA = "MT"
    NEBRASKA = "NE"
    NEVADA = "NV"
    NEW_HAMPSHIRE = "NH"
    NEW_JERSEY = "NJ"
    NEW_MEXICO = "NM"
    NEW_YORK = "NY"
    NORTH_CAROLINA = "NC"
    NORTH_DAKOTA = "ND"
    NORTHERN_MARIANA_IS = "MP"
    OHIO = "OH"
    OKLAHOMA = "OK"
    OREGON = "OR"
    PENNSYLVANIA = "PA"
    PUERTO_RICO = "PR"
    RHODE_ISLAND = "RI"
    SOUTH_CAROLINA = "SC"
    SOUTH_DAKOTA = "SD"
    TENNESSEE = "TN"
    TEXAS = "TX"
    UTAH = "UT"
    VERMONT = "VT"
    VIRGINIA = "VA"
    VIRGIN_ISLANDS = "VI"
    WASHINGTON = "WA"
    WEST_VIRGINIA = "WV"
    WISCONSIN = "WI"
    WYOMING = "WY"


@enum.unique
class ContactType(str, enum.Enum):
    GENERAL = "general"
    BOOKING = "booking"


@enum.unique
class DayOfWeek(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    PUBLIC_HOLIDAYS = "public_holidays"


@enum.unique
class VaccineType(str, enum.Enum):
    PFIZER_BIONTECH = "pfizer_biontech"
    MODERNA = "moderna"
    JOHNSON_JOHNSON_JANSSEN = "johnson_johnson_janssen"
    OXFORD_ASTRAZENECA = "oxford_astrazeneca"


@enum.unique
class VaccineSupply(str, enum.Enum):
    """Supply level of vaccine"""

    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"


@enum.unique
class WheelchairAccessLevel(str, enum.Enum):
    YES = "yes"  # there is wheelchair access not sure about level of service
    FULL = "full"  # here is full wheelchair access
    PARTIAL = "partial"  # there is partial wheelchair access
    NO = "no"  # there is no wheelchair access


@enum.unique
class VaccineProvider(str, enum.Enum):
    """Parent organization that provides vaccines"""

    RITE_AID = "rite_aid"
    WALGREENS = "walgreens"
    SAFEWAY = "safeway"
    VONS = "vons"
    SAMS = "sams"
    ALBERTSONS = "albertson"
    PAVILIONS = "pavilions"
    WALMART = "walmart"
    CVS = "cvs"


@enum.unique
class LocationAuthority(str, enum.Enum):
    """Authority that issues identifiers for locations"""

    GOOGLE_PLACES = "google_places"


class Address(BaseModel):
    """
    {
        "street1": str,
        "street2": str,
        "city": str,
        "state": str as state initial e.g. CA,
        "zip": str,
    },
    """

    street1: Optional[str]
    street2: Optional[str]
    city: Optional[str]
    state: Optional[State]
    zip: Optional[str] = Field(regex=ZIPCODE_RE.pattern)


class LatLng(BaseModel):
    """
    {
        "latitude": float,
        "longitude": float,
    },
    """

    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)


class Contact(BaseModel):
    """
    {
        "contact_type": str as contact type enum e.g. booking,
        "phone": str as (###) ###-###,
        "website": str,
        "email": str,
        "other": str,
    }
    """

    contact_type: Optional[ContactType]
    phone: Optional[str] = Field(regex=US_PHONE_RE.pattern)
    website: Optional[HttpUrl]
    email: Optional[EmailStr]
    other: Optional[str]

    @root_validator
    @classmethod
    def validate_has_one_value(cls, values: dict) -> dict:
        oneof_fields = ["phone", "website", "email", "other"]
        has_values = [key for key in oneof_fields if values.get(key)]

        if len(has_values) > 1:
            raise ValueError(
                f"Multiple values specified in {', '.join(has_values)}. "
                "Only one value should be specified per Contact entry."
            )

        if not has_values:
            raise ValueError("No values specified for Contact.")

        return values


class OpenDate(BaseModel):
    """
    {
        "opens": str as iso8601 date,
        "closes": str as iso8601 date,
    }
    """

    opens: Optional[StringDate]
    closes: Optional[StringDate]

    @root_validator
    @classmethod
    def validate_closes_after_opens(cls, values: dict) -> dict:
        opens = values.get("opens")
        closes = values.get("closes")

        if opens and closes:
            if closes < opens:
                raise ValueError("Closes date must be after opens date")

        return values


class OpenHour(BaseModel):
    """
    {
        "day": str as day of week enum e.g. monday,
        "opens": str as 24h local time formatted as hh:mm,
        "closes": str as 24h local time formatted as hh:mm,
    }
    """

    day: DayOfWeek
    opens: StringTime
    closes: StringTime

    @root_validator
    @classmethod
    def validate_closes_after_opens(cls, values: dict) -> dict:
        opens = values.get("opens")
        closes = values.get("closes")

        if opens and closes:
            if closes < opens:
                raise ValueError("Closes time must be after opens time")

        return values


class Availability(BaseModel):
    """
    {
        "drop_in": bool,
        "appointments": bool,
    },
    """

    drop_in: Optional[bool]
    appointments: Optional[bool]


class Vaccine(BaseModel):
    """
    {
        "vaccine": str as vaccine type enum,
        "supply_level": str as supply level enum e.g. more_than_48hrs
    }
    """

    vaccine: VaccineType
    supply_level: Optional[VaccineSupply]


class Access(BaseModel):
    """
    {
        "walk": bool,
        "drive": bool,
        "wheelchair": str,
    }
    """

    walk: Optional[bool]
    drive: Optional[bool]
    wheelchair: Optional[WheelchairAccessLevel]


class Organization(BaseModel):
    """
    {
        "id": str as parent organization enum e.g. rite_aid,
        "name": str,
    }
    """

    # Use VaccineProvider enum value if available overwise make your own.
    id: Union[VaccineProvider, str, None] = Field(regex=ENUM_VALUE_RE.pattern)
    name: Optional[str]


class Link(BaseModel):
    """
    {
        "authority": str as authority enum e.g. rite_aid or google_places,
        "id": str as id used by authority to reference this location e.g. 4096,
        "uri": str as uri used by authority to reference this location,
    }
    """

    # Use LocationAuthority enum value if available, overwise make your own.
    authority: Union[LocationAuthority, VaccineProvider, str, None] = Field(
        regex=ENUM_VALUE_RE.pattern
    )
    id: Optional[str]
    uri: Optional[AnyUrl]


class Source(BaseModel):
    """
    {
        "source": str as source type enum e.g. vaccinespotter,
        "id": str as source defined id e.g. 7382088,
        "fetched_from_uri": str as uri where data was fetched from,
        "fetched_at": str as iso8601 utc datetime (when scraper ran),
        "published_at": str as iso8601 utc datetime (when source claims it updated),
        "data": {...parsed source data in source schema...},
    }
    """

    source: str = Field(regex=ENUM_VALUE_RE.pattern)
    id: str = Field(regex=SOURCE_ID_RE.pattern)
    fetched_from_uri: Optional[AnyUrl]
    fetched_at: Optional[StringDatetime]
    published_at: Optional[StringDatetime]
    data: dict


class NormalizedLocation(BaseModel):
    id: str = Field(regex=LOCATION_ID_RE.pattern)
    name: Optional[str]
    address: Optional[Address]
    location: Optional[LatLng]
    contact: Optional[List[Contact]]
    languages: Optional[List[str]]  # [str as ISO 639-1 code]
    opening_dates: Optional[List[OpenDate]]
    opening_hours: Optional[List[OpenHour]]
    availability: Optional[Availability]
    inventory: Optional[List[Vaccine]]
    access: Optional[Access]
    parent_organization: Optional[Organization]
    links: Optional[List[Link]]
    notes: Optional[List[str]]
    active: Optional[bool]
    source: Source

    @root_validator
    @classmethod
    def validate_id_source(cls, values: dict) -> dict:
        loc_id = values.get("id")
        if not loc_id:
            return values

        source = values.get("source")
        if not source:
            return values

        source_name = source.source
        if not source_name:
            return values

        if not loc_id.startswith(f"{source_name}:"):
            raise ValueError("Location ID must be prefixed with with source name")

        return values
