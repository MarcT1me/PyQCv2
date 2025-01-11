def increment(initial_value=0):
    value = initial_value

    def inc(v=None):
        nonlocal value
        if v is not None:
            value = v
        result = value
        value += 1
        return result

    return inc
