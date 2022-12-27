import typing

from .command_parsing import parse_command
from .commands import Command
from .librus_session import LibrusSession
from . import exceptions


class LibrusTerminal():

    enable_color = True

    def __init__(self, session: LibrusSession, commands: typing.Dict[str, Command]) -> None:
        self.session: LibrusSession = session
        self.commands: typing.Dict[str, Command] = commands

    @property
    def _input_message(self) -> str:
        logged_in = True

        try:
            self.session.check_if_expired()

        except exceptions.TerminalAuthorizationException as exception:
            logged_in = False

        attrs = ("logged in", "BLUE") if logged_in else ("not logged in", "RED")

        message =\
            self._color("[Librus (", "GREEN") +\
            self._color(*attrs) +\
            self._color(")] >> ", "GREEN")

        return message

    @classmethod
    def _color(cls, text, col):

        if not cls.enable_color:
            return text

        colors = {
            "BLUE": '\033[94m',
            "GREEN": '\033[92m',
            "YELLOW": '\033[93m',
            "RED": '\033[91m',
            "ENDC": '\033[0m',
        }

        col = colors.get(col, "")

        return col + text + (colors["ENDC"] if col else "")

    def run_terminal(self) -> None:
        while True:
            try:
                command = input(self._input_message)
            except KeyboardInterrupt:
                exit()

            if not command:
                continue

            try:
                options, arguments = parse_command(command)
            except exceptions.ParsingException as exception:
                print(str(exception), *exception.errors)
                continue

            except ValueError as exception:
                print("niepoprawnie sformatowana komenda", str(exception))
                continue

            command, options = options[0], options[1:]

            if command not in self.commands:
                print("nie ma takiej komendy:", command)
                continue

            try:
                result = self.commands[command].run_command([self.session, *options], arguments)

            except exceptions.TerminalAuthorizationException as exception:
                print(exception.message_for_user)

            except exceptions.NotEnoughArgumentsException as exception:
                print(f"not enough options", ", ".join(exception.lacking), "are missing")

            except exceptions.InvalidArgumentType as exception:
                print(f"invalid option type, expected {exception.expected_type.__name__}, got {exception.passed_type.__name__}")

            except exceptions.TooManyArguments as exception:
                print(f"too many options")

            except exceptions.UnknownKeywordArgumenException as exception:
                print("unknown argument:", exception.arg_name)

            except exceptions.InvalidKeywordArgumentType as exception:
                print(f"invalid argument type ({exception.arg_name}), expected {exception.expected_type.__name__}, got {exception.passed_type.__name__}")

            except KeyboardInterrupt as exception:
                continue
