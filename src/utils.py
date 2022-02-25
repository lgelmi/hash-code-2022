from functools import reduce


def compose(*functions) -> callable:

    return reduce(compose_2, functions)


def compose_2(inner: callable, outer: callable) -> callable:
    def composed(*args, **kwargs):
        return outer(inner(*args, **kwargs))

    return composed
