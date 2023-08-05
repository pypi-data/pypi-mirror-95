#!/usr/bin/env python

"""
Copyright (C) 2021 Miguel Simoes, miguelrsimoes[a]yahoo[.]com

Command handlers do_sync, do_rsync, do_search, do_cmp, do_check
"""

# pylint: disable=too-many-nested-blocks, too-many-statements

import os
import pipes

from lnsync_pkg.sqlpropdb import SQLPropDBManager
import lnsync_pkg.printutils as pr
from lnsync_pkg.miscutils import is_subdir
from lnsync_pkg.human2bytes import bytes2human
import lnsync_pkg.fdupes as fdupes
from lnsync_pkg.prefixdbname import pick_db_basename
from lnsync_pkg.fileid import make_id_computer
from lnsync_pkg.groupedfileprinter import GroupedFileListPrinter
from lnsync_pkg.fstr_type import fstr, fstr2str
from lnsync_pkg.matcher import TreePairMatcher
from lnsync_pkg.hashtree import \
    FileHashTree, TreeError, PropDBException
from lnsync_pkg.lnsync_treeargs import \
    TreeLocation, TreeLocationOnline, DEFAULT_DBPREFIX
from lnsync_pkg.modaltype import ONLINE, OFFLINE

_QUOTER = pipes.quote

def do_lookup_and_rehash(location_arg, relpaths, force_rehash):
    error_found = False
    with FileHashTree(**location_arg.kws()) as tree:
        for relpath in relpaths:
            file_obj = tree.follow_path(relpath)
            fname = tree.printable_path(relpath, pprint=_QUOTER)
            if file_obj is None or not file_obj.is_file():
                pr.error("not a file: %s" % fname)
                error_found = True
                continue
            if force_rehash:
                try:
                    tree.recompute_prop(file_obj)
                except PropDBException as exc:
                    pr.debug(str(exc))
                    msg = "rehashing %s: %s" %  (fname, str(exc))
                    pr.error(msg)
                    error_found = True
                    continue
            hash_val = tree.get_prop(file_obj)
                # getprop Raises TreeError if no prop.
            pr.print("%d %s" % (hash_val, fname))
    return 1 if error_found else 0

def do_sync(args):
    TreeLocation.merge_patterns(args.source, args.target)
    with FileHashTree(**args.source.kws()) as src_tree:
        with FileHashTree(**args.target.kws()) as tgt_tree:
            FileHashTree.scan_trees_async([src_tree, tgt_tree])
            pr.progress("matching...")
            matcher = TreePairMatcher(src_tree, tgt_tree)
            if not matcher.do_match():
                raise NotImplementedError("match failed")
            tgt_tree.writeback = not args.dry_run
            for cmd in matcher.generate_sync_cmds():
                args_str = " ".join(
                    _QUOTER(fstr2str(arg)) for arg in cmd[1:])
                cmd_str = cmd[0] + " " + args_str
                pr.print(cmd_str)
                try:
                    tgt_tree.exec_cmd(cmd)
                except OSError as exc:
                    # E.g. if no linking support on target.
                    msg = "could not execute: " + cmd_str
                    raise RuntimeError(msg) from exc
            pr.progress("syncing empty dirs")
            dirs_to_rm_set = set()
            dirs_to_rm_list = []
            for dir_obj, _parent_obj, relpath \
                    in tgt_tree.walk_paths(
                            recurse=True, topdown=False,
                            dirs=True, files=False):
                if all((obj.is_dir() and obj in dirs_to_rm_set) \
                       for obj in dir_obj.entries.values()):
                    if src_tree.follow_path(relpath) is None:
                        dirs_to_rm_set.add(dir_obj)
                        dirs_to_rm_list.append(dir_obj)
            for dobj in dirs_to_rm_list:
                cmd_str = "rmdir %s" % \
                            (_QUOTER(fstr2str(dobj.get_relpath()),))
                pr.print(cmd_str)
                # Next follows tgt_tree.writeback.
                tgt_tree.rm_dir_writeback(dobj)
            pr.debug("sync done")

