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
from django.utils.translation import ugettext as _
from django_coverage import settings

TOP = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-type" content="text/html;charset=UTF-8" />
    <title>Test coverage report</title>
    <style type="text/css" media="screen">
      a {
        color: #3d707a;
      }
      a:hover, a:active {
        color: #bf7d18;
      }
    
      body {
        font-family: "Lucida Sans Unicode", "Lucida Grande", sans-serif;
        font-size: 13px;
      }

      .nav
      {
        font-size: 12px;
        margin-left: 50px;
      }

      tr:hover {
        background: #f5f5f5;
      }
      
      #content-header {
        margin-left: 50px;
      }

      #content-header h1 {
        font-size: 18px;
        margin-bottom: 0;
      }

      #content-header p {
        font-size: 13px;
        margin: 0;
        color: #909090;
      }
      
      #result-list table {
        font-size: 13px;
        background: white;
        margin: 15px 50px;
        width: 1000px;
        border-collapse: collapse;
        text-align: right;
      }

      #result-list thead tr.last th,
      th.statements
      {
        border-bottom: 1px solid #6d5e48;
      }
      
      th.statements
      {
        text-align: center;
      }

      #result-list th
      {
        padding: 3px 12px;
        font-size: 14px;
        font-weight: normal;
        color: #937F61;
      }

      #result-list td
      {
        border-bottom: 1px solid #e0e0e0;
        color: #606060;
        padding: 6px 12px;
      }
      
      #result-list tfoot td
      {
        color: #937F61;
        font-weight: bold;
      }

      #result-list .normal
      {
        color: #609030;
      }

      #result-list .warning
      {
        color: #d0a000;
      }

      #result-list .critical
      {
        color: red;
      }

      #result-list .module-name
      {
        text-align: left;
      }
      
      .footer-link
      {
        margin-left: 62px;
      }
   </style>
  </head>

  <body>
"""

CONTENT_HEADER = """\
<div id="content-header">
  <h1>""" + _('Test Coverage Report') + """</h1>
  <p>""" + _('Generated') + """: %(test_timestamp)s</p>
  <p><img src="coverage_status.png"></p>
"""
if settings.COVERAGE_PROCESS_AUTHORS:
    CONTENT_HEADER += '  <p><a target=_blank href="auth_index.html">' + _('Authors') + '</a></p>'
CONTENT_HEADER += '</div>'


CONTENT_HEADER_AUTHOR = """\
<div id="content-header">
  <h1>""" + _('Test Coverage Report') + """: %(author)s</h1>
  <p>""" + _('Generated') + """: %(test_timestamp)s</p>
</div>
"""

#
# thead, tfoot是语义标签，和出现的位置无关; tfoot即便放在前面，最终展示的时候也是在table的底部
#
CONTENT_BODY = """\
<div id="result-list">
  <table class="sortable">
    <thead>
      <tr class="last">
        <th class="module-name">""" + _('Module') + """</th>
        <th>""" + _('total') + """</th>
        <th>""" + _('executed') + """</th>
        <th>""" + _('excluded') + """</th>
        <th>""" + _('%% covered') + """</th>
      </tr>
    </thead>
    <tfoot>
      <tr>
        <td class="module-name">""" + _('Total') + """</td>
        <td><span style='color:#ff00ff;'>""" + _('Tolal lines') + """: %(total_lines)d</span></td>
        <td>%(total_executed)d</td>
        <td>%(total_excluded)d</td>
        <td><span style='color:#ff00ff;'>""" + _('Overall covered') + """: %(overall_covered)0.1f%%</span></td>
      </tr>
    </tfoot>
    <tbody>
      %(module_stats)s
    </tbody>
  </table>
</div>
"""

# 每一行统计的结果
MODULE_STAT = """\
<tr>
  <td class="module-name"><a href="%(module_link)s">%(module_name)s</a></td>
  <td>%(total_count)d</td>
  <td>%(executed_count)d</td>
  <td>%(excluded_count)d</td>
  <td class="%(severity)s">%(percent_covered)0.1f%%</td>
</tr>
"""

EXCEPTIONS_LINK = """\
<div>
  <a class="footer-link" href="%(exceptions_link)s">
    %(exception_desc)s
  </a>
</div>
"""

BOTTOM = """\
  <script src="sorttable.js"></script>
  </body>
</html>
"""
BOTTOM_AUTH = """\
  <script src="../sorttable.js"></script>
  </body>
</html>
"""


NAV = """\
<div class="nav">
  <a href="%(prev_link)s">%(prev_label)s</a> &lt;&lt;
  <a href="%(up_link)s">%(up_label)s</a>
  &gt;&gt; <a href="%(next_link)s">%(next_label)s</a>
</div>
"""

NAV_NO_PREV = """\
<div class="nav">
  <a href="%(up_link)s">%(up_label)s</a>
  &gt;&gt; <a href="%(next_link)s">%(next_label)s</a>
</div>
"""

NAV_NO_NEXT = """\
<div class="nav">
  <a href="%(prev_link)s">%(prev_label)s</a> &lt;&lt;
  <a href="%(up_link)s">%(up_label)s</a>
</div>
"""
NAV_NO = """\
<div class="nav">
  <a href="%(up_link)s">%(up_label)s</a>
</div>
"""