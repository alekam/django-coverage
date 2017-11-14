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
__all__ = ('Packages', 'Modules', 'Excluded', 'Errors', 'TemplateModule', 'Templates')


class SingletonType(type):
    # 1. 所有的 SingletonType 的实例，都具有__call__, 同时也是构造函数
    #    Packages()等返回的对象都是唯一的
    def __call__(cls, *args, **kwargs):
        if getattr(cls, '__instance__', None) is None:
            instance = cls.__new__(cls)
            instance.__init__(*args, **kwargs)
            cls.__instance__ = instance
        return cls.__instance__


# 单例如何使用呢?
# Packages().packages
# 1. 所有的 SingletonType 的实例，都具有__call__, 同时也是构造函数
class Packages(object):
    __metaclass__ = SingletonType
    packages = {}


class Modules(object):
    __metaclass__ = SingletonType
    modules = {}


class Excluded(object):
    __metaclass__ = SingletonType
    excluded = []


class Errors(object):
    __metaclass__ = SingletonType
    errors = []


class AuthorModule(object):
    module_link = ""
    executed = 0
    missed = 0
    excluded = 0


class Authors(object):
    __metaclass__ = SingletonType
    """
        数据结构:

        author <---> modules
                     module <----> module/coverage/
    """
    author_2_modules = {}
    author_2_url = {}


    def get_author_summary(self, author):
        """
        获取指定author的代码的覆盖情况(以可执行的代码为准)
        :param author:
        :return:
        """
        if author in self.author_2_modules:
            modules = self.author_2_modules[author]
            executed, missed, excluded = 0, 0, 0
            for module, author_module in modules.items():
                executed += author_module.executed
                missed += author_module.missed
                excluded += author_module.excluded
            total = executed + missed
            if total == 0:
                return executed, missed, excluded, total, 100.0
            else:
                return executed, missed, excluded, total, (executed * 100.0 / total)

        else:
            return None

    def add_auth_coverage(self, author, m_vars, executed, missed, excluded):
        """
        调整统计数据
        :param author:
        :param mod:
        :param executed:
        :param missed:
        :param excluded:
        :return:
        """
        if not author:
            return

        modules = self.author_2_modules.get(author)
        if modules is None:
            modules = {}
            self.author_2_modules[author] = modules

        module_name = m_vars.module_name

        module_info = modules.get(module_name)
        if module_info is None:
            module_link = m_vars.module_link

            # 初始化
            module_info = AuthorModule()
            module_info.module_link = module_link

            modules[module_name] = module_info

        module_info.executed += executed
        module_info.missed += missed
        module_info.excluded += excluded


class Templates(object):
    __metaclass__ = SingletonType
    templates = {}


class TemplateModule(object):
    """
    Fake module
    """
    is_template_module = True

    def __init__(self, name, path):
        self.path = path
        self.__path__ = path
        self.name = name
        self.__name__ = name
        self.module_name = name
