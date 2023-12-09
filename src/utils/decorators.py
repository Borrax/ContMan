from typing import Callable, Any, Union

type ErrorFunc = Callable[[Exception], Union[Any, None]]
type SuccessFunc = Callable[[Any], Union[Any, None]]
type BuilderReturn = Callable[[SuccessFunc], Union[Any, None]]


def tryexceptwrap_builder(
        error_func: ErrorFunc) -> BuilderReturn:
    def wrapper(success_func):
        def caller(*args, **kwargs):
            try:
                return success_func(*args, **kwargs)
            except Exception as e:
                return error_func(e)
        return caller

    return wrapper
