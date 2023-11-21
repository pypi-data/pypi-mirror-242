# -*- coding: utf-8; -*-
################################################################################
#
#  WuttJamaican -- Base package for Wutta Framework
#  Copyright © 2023 Lance Edgar
#
#  This file is part of Wutta Framework.
#
#  Wutta Framework is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  Wutta Framework is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  Wutta Framework.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
WuttJamaican - command framework
"""

import argparse
import logging
import sys

from wuttjamaican import __version__
from wuttjamaican.util import load_entry_points


log = logging.getLogger(__name__)


class Command:
    """
    Primary command for the application.

    A primary command will usually have multiple subcommands it can
    run.  The typical command line interface is like:

    .. code-block:: none

       <command> [command-options] <subcommand> [subcommand-options]

    :class:`Subcommand` will contain most of the logic, in terms of
    what actually happens when it runs.  Top-level commands are mostly
    a stub for sake of logically grouping the subcommands.

    The base class serves as the primary ``wutta`` command for
    WuttJamaican.  Most apps will subclass this and register their own
    top-level command, and create subcommands as needed.

    To do that, first create your Command class, and a ``main()``
    entry point (e.g. in ``poser/commands.py``)::

       import sys
       from wuttjamaican.commands import Command

       class Poser(Command):
           name = 'poser'
           description = 'my custom top-level command'
           version = '0.1'

       def main(*args):
           args = list(args) or sys.argv[1:]
           cmd = Poser()
           cmd.run(*args)

    Then register the ``main()`` entry point (in your ``setup.cfg``):

    .. code-block:: ini

       [options.entry_points]
       console_scripts =
           poser = poser.commands:main

    Next time your (``poser``) package is installed, the command will be
    available, so you can e.g.:

    .. code-block:: sh

       cd /path/to/venv
       bin/poser --help

    And see :class:`Subcommand` for info about adding those.

    Note that you can add as many top-level commands as needed.  Most
    apps only need one of course, but there is no actual limit.

    .. attribute::  name

       Name of the primary command, e.g. ``wutta``

    .. attribute:: description

       Description of the app itself or the primary command.

    .. attribute:: version

       Version string for the app or primary command.
    """
    name = 'wutta'
    version = __version__
    description = "Wutta Software Framework"

    def __init__(self, **kwargs):

        self.name = kwargs.get('name', self.name)

        self.stdout = kwargs.get('stdout', sys.stdout)
        self.stderr = kwargs.get('stderr', sys.stderr)

        self.subcommands = (kwargs.get('subcommands') or
                            load_entry_points(f'{self.name}.commands'))

    def sorted_subcommands(self):
        """
        Get a sorted list of subcommand classes.
        """
        return [self.subcommands[name]
                for name in sorted(self.subcommands)]

    def print_help(self):
        """
        Print usage help text for the main command.
        """
        self.parser.print_help()

    def run(self, *args):
        """
        Parse command line arguments and execute appropriate
        subcommand.

        Or, if requested, or args are ambiguous, show help for either
        the top-level or subcommand.

        Usually of course this method is invoked by way of command
        line.  But if you need to run it programmatically, you must
        specify the full command line args *except* not the top-level
        command name.  So for example::

           from wuttjamaican.commands import Command

           cmd = Command()
           assert cmd.name == 'wutta'
           cmd.run('setup', '--help')
        """
        subcommands = ""
        for subcmd in self.sorted_subcommands():
            subcommands += f"  {subcmd.name:<20s}  {subcmd.description}\n"

        epilog = f"""\
subcommands:
{subcommands}

