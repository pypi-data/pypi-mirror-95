#!/usr/bin/env python

# Copyright (C) 2018 Miguel Simoes, miguelrsimoes[a]yahoo[.]com
# For conditions of distribution and use, see copyright notice in lnsync.py

"""
Overview:

Each command accepts one or more tree positional arguments (directories and/or
offline tree files), as well as optional arguments.

Some optional arguments apply to some or all tree arguments.

These tree options and they either apply to the next tree in the command line,
to all trees following, or to all trees.

Both a type and an action are used for tree arguments.

- The type (TreeLocation, TreeLocationOnline, TreeLocationOffline) gathers
information (partial, incomplete, provisional) that will be later used to create
the actual Tree object.

- The TreeLocationAction records the tree arguments found so far and applies the
options found so far. There is also an Action object to process a list of trees.

For tree options, an Action is used:

- TreeOptionAction registers that option in the parser namespace and
also, if global, applies the all previous tree arguments.
"""

# pylint: disable=no-member, redefined-builtin

import os
import argparse

from lnsync_pkg.sqlpropdb import SQLPropDBManager
from lnsync_pkg.glob_matcher import Pattern, merge_pattern_lists
import lnsync_pkg.printutils as pr
from lnsync_pkg.modaltype import ONLINE, OFFLINE
from lnsync_pkg.argparse_scoped_options import ScOptArgAction, ScPosArgAction
from lnsync_pkg.prefixdbname import mode_from_location, pick_db_basename
from lnsync_pkg.fstr_type import fstr, fstr2str
from lnsync_pkg.argparse_config import NoSectionError, NoOptionError, \
    ArgumentParserConfig as ArgumentParser

DEFAULT_DBPREFIX = fstr("lnsync-")

def is_subdir(path, directory):
    """
    Test if 'path' is a subdir of 'directory'.
    """
    relative = os.path.relpath(path, directory)
    return not relative.startswith(fstr(os.pardir + os.sep))

class TreeLocationAction(ScPosArgAction):
    def __call__(self, parser, namespace, val, option_string=None):
        super().__call__(parser, namespace, val, option_string)
        tree_args = getattr(namespace, "sc_pos_args", [])
        locations_seen = []
        for tree_arg in tree_args:
            this_location = tree_arg.real_location
            if this_location in locations_seen:
                raise ValueError(
                    "duplicate location: %s" % (fstr2str(this_location,)))

#class TreeLocationListAction(ScPosArgListAction):
#    pass

class TreeLocation:
    """
    Immutable data: mode, cmd_location (what was specified in the command line),
    (either a directory in online mode or a database file in offline mode).

    Also available: real_path (the canonical form of cmd_location, via
    os.path.realpath).

    For online trees, the dblocation can only be determined when a database
    prefix or an altogether different database location is provided.
    An explicit db location takes precedence over a db prefix

    Attributes that will results in Tree object init keywords are stored
    in the namespace attribute (a dictionary, actually).
    """

    def __new__(cls, location, mandatory_mode=None):
        """
        Make it equivalent to create instances with TreeLocationOnline(loc),
        TreeLocation(loc, mode=ONLINE), even TreeLocation(loc) so long as loc is
        a dir.
        """
        mode = mode_from_location(fstr(location), mandatory_mode)
        assert mode in (ONLINE, OFFLINE)
        newcls = {ONLINE: TreeLocationOnline, OFFLINE:TreeLocationOffline}[mode]
        newobj = super().__new__(newcls)
        newobj.mode = mode
        if not isinstance(newobj, cls):
            newobj.__init__(location)
        return newobj

    def __init__(self, location):
        self.cmd_location = fstr(location)
        self.real_location = os.path.realpath(self.cmd_location)
        self.namespace = argparse.Namespace()
        setattr(self.namespace, "mode", self.mode)
        setattr(self.namespace, "dbmaker", SQLPropDBManager)

    def kws(self):
        """
        Return a dict suitable to initialize a proper Tree object,
        with at least mode, dbmaker, dbkwargs, root_path.
        """
        return vars(self.namespace)

    @staticmethod
    def merge_patterns(tree1, tree2):
        """
        Merge the exclude/include patterns of tree1 and tree2
        """
        tr1_pats = getattr(tree1.namespace, "exclude_patterns")
        tr2_pats = getattr(tree2.namespace, "exclude_patterns")
        merged_pats = merge_pattern_lists(tr1_pats, tr2_pats)
        setattr(tree1.namespace, "exclude_patterns", merged_pats)
        setattr(tree2.namespace, "exclude_patterns", merged_pats)


