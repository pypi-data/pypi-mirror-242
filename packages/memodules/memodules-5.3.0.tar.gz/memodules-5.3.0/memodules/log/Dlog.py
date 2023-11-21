from ..e_typing import (
    ColorStdOut,
    StdOut,
)
from functools import wraps
from typing import (
    ParamSpec,
    Callable,
    TypeVar,
    Any,
)
from .cprint import (
    Color,
)
__all__ = [
    'DebugPrint',
    'log',
]
_Args = ParamSpec('_Args')
_Returns = TypeVar('_Returns')


def log(cfunc: Callable[_Args, _Returns] = None, /,
        *, color: Color = Color.blue,
        show_call: bool = True,
        show_args: bool = True,
        show_returns: bool = True) -> Callable[_Args, _Returns]:
    @wraps(cfunc)
    def decorator(func: Callable[_Args, _Returns]) -> Callable[_Args, _Returns]:
        @wraps(func)
        def wrapper(*args: _Args.args, **kwargs: _Args.kwargs) -> _Returns:
            show = ''
            if show_call:
                show += f'call: {func.__name__}'
            if show_args:
                if show_call:
                    show += '\n'
                show += f'args: {args}, {kwargs}'
            if show_call or show_args:
                color(show)
            show = ''
            result = func(*args, **kwargs)
            if show_returns:
                show += f'returns: {result}'
                color(show)
            return result
        return wrapper

    if cfunc is not None:
        return decorator(cfunc)

    return decorator


class DebugPrint:
    def __init__(self, debug_flg: bool, newline_number: int = 3):
        """デバッグ用ログをデバッグフラグがTrueならcall構文で指定した引数の内容を色違いでコンソール出力してくれるクラス\n
        出力する項目をnewline_number個ごとに改行して出力を見やすくする"""
        self.debug = debug_flg
        self.nl_num = newline_number

    def __call__(self, *args):
        """examples:
            >>> debug = DebugPrint(True)
            >>> debug('debug', 'to', 'example')
            (light green)debug: debug, to, example
            >>> debug = DebugPrint(True, newline_number = 2)
            >>> debug('debug', 'to', 'example')
            debug: debug, to,
            \texample"""
        nt = '\n\t'
        spc = ' '
        if self.debug:
            for i in range(len(args)):
                if i == 0:
                    content = args[i]
                else:
                    mid_entry = nt if i % self.nl_num == 0 else spc
                    content = f'{content},{mid_entry}{args[i]}'

            print(f'\033[92mdebug: {content}\033[0m')
