import re
from typing import Tuple, Optional, List


def validate_required_fields(
    data: dict,
    required_fields: List[str]
) -> Tuple[bool, Optional[str]]:
    """
    Check if all required fields exist and are not empty.
    """
    if not isinstance(data, dict):
        return False, "Invalid request data"

    missing_fields = [
        field
        for field in required_fields
        if field not in data or data.get(field) in ("", None)
    ]

    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"

    return True, None


def validate_positive_int(
    value,
    field_name: str
) -> Tuple[bool, Optional[str]]:
    """
    Validate that value is a positive integer.
    """
    if not isinstance(value, int) or value <= 0:
        return False, f"{field_name} must be a positive integer"

    return True, None


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """
    Validate email format.
    """
    if not isinstance(email, str) or not email.strip():
        return False, "Email is required"

    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return False, "Invalid email address"

    return True, None