also try: {self.name} <subcommand> -h
"""

        self.parser = parser = CommandArgumentParser(
            prog=self.name,
            description=self.description,
            add_help=False,
            usage=f"{self.name} [options] <subcommand> [subcommand-options]",
            epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument('-c', '--config', metavar='PATH',
                            action='append', dest='config_paths',
                            help="Config path (may be specified more than once)")

        parser.add_argument('--plus-config', metavar='PATH',
                            action='append', dest='plus_config_paths',
                            help="Extra configs to load in addition to normal config")

        parser.add_argument('-P', '--progress', action='store_true', default=False,
                            help="Report progress when relevant")

        parser.add_argument('-V', '--version', action='version',
                            version=f"%(prog)s {self.version}")

        # primary parser gets first pass at full args, and stores
        # everything not used within args.argv
        args = parser.parse_args(args)
        if not args or not args.argv:
            self.print_help()
            sys.exit(1)

        # then argv should include <subcommand> [subcommand-options]
        subcmd = args.argv[0]
        if subcmd in self.subcommands:
            if '-h' in args.argv or '--help' in args.argv:
                subcmd = self.subcommands[subcmd](self)
                subcmd.print_help()
                sys.exit(0)
        else:
            self.print_help()
            sys.exit(1)

        # make the config object
        from wuttjamaican.conf import make_config
        self.config = make_config(args.config_paths,
                                  plus_files=args.plus_config_paths)

        # invoke subcommand
        log.debug("running command line: %s", sys.argv)
        subcmd = self.subcommands[subcmd](self)
        subcmd._run(*args.argv[1:])


class CommandArgumentParser(argparse.ArgumentParser):
    """
    Custom argument parser for use with :class:`Command`.

    This overrides some of the parsing logic which is specific to the
    primary command object, to separate command options from
    subcommand options.

    This is documented as FYI but you probably should not need to know
    about or try to use this yourself.  It will be used automatically
    by ``Command`` or a subclass thereof.
    """

    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        args.argv = argv
        return args


class Subcommand:
    """
    Base class for application subcommands.

    Subcommands are where the real action happens.  Each must define
    the :meth:`run()` method with whatever logic is needed.  They can
    also define :meth:`add_args()` to expose options.

    Subcommands always belong to a top-level command - the association
    is made by way of entry point registration, and the constructor
    for this class.

    :param command: Reference to top-level :class:`Command` object.

    Note that unlike :class:`Command`, the base ``Subcommand`` does
    not correspond to any real subcommand for WuttJamaican.  (It's
    *only* a base class.)  For a real example see
    :class:`~wuttjamaican.commands.setup.Setup`.

    In your project you can define new subcommands for any top-level
    command.  For instance to add a ``hello`` subcommand to the
    ``poser`` command example (cf. :class:`Command` docs):

    First create a Subcommand class (e.g. by adding to
    ``poser/commands.py``)::

       from wuttjamaican.commands import Subcommand

       class Hello(Subcommand):
           \"""
           Say hello to the user
           \"""
           name = 'hello'
           description = __doc__.strip()

           def add_args(self):
               self.parser.add_argument('--foo', default='bar', help="Foo value")

           def run(self, args):
               print("hello, foo value is:", args.foo)

    You may notice there is nothing in that subcommand definition
    which ties it to the ``poser`` top-level command.  That is done by
    way of another entry point in your ``setup.cfg`` file:

    .. code-block:: ini

       [options.entry_points]
       poser.commands =
           hello = poser.commands:Hello

    Next time your (``poser``) package is installed, the subcommand
    will be available, so you can e.g.:

    .. code-block:: sh

       cd /path/to/venv
       bin/poser hello --help

    Since the connection between command and subcommand is only "real"
    if there is an entry point, this means a) you can add the
    subcommand under *any* top-level command, but also b) you could
    technically add it to multiple top-level commands.  So for
    instance in addition to the above entry point you might also do:

    .. code-block:: ini

       [options.entry_points]
       wutta.commands =
           hello = poser.commands:Hello

    After re-installing your package then these commands would do the
    same thing:

    .. code-block:: sh

       cd /path/to/venv
       bin/poser hello
       bin/wutta hello
    """
    name = 'UNDEFINED'
    description = "TODO: not defined"

    def __init__(
            self,
            command,
    ):
        self.command = command

        self.stdout = self.command.stdout
        self.stderr = self.command.stderr

        self.parser = argparse.ArgumentParser(
            prog=f'{self.command.name} {self.name}',
            description=self.description)

        self.add_args()

    def add_args(self):
        """
        Configure additional args for the subcommand arg parser.

        Anything you setup here will then be available within
        :meth:`run()`.  You can add arguments directly to
        ``self.parser``, e.g.::

           self.parser.add_argument('--foo', default='bar', help="Foo value")

        See also docs for :meth:`python:argparse.ArgumentParser.add_argument()`.
        """

    def print_help(self):
        """
        Print usage help text for the subcommand.
        """
        self.parser.print_help()

    def _run(self, *args):
        args = self.parser.parse_args(args)
        return self.run(args)

    def run(self, args):
        """
        Run the subcommand logic.  Subclass should override this.

        :param args: Reference to the
           :class:`python:argparse.Namespace` object, as returned by
           the subcommand arg parser.

        The ``args`` should have values for everything setup in
        :meth:`add_args()`.  For example if you added the ``--foo``
        arg then here in ``run()`` you can do::

           print("foo value is:", args.foo)

        Usually of course this method is invoked by way of command
        line. But if you need to run it programmatically, you should
        *not* try to invoke this method directly.  Instead create the
        ``Command`` object and invoke its :meth:`~Command.run()`
        method.

        For a command line like ``bin/poser hello --foo=baz`` then,
        you might do this::

           from poser.commands import Poser

           cmd = Poser()
           assert cmd.name == 'poser'
           cmd.run('hello', '--foo=baz')
        """
        self.stdout.write("TODO: command logic not yet implemented\n")


def main(*args):
    """
    Primary entry point for the ``wutta`` command.
    """
    args = list(args) or sys.argv[1:]

    cmd = Command()
    cmd.run(*args)
