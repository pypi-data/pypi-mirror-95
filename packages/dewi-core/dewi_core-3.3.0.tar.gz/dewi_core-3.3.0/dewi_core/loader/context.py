# Copyright 2015-2020 Laszlo Attila Toth
# Distributed under the terms of the GNU Lesser General Public License v3

import collections.abc

from dewi_core.commandregistry import CommandRegistry, CommandRegistrar


class ContextError(Exception):
    pass


class ContextEntryNotFound(ContextError):
    pass


class ContextEntryAlreadyRegistered(ContextError):
    pass


class Context(collections.abc.Mapping):
    """
    A context is a generic purpose registry, which helps
    communicate between different parts of the code. Instead of a global variable
    or module is for storing object(s), the context can be used and passed around
    the necessary objects and functions.

    An example: a CommandRegistry object can be registered into this context.
    """

    def __init__(self):
        registry = CommandRegistry()
        self._entries = {
            'commands': CommandRegistrar(registry),
            'commandregistry': registry,
        }

    @property
    def command_registry(self) -> CommandRegistry:
        return self._entries['commandregistry']

    @property
    def commands(self) -> CommandRegistrar:
        return self._entries['commands']

    def register(self, name: str, value):
        """
        Registers an element into the context. It doesn't support overwriting already
        registered entries, in that case `ContextEntryAlreadyRegistered` will be raised.

        :param name: the name of the new entry
        :param value: the value of the new entry
       """
        if name in self._entries:
            raise ContextEntryAlreadyRegistered("Context entry {!r} already registered".format(name))
        self._entries[name] = value

    def unregister(self, name: str):
        """
        Unregisters an already registered entry
        :param name: The name of the entry to be unregistered
        """
        self._check_entry(name)

        del self._entries[name]

    def _check_entry(self, name: str):
        if name not in self._entries:
            raise ContextEntryNotFound("Requested context entry {!r} is not registered".format(name))

    def __len__(self):
        return len(self._entries)

    def __getitem__(self, item):
        self._check_entry(item)

        return self._entries[item]

    def __contains__(self, item):
        return item in self._entries

    def __iter__(self):
        return iter(self._entries)
