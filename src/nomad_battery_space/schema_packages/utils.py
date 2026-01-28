def validate_required(value, *, name: str) -> None:
    """Validate that a required field has a non-empty value.

    Raises a ``ValueError`` when ``value`` is ``None`` or an empty or
    whitespace-only string. Intended for use by schema package normalizers
    (e.g., in `battery_sample_package.py`).

    Args:
        value: The value to validate.
        name: The human-readable name of the field used in the exception
            message.

    Raises:
        ValueError: If ``value`` is ``None`` or an empty/whitespace-only
            string.
    """
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValueError(f"'{name}' is mandatory and must not be empty.")