def do_rsync(args, rsyncargs):
    """
    Print (and optionally execute) a suitable rsync command.
    """
    src_dir = fstr2str(args.source.real_location)
    tgt_dir = fstr2str(args.target.real_location)
    if src_dir[-1] != os.sep:
        src_dir += os.sep # rsync needs trailing / on sourcedir.
    src_dir = _QUOTER(src_dir)
    tgt_dir = _QUOTER(tgt_dir)
    while tgt_dir[-1] == os.sep:
        tgt_dir = tgt_dir[:-1]

    # Options for rsync: recursive, preserve hardlinks.
    rsync_opts = "-r -H --size-only --progress"
    if args.maxsize >= 0:
        rsync_opts += " --max-size=%d" % args.maxsize
    if args.dry_run:
        rsync_opts += " -n"

    # Exclude databases at both ends.
    def get_exclude_str(namespace):
        if namespace.dblocation is not None:
            relpath = \
                is_subdir(os.path.dirname(namespace.dblocation), \
                          namespace.real_location)
            if relpath:
                exclude_str = '/%s' % fstr2str(relpath)
            else:
                exclude_str = None
        else:
            exclude_str = '/%s[0-9]*[0-9].db' % fstr2str(namespace.dbprefix)
        return exclude_str
    src_exclude_str = get_exclude_str(args.source)
    if src_exclude_str is not None:
        rsync_opts += r' --exclude="%s"' % src_exclude_str
    tgt_exclude_str = get_exclude_str(args.target)
    if tgt_exclude_str is not None and tgt_exclude_str != src_exclude_str:
        rsync_opts += r' --exclude="%s"' % tgt_exclude_str

    for pat in getattr(args.source.namespace, "exclude_patterns", []):
        cmd_pattern = pat.to_fstr()
        rsync_opts += \
            ' --%s="%s"' % \
                ("exclude" if pat.is_exclude() else "include",
                 fstr2str(cmd_pattern))

    if rsyncargs:
        rsync_opts += " " + " ".join(rsyncargs)

    rsync_cmd = "rsync %s %s %s" % (rsync_opts, src_dir, tgt_dir)
    pr.print(rsync_cmd)

    if args.execute:
        try:
            os.system(rsync_cmd)
        except OSError as exc:
            msg = "executing %s: %s" % (rsync_cmd, str(exc))
            pr.error(msg)
            raise RuntimeError(msg) from exc

def do_search(args):
    """
    Search for files by relative pattern glob pattern.
    """

    def print_file_match(tree, fobj):
        pr.print(tree.printable_path(files_paths_matched[fobj][0]))
        for fpath in files_paths_matched[fobj][1:]:
            pr.print(" ", tree.printable_path(fpath))
        if args.alllinks:
            for fpath in fobj.relpaths:
                if fpath not in files_paths_matched[fobj]:
                    pr.print(" ", tree.printable_path(fpath))

    def search_dir(tree, dir_obj, patterns):
        nonlocal files_paths_to_check
        nonlocal files_paths_matched
        if not patterns:
            return
        tree.scan_dir(dir_obj)
        patterns = set(patterns)

        def handle_file_match(obj, basename):
            path = os.path.join(dir_obj.get_relpath(), basename)
            if args.hardlinks or len(obj.relpaths) == 1:
                pr.print(tree.printable_path(path))
            else:
                if obj not in files_paths_to_check:
                    files_paths_to_check[obj] = list(obj.relpaths)
                    files_paths_matched[obj] = []
                assert path in files_paths_to_check[obj]
                files_paths_to_check[obj].remove(path)
                files_paths_matched[obj].append(path)
                if not files_paths_to_check[obj]:
                    print_file_match(tree, obj)
                    del files_paths_to_check[obj]
                    del files_paths_matched[obj]

        for basename, obj in dir_obj.entries.items():
            if obj.is_file():
                for pat in patterns:
                    if pat.matches_exactly(basename):
                        handle_file_match(obj, basename)
                    break
            if obj.is_dir():
                subdir_patterns = \
                    [p for p in patterns if not p.is_anchored()]
                for pat in patterns:
                    for tail_pat in pat.head_to_tails(basename):
                        if not tail_pat.is_empty():
                            subdir_patterns.append(tail_pat)
                if subdir_patterns:
                    search_dir(tree, obj, subdir_patterns)

    tree_kws = (treearg.kws() for treearg in args.locations)
    with FileHashTree.listof(tree_kws) as all_trees:
        for tree in all_trees:
            if not args.hardlinks:
                files_paths_to_check = {}
                files_paths_matched = {}
                tree.scan_subtree()
            search_dir(tree, tree.rootdir_obj, [args.glob])
            if not args.hardlinks:
                for fobj in files_paths_matched:
                    print_file_match(tree, fobj)


