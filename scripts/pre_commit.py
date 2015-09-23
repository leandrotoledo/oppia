# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pre commit hook tests"""

__author__ = 'leandrotoledo@google.com'

import os
import sys

import common

# Root path of the app.
ROOT_PATH = os.getcwd()

THIRD_PARTY_LIBS = [
    os.path.join(ROOT_PATH, 'third_party', 'astroid-1.3.8'),
    os.path.join(ROOT_PATH, 'third_party', 'six-1.9.0'),
    os.path.join(ROOT_PATH, 'third_party', 'logilab-common-1.0.2'),
    os.path.join(ROOT_PATH, 'third_party', 'pylint-1.4.4'),
]

for lib_path in THIRD_PARTY_LIBS:
    if not os.path.isdir(lib_path):
        raise Exception('Invalid path for third_party library: %s' % lib_path)
    sys.path.insert(0, lib_path)


def _is_python_file(filename):
    """Checks if file is a python file based on its extension."""
    try:
        filename_extension = os.path.splitext(filename)[1]

        if not filename_extension.lower() == '.py':
            return False
    except IndexError:
        return False

    return True


def _get_current_commit():
    """Uses git to get the current commit from the repository."""
    GET_SHA1_EMPTY_TREE = '4b825dc642cb6eb9a060e54bf8d69288fbee4904'
    GIT_REV_PARSE_CMD = 'git rev-parse --verify HEAD'.split()
    
    if not common.run_shell_cmd(GIT_REV_PARSE_CMD):
        return GET_SHA1_EMPTY_TREE

    return 'HEAD'


def _get_list_of_committed_files():
    """Uses git to get a list of all commited files on current commit."""
    GIT_DIFF_INDEX_CMD = ('git diff --cached --name-only %s' % 
        _get_current_commit())
    GIT_DIFF_INDEX_CMD = GIT_DIFF_INDEX_CMD.split()

    commited_files_list = []

    result = common.run_shell_cmd(GIT_DIFF_INDEX_CMD)
    for commited_file in result.split('\n'):
        if commited_file:
            commited_files_list.append(commited_file)

    return commited_files_list


class CommitHookPyLint(object):
    """Executes pylint tests given a list of python files or directories."""

    PYLINT_OPTIONS = [
        '--rcfile=%s/.pylintrc' % ROOT_PATH,
    ]

    def __init__(self, test_targets):
        self.test_targets = test_targets

    def run(self):
        """Runs all tests corresponding to the given test target."""
        from pylint.lint import Run

        test_targets_flag = self.PYLINT_OPTIONS
        test_targets_flag.extend(self.test_targets)

        return Run(test_targets_flag)


def main():
    commited_files = _get_list_of_committed_files()

    py_commited_files = []
    for commited_file in commited_files:
        if _is_python_file(commited_file):
            py_commited_files.append(commited_file)

    if py_commited_files:
        pylint = CommitHookPyLint(py_commited_files)
        result = pylint.run()


if __name__ == '__main__':
    main()