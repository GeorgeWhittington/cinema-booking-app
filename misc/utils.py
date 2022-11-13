def get_hours_minutes(total_seconds):
    """Gets the hours and minutes from a duration in seconds."""
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)
    return int(h), int(m)