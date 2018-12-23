def validate_percent_value(value: int, accuracy: int = 0) -> bool:
    _is_percent_value = is_percent_value(value=value, accuracy=accuracy)
    if not _is_percent_value:
        raise ValueError('Not a valid percent value: {0} (Accuracy: {1})'.format(value, accuracy))


def is_percent_value(value: int, accuracy: int = 0) -> bool:
    if accuracy < 0:
        raise ValueError('Accuracy has to be greater or equal to zero.')
    
    if value < 0:
        raise ValueError('Percent value has to be greater or equal to zero.')
    
    divisor = 100 * (10 ** accuracy)
    value = int(value / divisor)
    in_range = value in range(0, 101)
    
    return in_range

