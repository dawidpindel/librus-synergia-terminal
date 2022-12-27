class ParsingException(Exception):
    def __init__(self, message, errors) -> None:
        super().__init__(message)

        self.errors = errors


class TerminalAuthorizationException(Exception):
    def __init__(self, message, message_for_user) -> None:
        super().__init__(message)

        self.message_for_user = message_for_user


class NotEnoughArgumentsException(Exception):

    def __init__(self, message: str, lacking: list[str]) -> None:
        super().__init__(message)

        self.lacking = lacking


class InvalidArgumentType(Exception):

    def __init__(self, message: str, passed_type: type, expected_type: type, arg_name: str, arg_index: int) -> None:
        super().__init__(message)

        self.passed_type = passed_type
        self.expected_type = expected_type
        self.arg_name = arg_name
        self.arg_index = arg_index


class TooManyArguments(Exception):
    def __init__(self, message: str, unexpected: list[str]) -> None:
        super().__init__(message)

        self.unexpected = unexpected


class UnknownKeywordArgumenException(Exception):
    def __init__(self, message: str, arg_name: str) -> None:
        super().__init__(message)

        self.arg_name = arg_name


class InvalidKeywordArgumentType(Exception):

    def __init__(self, message: str, passed_type: type, expected_type: type, arg_name: str) -> None:
        super().__init__(message)

        self.passed_type = passed_type
        self.expected_type = expected_type
        self.arg_name = arg_name
