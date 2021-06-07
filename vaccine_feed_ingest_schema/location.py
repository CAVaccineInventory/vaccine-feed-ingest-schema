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
    r"^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(([0-9]{3})\)|([0-9]{3}))\s*(?:[.-]\s*)?)?([0-9]{3})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:\#|x\.?|ext\.?|extension)\s*(\d+))?$"  # noqa: E501
)

# Lowercase alpha-numeric and underscores
# e.g. google_places
ENUM_VALUE_RE = re.compile(r"^[a-z0-9_]+$")

# Lowercase alpha-numeric and underscores with one colon
# e.g. az_arcgis:hsdg46sj
LOCATION_ID_RE = re.compile(r"^[a-z0-9_]+\:[a-zA-Z0-9_-]+$")

# Source ids can have anything but a space or a colon. Those must be replaced with another character (like a dash).
SOURCE_ID_RE = re.compile(r"^[^\s\:]+$")

# Max length for long text fields storing notes
NOTE_MAX_LENGTH = 2046

# Max length for normal string value fields
VALUE_MAX_LENGTH = 256

# Max length for short enum identifier fields
ENUM_MAX_LENGTH = 64

# Max length for id string fields
ID_MAX_LENGTH = 128


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
    """Brand that administers vaccines.

    The list of participating US pharmacies can be found here:
    https://www.cdc.gov/vaccines/covid-19/retail-pharmacy-program/participating-pharmacies.html

    If multiple brands (eg Big Y Pharmacy, Brookshires) are owned by the same
    parent (eg TOPCO), each brand will get a separate entry in this enum.

    In the future, the parent corporations that own one or more brands
    might also be explicitly represented in the schema.
    """

    ACME = "acme"
    ALBERTSONS = "albertson"
    ALBERTSONS_MARKET = "albertsons_market"
    ALBERTSONS_MARKET_STREET = "albertsons_market_street"
    AMIGOS = "amigos"
    BAKERS = "bakers"
    BIG_Y = "big_y"
    BROOKSHIRE = "brookshire"
    CARRS = "carrs"
    CITY_MARKET = "city_market"
    COSTCO = "costco"
    CUB = "cub_pharmacy"
    CVS = "cvs"
    DILLONS = "dillons"
    DRUGCO = "drugco"
    DUANE_READE = "duane_reade"
    FAMILY_FARE = "family_fare"
    FOOD_CITY = "food_city"
    FOOD_LION = "food_lion"
    FRED_MEYER = "fred_meyer"
    FRESCO_Y_MAS = "fresco_y_mas"
    FRYS = "frys_food_and_drug"
    GENOA = "genoa_healthcare"
    GERBES = "gerbes"
    GIANT = "giant"
    GIANT_EAGLE = "giant_eagle"
    GIANT_FOOD = "giant_food"
    HAGGEN = "haggen"
    HANNAFORD = "hannaford"
    HARMONS = "harmons"
    HARPS = "harps"
    HARRIS_TEETER = "harris_teeter"
    HART = "hart"
    HARTIG = "hartig"
    HARVEYS = "harveys"
    HEALTH_MART = "health_mart"
    HEB = "heb"
    HOMELAND = "homeland"
    HY_VEE = "hyvee"
    INGLES = "ingles"
    JAYC = "jayc"
    JEWEL_OSCO = "jewel_osco"
    KAISER_HEALTH_PLAN = "kaiser_health_plan"
    KAISER_PERMANENTE = "kaiser_permanente"
    KING_SOOPERS = "king_soopers"
    KROGER = "kroger"
    KTA_SUPER_STORES = "kta_super_stores"
    LITTLE_CLINIC = "little_clinic"
    MARIANOS = "marianos"
    MARKET_32 = "market_32"
    MARKET_BISTRO = "market_bistro"
    MARKET_STREET = "market_street"
    MEDICAP = "medicap"
    MEIJER = "meijer"
    METRO_MARKET = "metro_market"
    OSCO = "osco"
    PAK_N_SAVE = "pak_n_save"
    PAVILIONS = "pavilions"
    PAY_LESS = "pay_less"
    PHARMACA = "pharmaca"
    PICK_N_SAVE = "pick_n_save"
    PRICE_CHOPPER = "price_chopper"
    PUBLIX = "publix"
    QFC = "qfc"
    RALEYS = "raleys"
    RALPHS = "ralphs"
    RANDALLS = "randalls"
    RITE_AID = "rite_aid"
    SAFEWAY = "safeway"
    SAMS = "sams"
    SAV_ON = "sav_on"
    SHAWS = "shaws"
    SHOP_RITE = "shop_rite"
    SMITHS = "smiths"
    SOUTH_EASTERN = "south_eastern"
    STAR_MARKET = "star_market"
    STOP_AND_SHOP = "stop_and_shop"
    THRIFTY = "thrifty"
    THRIFTY_WHITE = "thrifty_white"
    TOM_THUMB = "tom_thumb"
    UNITED_SUPERMARKET = "united_supermarket"
    VONS = "vons"
    WALGREENS = "walgreens"
    WALMART = "walmart"
    WEGMANS = "wegmans"
    WEIS = "weis"
    WINN_DIXIE = "winn_dixie"


@enum.unique
class LocationAuthority(str, enum.Enum):
    """Authority that issues identifiers for locations"""

    GOOGLE_PLACES = "google_places"
    VTRCKS = "vtrcks"


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

    street1: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    street2: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
    city: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
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
    other: Optional[str] = Field(max_length=NOTE_MAX_LENGTH)

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
    id: Union[VaccineProvider, str, None] = Field(
        regex=ENUM_VALUE_RE.pattern, max_length=ENUM_MAX_LENGTH
    )
    name: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)


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
        regex=ENUM_VALUE_RE.pattern, max_length=ENUM_MAX_LENGTH
    )
    id: Optional[str] = Field(regex=SOURCE_ID_RE.pattern, max_length=ID_MAX_LENGTH)
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

    source: str = Field(regex=ENUM_VALUE_RE.pattern, max_length=ENUM_MAX_LENGTH)
    id: str = Field(regex=SOURCE_ID_RE.pattern, max_length=ID_MAX_LENGTH)
    fetched_from_uri: Optional[AnyUrl]
    fetched_at: Optional[StringDatetime]
    published_at: Optional[StringDatetime]
    data: dict


class NormalizedLocation(BaseModel):
    id: str = Field(regex=LOCATION_ID_RE.pattern, max_length=ID_MAX_LENGTH)
    name: Optional[str] = Field(max_length=VALUE_MAX_LENGTH)
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
            raise ValueError("Location ID must be prefixed with source name")

        return values
