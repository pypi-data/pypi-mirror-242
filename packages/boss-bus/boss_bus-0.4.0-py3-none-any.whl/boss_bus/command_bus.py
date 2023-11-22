"""Interfaces for a form of message bus that executes commands.

Commands can only have one handler.

Classes:

    Command
    CommandBus
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, Type, TypeVar

from typeguard import typechecked

from boss_bus.handler import MissingHandlerError
from boss_bus.interface import Message, SupportsHandle

from ._utils.typing import get_annotations, type_matches


class Command(Message):
    """A form of message which only has one handler."""

    message_type: str = "command"


SpecificCommand = TypeVar("SpecificCommand", bound=Command)


class CommandHandler(ABC, SupportsHandle, Generic[SpecificCommand]):
    """A form of message which only has one handler."""

    @abstractmethod
    def handle(self, command: SpecificCommand) -> Any:
        """Perform actions using a specific command."""


class TooManyHandlersError(Exception):
    """Only one handler can be used with a command."""


class InvalidHandlerError(Exception):
    """The handler does not match the command."""


def _validate_handler(
    command_type: Type[Command], handler: CommandHandler[Any]
) -> None:
    if not type_matches(get_annotations(handler.handle)["command"], command_type):
        raise InvalidHandlerError(
            f"The handler '{handler}' does not match the command '{command_type.__name__}'"
        )


class CommandBus:
    """Executes commands using their associated handler.

    Example:
        >>> from tests.examples import PrintCommand, PrintCommandHandler
        >>> bus = CommandBus()
        >>> test_handler = PrintCommandHandler()
        >>> test_command = PrintCommand("Testing...")
        >>>
        >>> bus.register_handler(PrintCommand, test_handler)
        >>> bus.execute(test_command)
        Testing...
    """

    def __init__(self) -> None:
        """Creates a Command Bus."""
        self._handlers: dict[type[Command], CommandHandler[Any]] = {}

    @typechecked
    def register_handler(
        self,
        command_type: Type[SpecificCommand],
        handler: CommandHandler[SpecificCommand],
    ) -> None:
        """Register a single handler that will execute a type of Command.

        Example:
            >>> from tests.examples import PrintCommand, PrintCommandHandler
            >>> bus = CommandBus()
            >>> bus.register_handler(PrintCommand, PrintCommandHandler())
            >>>
            >>> bus.is_registered(PrintCommand)
            True
        """
        _validate_handler(command_type, handler)

        self._handlers[command_type] = handler

    @typechecked
    def remove_handler(self, command_type: Type[SpecificCommand]) -> None:
        """Remove a previously registered handler.

        Example:
            >>> from tests.examples import PrintCommand, PrintCommandHandler
            >>> bus = CommandBus()
            >>> bus.register_handler(PrintCommand, PrintCommandHandler())
            >>>
            >>> bus.remove_handler(PrintCommand)
            >>> bus.is_registered(PrintCommand)
            False
        """
        if command_type not in self._handlers:
            raise MissingHandlerError(
                f"A handler has not been registered for the command '{command_type.__name__}'"
            )

        del self._handlers[command_type]

    def is_registered(self, command_type: Type[SpecificCommand]) -> bool:
        """Checks if a command is registered with the bus.

        Example:
            >>> from tests.examples import PrintCommand, PrintCommandHandler
            >>> bus = CommandBus()
            >>> bus.register_handler(PrintCommand, PrintCommandHandler())
            >>>
            >>> bus.is_registered(PrintCommand)
            True
        """
        if command_type in self._handlers:
            return True

        return False

    @typechecked
    def execute(
        self,
        command: SpecificCommand,
        handler: CommandHandler[SpecificCommand] | None = None,
    ) -> Any:
        """Calls the handle method on a command's handler.

        Example:
            >>> from tests.examples import PrintCommand, PrintCommandHandler
            >>> bus = CommandBus()
            >>> test_handler = PrintCommandHandler()
            >>> test_command = PrintCommand("Testing...")
            >>>
            >>> bus.execute(test_command, test_handler)
            Testing...
        """
        if handler:
            _validate_handler(type(command), handler)

        matched_handler = self._handlers.get(type(command), handler)

        if handler and handler != matched_handler:
            raise TooManyHandlersError(
                f"A handler has already been registered for the command '{type(command).__name__}'"
            )

        if not matched_handler:
            raise MissingHandlerError(
                f"A handler has not been registered for the command '{type(command).__name__}'"
            )

        return matched_handler.handle(command)
