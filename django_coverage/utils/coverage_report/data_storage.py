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

import time, os


class ModuleVars(object):
    modules = dict()

    def __new__(cls, module_name, module=None, coverage=None):
        # ModuleVars 是按照 module_name 唯一的
        if cls.modules.get(module_name, None):
            return cls.modules.get(module_name)
        else:
            obj = super(ModuleVars, cls).__new__(cls)
            obj._init(module_name, module, coverage)
            cls.modules[module_name] = obj
            return obj

    def _init(self, module_name, module, coverage):
        # 从coverage获取统计数据
        try:
            source_file, stmts, excluded, missed, missed_display = coverage.analysis2(module)
        except Exception as e:
            # no source file - skip (*.pyc for example)
            self.total_count = 0
            return

        executed = list(set(stmts).difference(missed))
        total = list(set(stmts).union(excluded))
        total.sort()

        title = module.__name__
        total_count = len(total)
        executed_count = len(executed)
        excluded_count = len(excluded)
        missed_count = len(missed)
        try:
            percent_covered = float(len(executed)) / len(stmts) * 100
        except ZeroDivisionError:
            percent_covered = 100
        test_timestamp = time.strftime('%a %Y-%m-%d %H:%M %Z')

        severity = 'normal'
        if percent_covered < 75: severity = 'warning'
        if percent_covered < 50: severity = 'critical'

        # 将当前的局部变量设置到ModuleVars中
        for k, v in locals().iteritems():
            setattr(self, k, v)

    def get_module_path(self):
        return self.module_name.replace(".", "/") + ".py"

    def get_module_dir(self):
        return self.source_file[:-len(self.get_module_path())]


class TemplateVars(object):
    modules = dict()

    def __new__(cls, module_name, module=None, coverage=None):
        if cls.modules.get(module_name, None):
            return cls.modules.get(module_name)
        else:
            obj = super(TemplateVars, cls).__new__(cls)
            obj._init(module_name, module, coverage)
            cls.modules[module_name] = obj
            return obj

    def _init(self, module_name, module, coverage):
        plugin = coverage.plugins.get('django_coverage_plugin.DjangoTemplatePlugin')
        if plugin:
            fr = plugin.file_reporter(module.__path__)
            try:
                analysis = coverage._analyze(fr)
            except Exception as e:
                print '-- problem with file %s --' % module.__path__
                print e
                # skip this file
                self.total_count = 0
                return

            source_file, stmts, excluded, missed, missed_display = (
                analysis.filename, sorted(analysis.statements),
                sorted(analysis.excluded), sorted(analysis.missing),
                analysis.missing_formatted(),
            )

            executed = list(set(stmts).difference(missed))
            total = list(set(stmts).union(excluded))
            total.sort()

            title = os.path.basename(module_name)
            total_count = len(total)
            executed_count = len(executed)
            excluded_count = len(excluded)
            missed_count = len(missed)
            try:
                percent_covered = float(len(executed)) / len(stmts) * 100
            except ZeroDivisionError:
                percent_covered = 100
            test_timestamp = time.strftime('%a %Y-%m-%d %H:%M %Z')

            severity = 'normal'
            if percent_covered < 75: severity = 'warning'
            if percent_covered < 50: severity = 'critical'

            # 将当前的局部变量设置到ModuleVars中
            for k, v in locals().iteritems():
                setattr(self, k, v)
            return

    def get_module_path(self):
        paths = self.source_file.split('/')
        filename = paths[-1]

        mod_paths = self.module_name[:-len(filename)].replace('.', '/').split('/')
        if mod_paths[-1] == '':
            mod_paths = mod_paths[:-1]

        paths = paths[:-1]
        for i in range(0, len(paths)):
            if paths[i:] == mod_paths:
                break
        paths = paths[i:]
        paths.append(filename)
        return os.path.join(*paths)

    def get_module_dir(self):
        return self.source_file[:-len(self.get_module_path())]


def get_vars_class(mod):
    if hasattr(mod, 'is_template_module') and mod.is_template_module:
        return TemplateVars
    else:
        return ModuleVars
