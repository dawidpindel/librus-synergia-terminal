from .librus_session import LibrusSession
from .librus_terminal import LibrusTerminal
from .commands import Command

from . import messages_commands
from . import other_commands
from . import authorization_commands
from . import help_command
from . import grades_commands


def main():
    commands = {
        "gmes": Command(messages_commands.get_messages_command),
        "exit": Command(other_commands.exit_command),
        "cls": Command(other_commands.clear_command),
        "clear": Command(other_commands.clear_command),
        "login": Command(authorization_commands.login_command),
        "logout": Command(authorization_commands.logout_command),
        "rmes": Command(messages_commands.read_message_command),
        "help": Command(help_command.help_command),
        "abs": Command(other_commands.absences_command),
        "grades": Command(grades_commands.grades_command)
    }

    session = LibrusSession()

    terminal = LibrusTerminal(session, commands)

    terminal.run_terminal()


if __name__ == "__main__":
    main()
