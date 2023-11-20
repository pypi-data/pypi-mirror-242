from functools import wraps
import inspect
from typing import Any, Callable, Dict, Generic, Optional, TypeVar, cast

from typing_extensions import ParamSpec, Protocol


ReplaceFuncType = TypeVar('ReplaceFuncType', bound=Callable[..., Any])

P = ParamSpec('P')
T = TypeVar('T')


class ReplacedFuncType(Protocol, Generic[P, T]):
    originalFunc: Callable[P, T]
    def __call__(self, *args: Any, **kwds: Any) -> T:
        ...


def replaceFunc(replaceFunc: ReplaceFuncType, *, isEnabled=True,
                filter_: Optional[Callable[[Dict[str, Any]], bool]] = None):
    '''
    replace wrapped function by replaceFunc
    @param isEnable:
        is replace functionality is enabled
    @param filter_:
        function that determines if original or replace function should be called\n
        if returns True then the replacement one is called
    >>> def devFunc():
    >>>     ...
    >>> @replaceFunc(devFunc, isEnabled=os.getenv("IS_DEV", "")=="true")
    >>> def prodFunc():
    >>>     ...
    call the original finction
    originalResult = prodFunc.originalFunc()
    '''
    def decorator(func: Callable[P, T]) -> ReplacedFuncType[P, T]:
        if not isEnabled:
            return func  # type: ignore
        signature = inspect.signature(func)

        @wraps(func)
        def decorated(*args, **kwargs):
            if not filter_:
                return replaceFunc(*args, **kwargs)
            if filter_:
                kw = signature.bind(*args, **kwargs)
                if filter_(kw.arguments):
                    return replaceFunc(*args, **kwargs)
            return func(*args, **kwargs)  # type: ignore
        decorated.originalFunc = func  # type: ignore
        return cast(ReplacedFuncType[P, T], decorated)
    return decorator
