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
import os
import sys

import django

if django.VERSION < (1, 2):
    msg = """

    django-coverage 1.1+ requires django 1.2+.
    Please use django-coverage 1.0.3 if you have django 1.1 or django 1.0
    """
    raise Exception(msg)

from django.conf import global_settings
from django.test.utils import get_runner

from coverage import Coverage

from django_coverage import settings
from django_coverage.utils.coverage_report import html_report
from django_coverage.utils.module_tools import get_all_modules


DjangoTestSuiteRunner = get_runner(global_settings)

def get_app(app_label):
    try:
        # django >= 1.7
        from django.apps import apps
        return apps.get_app_config(app_label).models_module
    except ImportError:
        from django.db import models
        return models.get_app(app_label)


def get_apps():
    try:
        # django >= 1.7, to support AppConfig
        from django.apps import apps
        return [app.models_module for app in apps.get_app_configs() if app.models_module]
    except ImportError:
        from django.db import models
        return models.get_apps()



class CoverageRunner(DjangoTestSuiteRunner):
    """
        跑Coverage时默认使用的TestSuiteRunner
        Test runner which displays a code coverage report at the end of the run.
    """

    def __new__(cls, *args, **kwargs):
        """
        Add the original test runner to the front of CoverageRunner's bases,
        so that CoverageRunner will inherit from it. This allows it to work
        with customized test runners.
        """
        # If the test runner was changed by the management command, change it
        # back to its original value in order to get the original runner.
        if getattr(settings, 'ORIG_TEST_RUNNER', None):
            settings.TEST_RUNNER = settings.ORIG_TEST_RUNNER
            TestRunner = get_runner(settings)
            if (TestRunner != DjangoTestSuiteRunner):
                cls.__bases__ = (TestRunner,) + cls.__bases__
        return super(CoverageRunner, cls).__new__(cls)

    def _get_app_package(self, app_model_module):
        """
        Returns the app module name from the app model module.
        """
        return '.'.join(app_model_module.__name__.split('.')[:-1])

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        # 1. 设置coverage
        opts = {
            'auto_data': settings.COVERAGE_USE_CACHE,
        }
        if settings.COVERAGE_SOURCE:
            opts['source'] = settings.COVERAGE_SOURCE
        if settings.COVERAGE_CONFIG_FILE:
            opts['config_file'] = settings.COVERAGE_CONFIG_FILE
        coverage = Coverage(**opts)
        for e in settings.COVERAGE_CODE_EXCLUDES:
            coverage.exclude(e)
        coverage.start()
        results = super(CoverageRunner, self).run_tests(test_labels,
                                                        extra_tests, **kwargs)
        coverage.stop()

        # 2. 添加coverage_modules
        coverage_modules = []
        if test_labels:
            for label in test_labels:
                label = label.split('.')[0].rstrip('/')
                app = get_app(label)
                coverage_modules.append(self._get_app_package(app))
        else:
            for app in get_apps():
                coverage_modules.append(self._get_app_package(app))

        coverage_modules.extend(settings.COVERAGE_ADDITIONAL_MODULES)

        # 加载所有的packages, modules等
        packages, modules, excludes, errors = get_all_modules(coverage_modules, settings.COVERAGE_MODULE_EXCLUDES, settings.COVERAGE_PATH_EXCLUDES)

        if settings.COVERAGE_USE_STDOUT:
            coverage.report(modules.values(), show_missing=1)
            if excludes:
                message = "The following packages or modules were excluded:"
                print("")
                print(message)
                for e in excludes:
                    print(e)
                print("")
            if errors:
                message = "There were problems with the following packages "
                message += "or modules:"
                print("")
                print(message)
                for e in errors:
                    print(e)
                print("")

        # 输出Html格式的数据
        # modules: module_name --> module
        #
        outdir = settings.COVERAGE_REPORT_HTML_OUTPUT_DIR
        if outdir:
            outdir = os.path.abspath(outdir)
            # 默认使用55minutes的html表
            if settings.COVERAGE_CUSTOM_REPORTS:
                html_report(coverage, outdir, modules, excludes, errors)
            else:
                coverage.html_report(modules.values(), outdir)
            print("")
            print("HTML reports were output to '%s'" %outdir)

        return results
