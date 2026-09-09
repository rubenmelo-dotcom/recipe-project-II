def is_positive_number(value):
    try:
        string_to_float = float(value)
    except ValueError:
        return False
    return string_to_float > 0
