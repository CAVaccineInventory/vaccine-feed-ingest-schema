"""Common config for all schemas"""

import pydantic


class BaseModel(pydantic.BaseModel):
    """BaseModel for all schema to inherit from."""

    class Config:
        # Strip whitespace from str values by default.
        # This will help have consistant data if parsers forgot to strip.
        anystr_strip_whitespace = True

        # Fail if an attrbute that doesn't exist is added.
        # This will help reduce typos.
        extra = "forbid"

        # Validate when setting attributes.
        # This will help trigger errors right where they occur.
        validate_assignment = True

        # Store enums as string values.
        # This helps so people can use either strings or enums.
        use_enum_values = True