def do_cmp(args):
    """
    Recursively compare files and dirs in two directories.
    """
    TreeLocation.merge_patterns(args.leftlocation, args.rightlocation)
    def cmp_files(path, left_obj, right_obj):
        left_prop, right_prop = None, None
        if left_obj.file_metadata.size != right_obj.file_metadata.size:
            pr.print("files differ in size: %s" % fstr2str(path,))
            return
        try:
            left_prop = left_tree.get_prop(left_obj)
            right_prop = right_tree.get_prop(right_obj)
        except TreeError:
            if left_prop is None:
                err_path = \
                    left_tree.printable_path(path, pprint=_QUOTER)
            else:
                err_path = \
                    right_tree.printable_path(path, pprint=_QUOTER)
            pr.error("reading %s, ignoring" % (err_path,))
        else:
            if left_prop != right_prop:
                pr.print("files differ in content: %s" % fstr2str(path,))
            else:
                if args.hardlinks or \
                    (len(left_obj.relpaths) \
                        == len(right_obj.relpaths) == 1):
                    pr.info("files equal: %s" % fstr2str(path,))
                else:
                    left_links = list(left_obj.relpaths)
                    right_links = list(right_obj.relpaths)
                    for left_link in left_obj.relpaths:
                        if left_link in right_links:
                            left_links.remove(left_link)
                            right_links.remove(left_link)
                    if not left_links and not right_links:
                        pr.info("files equal: %s" % fstr2str(path,))
                    else:
                        msg = \
                            "files equal, link mismatch: %s" % \
                                 fstr2str(path,)
                        pr.print(msg)
                        for lnk in left_links:
                            pr.print(
                                " left only link: %s" % \
                                    fstr2str(lnk,))
                        for lnk in right_links:
                            pr.print(" right only link: %s" % \
                                fstr2str(lnk,))
    def cmp_subdir(dirpaths_to_visit, cur_dirpath):
        for left_obj, basename in \
                left_tree.walk_dir_contents(cur_dirpath, dirs=True):
            left_path = os.path.join(cur_dirpath, basename)
            right_obj = right_tree.follow_path(left_path)
            if right_obj is None or right_obj.is_excluded():
                if left_obj.is_file():
                    pr.print("left only: %s" % fstr2str(left_path))
                elif left_obj.is_dir():
                    pr.print("left only: %s" %
                             fstr2str(left_path+fstr(os.path.sep)))
                else:
                    raise RuntimeError(
                        "unexpected left object: " + fstr2str(left_path))
            elif left_obj.is_file():
                if  right_obj.is_file():
                    cmp_files(left_path, left_obj, right_obj)
                elif right_obj.is_dir():
                    pr.print("left file vs right dir: %s" % fstr2str(left_path))
                else:
                    pr.print("left file vs other: %s" % fstr2str(left_path))
            elif left_obj.is_dir():
                if right_obj.is_dir():
                    dirpaths_to_visit.append(left_path)
                elif right_obj.is_file():
                    pr.print("left dir vs right file: %s" %
                             fstr2str(left_path))
                else:
                    pr.print("left dir vs other: %s" %
                             fstr2str(left_path+fstr(os.path.sep)))
            else:
                raise RuntimeError(
                    "unexpected left object: " + fstr2str(left_path))
        for right_obj, basename in \
                right_tree.walk_dir_contents(cur_dirpath, dirs=True):
            right_path = os.path.join(cur_dirpath, basename)
            left_obj = left_tree.follow_path(right_path)
            if left_obj is None or left_obj.is_excluded():
                if right_obj.is_file():
                    pr.print("right only: %s" % fstr2str(right_path))
                elif right_obj.is_dir():
                    pr.print("right only: %s" %
                             fstr2str(right_path+fstr(os.path.sep)))
                else:
                    raise RuntimeError(
                        "unexpected right object: " + fstr2str(right_path))
            elif right_obj.is_file():
                if not left_obj.is_file() and not left_obj.is_dir():
                    pr.print(
                        "left other vs right file: %s" % fstr2str(right_path))
            elif right_obj.is_dir():
                if not left_obj.is_file() and not left_obj.is_dir():
                    pr.print(
                        "left other vs right dir: %s" % fstr2str(right_path))
            else:
                raise RuntimeError(
                    "unexpected right object: " + fstr2str(right_path))
    with FileHashTree(**args.leftlocation.kws()) as left_tree:
        with FileHashTree(**args.rightlocation.kws()) as right_tree:
            if not args.hardlinks:
                FileHashTree.scan_trees_async([left_tree, right_tree])
            dirpaths_to_visit = [fstr("")]
            while dirpaths_to_visit:
                cur_dirpath = dirpaths_to_visit.pop()
                cmp_subdir(dirpaths_to_visit, cur_dirpath)


