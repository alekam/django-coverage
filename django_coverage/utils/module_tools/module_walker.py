# -*- encoding: utf-8 -*-
"""
Copyright 2009 55 Minutes (http://www.55minutes.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os, re
from glob import glob

from django_coverage.utils.module_tools.data_storage import *
from django_coverage.utils.module_tools.module_loader import find_or_load_module

try:
    set
except:
    from sets import Set as set

__all__ = ('get_all_modules',)

def _build_pkg_path(pkg_name, pkg, path):
    for rp in [x for x in pkg.__path__ if path.startswith(x)]:
        p = path.replace(rp, '').replace(os.path.sep, '.')
        return pkg_name + p

def _build_module_path(pkg_name, pkg, path):
    return _build_pkg_path(pkg_name, pkg, os.path.splitext(path)[0])

def _prune_whitelist(whitelist, blacklist):
    """
    将whitelist中属于blacklist的东西过滤掉
    :param whitelist:
    :param blacklist:
    :return:
    """
    excluded = Excluded().excluded

    # 如果white_list中包含 blacklist指定的pattern, 则将它们移除，添加到excluded中
    for wp in whitelist[:]:
        for bp in blacklist:
            if re.search(bp, wp):
                whitelist.remove(wp)
                excluded.append(wp)
                break
    return whitelist

def _parse_module_list(m_list):
    packages = Packages().packages
    modules = Modules().modules
    excluded = Excluded().excluded
    errors = Errors().errors

    for m in m_list:
        components = m.split('.')
        m_name = ''
        search_path = []
        processed=False
        for i, c in enumerate(components):
            m_name = '.'.join([x for x in m_name.split('.') if x] + [c])
            try:
                module = find_or_load_module(m_name, search_path or None)
            except ImportError:
                processed=True
                errors.append(m)
                break
            try:
                search_path.extend(module.__path__)
            except AttributeError:
                processed = True
                if i+1==len(components):
                    modules[m_name] = module
                else:
                    errors.append(m)
                    break

        # 记录成功导入的package
        if not processed:
            packages[m_name] = module

def prune_dirs(root, dirs, exclude_dirs):
    regexes = [re.compile(exclude_dir) for exclude_dir in exclude_dirs] # 重复操作
    for path, dir_ in [(os.path.join(root, dir_), dir_) for dir_ in dirs]:
        for regex in regexes:
            if regex.search(path):
                dirs.remove(dir_)
                break

def _get_all_packages(pkg_name, pkg, blacklist, exclude_dirs):
    packages = Packages().packages
    errors = Errors().errors

    for path in pkg.__path__:

        # 遍历pkg下的所有的dirs
        for root, dirs, files in os.walk(path):
            # 将dirs下的部分目录过滤
            prune_dirs(root, dirs, exclude_dirs or [])

            m_name = _build_pkg_path(pkg_name, pkg, root)
            try:
                # 如果m_name有效，则将m添加到packages中
                if _prune_whitelist([m_name], blacklist):
                    m = find_or_load_module(m_name, [os.path.split(root)[0]])
                    packages[m_name] = m
                else:
                    for d in dirs[:]:
                        dirs.remove(d)
            except ImportError:
                errors.append(m_name)
                for d in dirs[:]:
                    dirs.remove(d)

def _get_all_modules(pkg_name, pkg, blacklist):
    modules = Modules().modules
    errors = Errors().errors

    for p in pkg.__path__:
        for f in glob('%s/*.py' %p):
            m_name = _build_module_path(pkg_name, pkg, f)
            try:
                if _prune_whitelist([m_name], blacklist):
                    m = find_or_load_module(m_name, [p])
                    modules[m_name] = m
            except ImportError:
               errors.append(m_name)

def get_all_modules(whitelist, blacklist=None, exclude_dirs=None):
    """
    给定了whitelist
    :param whitelist: 为各个app的package, 例如: api, django.contrib.auth
    :param blacklist:
    :param exclude_dirs:
    :return:
    """
    packages = Packages().packages
    modules = Modules().modules
    excluded = Excluded().excluded
    errors = Errors().errors

    whitelist = _prune_whitelist(whitelist, blacklist or [])

    # 将str ---> module
    _parse_module_list(whitelist)

    for pkg_name, pkg in packages.copy().items(): # 在iterator中将packages做一个copy
        _get_all_packages(pkg_name, pkg, blacklist, exclude_dirs)

    for pkg_name, pkg in packages.copy().items():
        _get_all_modules(pkg_name, pkg, blacklist)

    return packages, modules, list(set(excluded)), list(set(errors))
