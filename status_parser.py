MAX_STATUS_RETRIES = 1  # Single retry allowed for status parse failures


class StatusParseError(Exception):
    """Raised when status parsing fails after all retries exhausted."""
    pass


def parse_status(response: str) -> tuple[str | None, str]:
    """
    Parse status from LLM response.

    Args:
        response: Raw LLM response text

    Returns:
        (status, content) where:
        - status: "INTAKE", "READY", or None if missing/malformed
        - content: response with status line removed (if valid), or original response (if invalid)
    """
    lines = response.split('\n', 1)
    first_line = lines[0]

    # Check for valid format: "STATUS: " followed by INTAKE or READY (case insensitive)
    if first_line.upper().startswith('STATUS: '):
        # Verify exact format (no leading space, exactly one space after colon)
        if not first_line.startswith(first_line.lstrip()):
            return (None, response)

        colon_pos = first_line.find(':')
        if colon_pos == -1 or first_line[colon_pos:colon_pos+2] != ': ':
            return (None, response)

        status_value = first_line[colon_pos+2:].upper()

        # Check for trailing spaces (invalid)
        if status_value != first_line[colon_pos+2:].strip().upper():
            return (None, response)

        if status_value in ('INTAKE', 'READY'):
            content = lines[1] if len(lines) > 1 else ''
            return (status_value, content)

    return (None, response)