def do_check(args):
    def gen_all_paths(tree):
        for _obj, _parent, path in tree.walk_paths(
                files=True, dirs=False, recurse=True):
            yield path
    with FileHashTree(**args.location.kws()) as tree:
        assert tree.db.mode == ONLINE, "do_check tree not online"

        if not args.relpaths:
            num_items = tree.get_file_count()
            items_are_paths = False
            paths_gen = gen_all_paths(tree)
        else:
            num_items = len(args.relpaths)
            items_are_paths = True
            paths_gen = args.relpaths

        def print_report():
            """
            Print report and return final error status.
            """
            pr.print("%d distinct file(s) checked" % \
                     (len(file_objs_checked_ok) \
                      + len(file_objs_checked_bad),))
            if files_skipped > 0:
                pr.print("%d file(s) skipped due to no existing hash" %
                         (files_skipped,))
            if files_error > 0:
                pr.print("%d file(s) skipped due to file error" %
                         (files_error,))
            if file_objs_checked_bad:
                pr.print("%d file(s) failed" % (len(file_objs_checked_bad),))
                for fobj in file_objs_checked_bad:
                    pr.print(tree.printable_path(fobj.relpaths[0]))
                    if args.alllinks or args.hardlinks:
                        for other_path in fobj.relpaths[1:]:
                            prefix = "" if args.hardlinks else " "
                            pr.print(prefix, tree.printable_path(other_path))
                res = 1
            else:
                pr.info("no files failed check")
                res = 0
            return res

        def check_one_file(fobj, path):
            if tree.db_check_prop(fobj):
                pr.info(
                    "passed check: %s" % tree.printable_path(path))
                file_objs_checked_ok.add(fobj)
            else:
                pr.print(
                    "failed check: %s" % tree.printable_path(path))
                file_objs_checked_bad.add(fobj)

        file_objs_checked_ok = set()
        file_objs_checked_bad = set()
        try:
            index = 1
            files_skipped = 0
            files_error = 0
            for path in paths_gen:
                with pr.ProgressPrefix("%d/%d:" % (index, num_items)):
                    fobj = tree.follow_path(path)
                    if fobj in file_objs_checked_ok \
                       or fobj in file_objs_checked_bad:
                        if items_are_paths:
                            index += 1
                        continue
                    try:
                        check_one_file(fobj, path)
                    except PropDBException:
                        pr.warning("not checked: '%s'" % tree.printable_path(path))
                        files_skipped += 1
                        continue
                    except TreeError as exc:
                        pr.warning(
                            "while checking %s: %s" % \
                                (fstr2str(path), str(exc)))
                        files_error += 1
                        continue
                    index += 1
#        except KeyboardInterrupt:
#            _, v, tb = sys.exc_info()
#            pr.print("Interrupted... ")
#            raise
        finally:
            res = print_report()
    return res

def do_fdupes(args):
    """
    Find duplicate files, using file size as well as file hash.
    """
    grouper = \
        GroupedFileListPrinter(args.hardlinks, args.alllinks,
                               args.sameline, args.sort)
    with FileHashTree.listof(targ.kws() for targ in args.locations) \
            as all_trees:
        FileHashTree.scan_trees_async(all_trees)
        for file_sz in fdupes.sizes_repeated(all_trees, args.hardlinks):
            with pr.ProgressPrefix("size %s:" % (bytes2human(file_sz),)):
                for _hash, located_files in \
                    fdupes.located_files_repeated_of_size(
                            all_trees, file_sz, args.hardlinks):
                    grouper.add_group(located_files)
        grouper.flush()

