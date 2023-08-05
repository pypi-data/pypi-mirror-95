#!/usr/bin/env python

"""
Extend argparse to to apply options to specific positional arguments.

Copyright (C) 2021 Miguel Simoes, miguelrsimoes[a]yahoo[.]com

Allow each option to apply only to a certain type of positionals,
either to the following one, to all following, or to all.

Usage:
======

If a scoped optional applies to a scoped positional, then the optional's
Action scoped_action is called with the parser namespace and positional as
arguments, in the following order:

Whenever a scoped positional is parsed, all preceding applicable optionals are
applied to it.

Whenever a scoped optional is parsed, it is applied to all preceding positionals
to which it applies.

Scoped optional arguments should encapsulate their add_parser action keyword
argument in a call to ScopedOptional and likewise the target positional
arguments' action in ScopedPositional.

Subclasses can redefine the following methods:

- sc_action(self, parser, namespace, pos_val, opt_val, option_string=None)
    Called for positional args within scope of each option occurrence.

- sc_apply_default(self, parser, namespace, pos_val)
    Called once for all positional args.
    This is regardless of scope or of actual occurrances of the option in the
    command line.
    The default version sets the self.sc_dest attribute of pos_val to
    sc_default.

- sc_getnamespace(self, parser, namespace, pos_val)
    Called to get the object that will get the positional argument attributes.
    (By default, it is the pos_val object itself.)

Implementation:
===============

For each occurrence of an optional argument, an OptionCall instance is created
and added to a list kept in the namespace.
"""

# pylint: disable=function-redefined, protected-access

import argparse
import lnsync_pkg.printutils as pr

SC_ALL = 1 # Default
SC_NEXT = 2
SC_FOLLOWING = 3

class _OptionCall:
    """
    Represents an occurrence of an option in the command line.
    (Corresponding to __call__ invokations by argparse)
    These are saved and applied to subsequent positionals,
    as needed.
    """
    def __init__(self, parser, namespace, opt_val, option_string, opt_action):
        self.parser = parser
        self.namespace = namespace
        self.opt_val = opt_val
        self.option_string = option_string
        self.opt_action = opt_action

    def _sc_action(self, pos_arg):
        pr.trace("applying: %s %s", self.option_string, self.opt_val)
        self.opt_action.sc_action(self.parser, self.namespace,
                                  pos_arg, self.opt_val, self.option_string)

class ScOptArgAction(argparse.Action):
    """
    Base for scoped optional argument actions.
    """

    def __init__(self, *args, sc_scope=None, sc_action=None,
                 nargs=None, **kwargs):
        """
        scope is one of "all", "next", "following"
        sc_action is a function that accepts
            (parser, namespace, val, option_string=None, sc_namespace)
            and applies the option to the positional.
        or it may be a string:
        - "store": simply store the value into sc_namespace, under sc_dest.
        - "store_true": store the value in the tree kwargs in dest, apply
            True default, and also interpret options prefixed by "--no-")
            This forces nargs to be 0.
        - "append": append to a list of values, starting from an empty list.

        If the scope is "all", these actions are also taken on the main
        namespace.
        """
        dest = kwargs.pop("dest")
        self.sc_dest = kwargs.pop("sc_dest", dest)
        if sc_action == "store_true":
            nargs = 0
        super().__init__(*args, dest=dest, nargs=nargs, **kwargs)
        if "default" in kwargs:
            self.sc_default = kwargs["default"]
        if not sc_scope in ("all", "next", "following"):
            assert sc_scope in ("all", "next", "following")
        self.sc_scope = sc_scope

        if sc_action == "store":
            def sc_action(_parser, namespace, pos_val, opt_val, _option_string,
                          _sc_dest=self.sc_dest, _sc_scope=sc_scope,
                          _dest=dest):
                sc_ns = self.sc_get_namespace(pos_val)
                setattr(sc_ns, _sc_dest, opt_val)
                if _sc_scope == "all":
                    setattr(namespace, _dest, opt_val)
        elif sc_action == "store_true":
            def sc_action(_parser, namespace, pos_val, _opt_val, option_string,
                          _sc_dest=self.sc_dest, _sc_scope=sc_scope,
                          _dest=dest):
                sc_ns = self.sc_get_namespace(pos_val)
                if option_string[0:5] == "--no-":
                    val = False
                else:
                    val = True
                setattr(sc_ns, _sc_dest, val)
                if _sc_scope == "all":
                    setattr(namespace, _dest, val)
        elif sc_action == "append":
            def sc_action(_parser, namespace, pos_val, opt_val, _option_string,
                          _sc_dest=self.sc_dest, _sc_scope=sc_scope,
                          _dest=dest, _nargs=self.nargs):
                def do_append(val, to_this):
                    if _nargs is not None:
                        assert isinstance(val, list)
                        return to_this + val
                    else:
                        return to_this + [val]
                sc_ns = self.sc_get_namespace(pos_val)
                prev = getattr(sc_ns, _sc_dest, [])
                if prev is None:
                    prev = []
                prev = do_append(opt_val, prev)
                setattr(sc_ns, _sc_dest, prev)
                if _sc_scope == "all":
                    prev = getattr(namespace, _dest, [])
                    if prev is None:
                        prev = []
                    prev = do_append(opt_val, prev)
                    setattr(namespace, _dest, prev)
        elif callable(sc_action):
            pass
        if sc_action is not None:
            self.sc_action = sc_action

    @staticmethod
    def sc_get_namespace(pos_val):
        return pos_val

    def sc_apply_default(self, _parser, namespace, pos_val):
        """
        Apply this option in default form to the pos_arg object.
        """
        if hasattr(self, "sc_default"):
            sc_ns = self.sc_get_namespace(pos_val)
            if not hasattr(sc_ns, self.sc_dest):
                setattr(sc_ns, self.sc_dest, self.sc_default)
