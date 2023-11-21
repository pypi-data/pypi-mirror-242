import argparse
import functools
import inspect
import re


class Aga(object):
    def __init__(self):
        super().__init__()
        self._parser = argparse.ArgumentParser()
        self._args = None

    @property
    def args(self):
        return self._args

    def bake(self):
        self._args = self._parser.parse_args()

    @staticmethod
    def get_arg_docstrings(docstring: str, args: list) -> dict:
        args = [arg + ":" for arg in args]
        args.append('Returns:')

        ds_only_args = docstring.split("Args:")[1]

        args_dict = dict()

        for idx, arg in enumerate(args[:-1]):
            val = ds_only_args.split(arg)[1].split(args[idx+1])[0]
            val = val.replace('\n', ' ').replace('\t', ' ').strip()
            args_dict[arg.replace(":", "")] = val

        return args_dict

    def add_arg(self, func) -> callable:
        f_inf = inspect.getfullargspec(func)

        defaults = None
        if f_inf.defaults is not None:
            defaults = [d for d in reversed(f_inf.defaults)]

        arg_docstrings = None
        if func.__doc__ is not None:
            arg_docstrings = self.get_arg_docstrings(func.__doc__, f_inf.args)

        for arg in reversed(f_inf.args):
            default = None

            if defaults:
                default = defaults[0]
                del defaults[0]

            self._parser.add_argument(
                f'-{arg[0]}',
                f'--{arg}',
                metavar='',
                type=f_inf.annotations[arg] if arg in f_inf.annotations.keys() else None,
                default=default,
                help=arg_docstrings[arg] if arg_docstrings is not None else None,
                action=argparse.BooleanOptionalAction if f_inf.annotations[arg] == bool else None
            )

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper
