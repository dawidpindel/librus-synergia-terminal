from dataclasses import dataclass, field
from . import exceptions
import typing


def _load_args_from_function(func: typing.Callable) -> list[list[str, type]]:
    variable_names = list(func.__code__.co_varnames[:func.__code__.co_argcount])

    variable_types = func.__annotations__

    variables = [[name, variable_types[name]] for name in variable_names]

    return variables


def _load_kwargs_from_function(func: typing.Callable) -> typing.Dict[str, type]:
    keywords = func.__kwdefaults__.copy() if func.__kwdefaults__ is not None else {}

    variable_types = func.__annotations__.copy()

    for argument_name in keywords:
        keywords[argument_name] = variable_types[argument_name]

    return keywords


@dataclass()
class Command:
    function: typing.Callable

    arguments: list[list[str, type]] = field(repr=False, init=False)
    keyword_arguments: typing.Dict[str, type] = field(repr=False, init=False)
    argument_names: list[str] = field(repr=False, init=False)
    expected_argument_types: list[type] = field(repr=False, init=False)

    def __post_init__(self) -> None:
        self.keyword_arguments = _load_kwargs_from_function(self.function)
        self.arguments = _load_args_from_function(self.function)

        self.argument_names = [entry[0] for entry in self.arguments]
        self.expected_argument_types = [entry[1] for entry in self.arguments]

    def validate_args(self, arguments: list[typing.Any]) -> None:
        """
        This function will validate given list of arguments (it will check count and type)

        Raises:
            NotEnoughArgumentsException: when given list contains less arguments than
                expected (less than specified when creating given instance)
            TooManyArguments: when given list contains more arguments than
                expected (more than specified when creating given instance)
            InvalidArgumentType: when some argument in given list is of different type than expected
                (different type than specified when creating given instance)
        """
        if len(arguments) < len(self.argument_names):
            raise exceptions.NotEnoughArgumentsException(
                "not enough arguments", self.argument_names[len(arguments):]
            )

        elif len(arguments) > len(self.argument_names):
            raise exceptions.TooManyArguments(
                "you passed too many arguments", arguments[len(self.arguments):]
            )

        for index, arg in enumerate(arguments):
            expected_arg_type = self.expected_argument_types[index]

            if isinstance(arg, expected_arg_type):
                continue

            raise exceptions.InvalidArgumentType(
                "you passed an argument of invalid type",
                type(arg),
                expected_arg_type,
                self.argument_names[index],
                index
            )

    def validate_kwargs(self, keyword_arguments: typing.Dict[str, type]) -> None:
        """
        This function will validate given keyword arguments (it will check name and type)

        Raises:
            UnknownKeywordArgumenException: when there is an unexpected keyword argument in given dictionary
            InvalidKeywordArgumentType: when any of the keywords has a value of invalid type assigned to it
        """
        for argument_name in keyword_arguments:
            if argument_name not in self.keyword_arguments:
                raise exceptions.UnknownKeywordArgumenException("unknown keyword argument", argument_name)

            if not isinstance(keyword_arguments[argument_name], self.keyword_arguments[argument_name]):
                raise exceptions.InvalidKeywordArgumentType(
                    "invalid keyword argument type",
                    type(keyword_arguments[argument_name]),
                    self.keyword_arguments[argument_name],
                    argument_name
                )

    def run_command(self, arguments: list, keyword_arguments: dict) -> None:
        """
        Runs this command with given arguments and keyword arguments (validating them before)

        Args:
            arguments: list of arguments
            keyword_arguments: dictionary containing keyword arguments
        """
        self.validate_args(arguments)
        self.validate_kwargs(keyword_arguments)

        return self.function(*arguments, **keyword_arguments)