class TreeLocationOffline(TreeLocation):
    def __init__(self, cmd_location):
        super().__init__(cmd_location)
        setattr(self.namespace, "root_path", None)
        setattr(self.namespace, "dbkwargs", \
                {"dbpath":self.cmd_location, "root_path":None})

    def set_dbprefix(self, _dbprefix):
        # dbprefix option has no effect on offline trees
        pass

    def set_dblocation(self, _dbpath):
        # dblocation option has no effect on offline trees"
        pass

    def set_root_option(self, alt_root):
        pass

class TreeLocationOnline(TreeLocation):
    def __init__(self, cmd_location):
        super().__init__(cmd_location)
        self._kws = None
        self.dblocation = None
        self.dbprefix = None
        setattr(self.namespace, "root_path", self.cmd_location)
        self._alt_root = None

    def set_dbprefix(self, dbprefix):
        assert self._kws is None
        self.dbprefix = dbprefix

    def set_dblocation(self, dbpath):
        assert self._kws is None
        if os.path.exists(dbpath) and not os.path.isfile(dbpath):
            raise ValueError("not a file: %s" % (fstr2str(dbpath)))
        self.dblocation = dbpath

    def set_root_option(self, alt_root):
        """
        Assume alt_root is a readable directory.
        """
        if is_subdir(self.real_location, alt_root) \
                and not os.path.samefile(self.real_location, alt_root):
            self._alt_root = alt_root
        else:
            pr.trace("root does not apply: %s for %s",
                     fstr2str(alt_root), fstr2str(self.real_location))

    def kws(self):
        if self._kws is None:
            if self.dblocation is None:
                assert self.dbprefix is not None
                if self._alt_root is not None:
                    db_dir = self._alt_root
                else:
                    db_dir = self.cmd_location
                db_basename = pick_db_basename(db_dir, self.dbprefix)
                dblocation = os.path.join(db_dir, db_basename)
                pr.info("using %s for %s" %
                        (fstr2str(dblocation), fstr2str(self.cmd_location)))
            else:
                dblocation = self.dblocation
            setattr(self.namespace, "dbkwargs", \
                {"dbpath":dblocation, "root_path":self.cmd_location})
            self._kws = super().kws()
        return self._kws


class TreeOptionAction(ScOptArgAction):

    @staticmethod
    def sc_get_namespace(pos_val):
        return pos_val.namespace

    @staticmethod
    def make_comparator(location):
        """
        Makes a comparator function that will match config file section
        wildcards to the given dir location.
        """
        def comparator(section, location=location):
            section = fstr(section)
            try:
                if os.path.samefile(section, location):
                    return True
            except OSError:
                pass
            pat = Pattern(section)
            return pat.matches_path(location)
        return comparator

    def get_from_tree_section(self, arg_tree, key, merge_sections, type=None):
        """
        Return value corresponding to key from locations matching arg_tree's
        real location.
        """
        location = arg_tree.real_location
        section_name_comparator = TreeOptionAction.make_comparator(location)
        if type is None:
            type = self.type
        val = ArgumentParser.get_from_section(
            key,
            type=type,
            sect=section_name_comparator,
            merge_sections=merge_sections,
            nargs=self.nargs)
        return val

class ConfigTreeOptionAction(TreeOptionAction):
    def sc_apply_default(self, parser, namespace, pos_val):
        super().sc_apply_default(parser, namespace, pos_val)
        for opt_str in self.option_strings:
            if opt_str.startswith("--"):
                short_opt_str = opt_str[2:]
            elif opt_str.startswith("-"):
                short_opt_str = opt_str[1:]
            else:
                assert False, "unexpected option string: %s" % opt_str
            try:
                vals = self.get_from_tree_section(
                    pos_val,
                    short_opt_str,
                    type=self.type,
                    merge_sections=True)
                print("got ->", vals)
                if vals:
                    self.sc_action(
                        parser, namespace, pos_val, vals, opt_str)
            except (NoSectionError, NoOptionError):
                pass