#   iffy TODO
        if hasattr(self, "default"):
            if not hasattr(namespace, self.dest):
                setattr(namespace, self.dest, self.default)

    def __call__(self, parser, namespace, opt_val, option_string=None):
        this_opt_call = _OptionCall(parser, namespace,
                                    opt_val, option_string, self)
        prec_opt_calls = getattr(namespace, "_sc_opt_calls", [])
        prec_opt_calls.append(this_opt_call)
        setattr(namespace, "_sc_opt_calls", prec_opt_calls)
        if self.sc_scope == "all":
            preceding_pos_args = getattr(namespace, "sc_pos_args", [])
            for pos_arg in preceding_pos_args:
                this_opt_call._sc_action(pos_arg)

class ScPosArgAction(argparse.Action):
    """
    Base for scoped positional argument Actions, for one or zero argument
    values.
    """
    def __call__(self, parser, namespace, pos_arg, option_string=None):
        if self.nargs == "+":
            assert isinstance(pos_arg, list)
            for pos_val in pos_arg:
                self._process_pos_arg(parser, namespace, pos_val)
            setattr(namespace, self.dest, pos_arg)
        else:
            assert not isinstance(pos_arg, list)
            self._process_pos_arg(parser, namespace, pos_arg)
            setattr(namespace, self.dest, pos_arg)

    def _process_pos_arg(self, parser, namespace, pos_arg):
        self._apply_preceding_opt_args(parser, namespace, pos_arg)
        self._fill_in_defaults(parser, namespace, pos_arg)
        self._save_to_namespace(parser, namespace, pos_arg)

    @staticmethod
    def _fill_in_defaults(parser, namespace, pos_arg):
        for action in parser._actions:
            if isinstance(action, ScOptArgAction):
                action.sc_apply_default(parser, namespace, pos_arg)

    @staticmethod
    def _apply_preceding_opt_args(_parser, namespace, pos_arg):
        preceding_opt_calls = getattr(namespace, "_sc_opt_calls", [])
        for opt_call in preceding_opt_calls:
            opt_call._sc_action(pos_arg)
        remaining_opt_calls = \
            [opt for opt in preceding_opt_calls \
             if opt.opt_action.sc_scope != "next"]
        setattr(namespace, "_sc_opt_calls", remaining_opt_calls)

    @staticmethod
    def _save_to_namespace(_parser, namespace, pos_val):
        prec_pos_args = getattr(namespace, "sc_pos_args", [])
        prec_pos_args.append(pos_val)
        setattr(namespace, "sc_pos_args", prec_pos_args)