def do_onall(args):
    if len(args.locations) == 1:
        return do_onfirstonly(args)
    grouper = \
        GroupedFileListPrinter(args.hardlinks, args.alllinks,
                               args.sameline, args.sort)
    treekws = [loc.kws() for loc in args.locations]
    with FileHashTree.listof(treekws) as all_trees:
        FileHashTree.scan_trees_async(all_trees)
        for file_sz in sorted(fdupes.sizes_onall(all_trees)):
            with pr.ProgressPrefix("size %s:" % (bytes2human(file_sz),)):
                for _hash, located_files in \
                        fdupes.located_files_onall_of_size(all_trees, file_sz):
                    grouper.add_group(located_files)
        grouper.flush()
    return None

def do_onfirstonly(args):
    grouper = \
        GroupedFileListPrinter(args.hardlinks, args.alllinks,
                               args.sameline, args.sort)
    with FileHashTree.listof(loc.kws() for loc in args.locations) as all_trees:
        FileHashTree.scan_trees_async(all_trees)
        first_tree = all_trees[0]
        other_trees = all_trees[1:]
        for file_sz in sorted(first_tree.get_all_sizes()):
            if not any(tr.size_to_files(file_sz) for tr in other_trees):
                for fobj in first_tree.size_to_files(file_sz):
                    grouper.add_group({first_tree: [fobj]})
                continue
            with pr.ProgressPrefix("size %s:" % (bytes2human(file_sz),)):
                for _hash, located_files in \
                        fdupes.located_files_onfirstonly_of_size(
                                all_trees, file_sz):
                    grouper.add_group(located_files)
        grouper.flush()

def do_onlastonly(args):
    locs = args.locations
    locs[0], locs[-1] = locs[-1], locs[0]
    do_onfirstonly(args)

def do_aliases(args):
    """
    Handler for printing all alias.
    """
    with FileHashTree(**args.location.kws()) as tree:
        tree.scan_subtree() # Must scan full tree to find all aliases.
        file_obj = tree.follow_path(args.relpath)
        file_path_printable = fstr2str(args.relpath)
        if file_obj is None:
            pr.error("path does not exist: %s" % (file_path_printable,))
        elif not file_obj.is_file():
            pr.error("not a file: %s" % (file_path_printable,))
        else:
            for path in file_obj.relpaths:
                pr.print(fstr2str(path))

def make_treekwargs(location, dbprefix=DEFAULT_DBPREFIX):
    """
    Create a treekwargs dictionary with root_path, dbmaker, dbkwargs.

    Used in the tests as as well as in do_subdir.
    """
    tree_arg = TreeLocationOnline(location)
    tree_arg.set_dbprefix(dbprefix)
    return tree_arg.kws()

def do_subdir(args):
    kwargs = args.topdir.kws()
    dbprefix = args.topdir.dbprefix
    src_dir = kwargs["root_path"]
    src_dbpath = kwargs["dbkwargs"]["dbpath"]
    tgt_dir = os.path.join(src_dir, args.relativesubdir)
    tgt_dbpath = os.path.join(tgt_dir, pick_db_basename(tgt_dir, dbprefix))
    top_idc = make_id_computer(src_dir)
    if not top_idc.subdir_invariant:
        msg = "no subdir command for file system = %s" % top_idc.file_sys
        raise NotImplementedError(msg)
    with SQLPropDBManager(src_dbpath, mode=ONLINE) as src_db:
        with SQLPropDBManager(tgt_dbpath, mode=ONLINE) as tgt_db:
            src_db.merge_prop_values(tgt_db)
    with FileHashTree(**make_treekwargs(tgt_dir, dbprefix)) \
            as tgt_tree:
        tgt_tree.db_purge_old_entries()
        tgt_tree.db.compact()

def do_mkoffline(args):
    """
    Create an offline db by updating an online tree, copying it to
    the provided output filename and inserting file tree directory
    structure and file metadata into the outputm, offline db.
    Overwrites any file at the output.
    """
    with FileHashTree(**args.sourcedir.kws()) as src_tree:
        src_tree.db_update_all()
        if args.forcewrite and os.path.isfile(args.outputpath):
            os.remove(args.outputpath)
        with SQLPropDBManager(args.outputpath, mode=OFFLINE) as tgt_db:
            with pr.ProgressPrefix("saving: "):
                src_tree.db_store_offline(tgt_db)
            tgt_db.compact()

def do_cleandb(args):
    """
    Purge old entries from db and compact it.
    """
    with FileHashTree(**args.location.kws()) as tree:
        pr.progress("removing offline data")
        tree.db.rm_offline_tree()
        pr.progress("purging old entries")
        tree.db_purge_old_entries()
        pr.progress("compacting database")
        tree.db.compact()
