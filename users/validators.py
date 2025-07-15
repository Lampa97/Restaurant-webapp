import re

from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Validates a phone number to ensure it matches the required format.

    Args:
        value (str): The phone number to validate.

    Raises:
        ValidationError: If the phone number does not match the required format.
    """
    # Regular expression for validating phone numbers
    if not re.match(r"^\+?1?\d{9,15}$", value):
        raise ValidationError("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
