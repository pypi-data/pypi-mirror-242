import configparser
import glob
import os
import platform
import re
import sys

import common
from debug_logger import DebugLogger as logger


# --------------------
## holds functions to check all installation and environment
# Do not use any non-built in modules
# Do not use out/ directory
class App:
    # --------------------
    ## constructor
    def __init__(self):
        ## the name of the OS
        self._osname = 'unknown'

        ## holds additional scripts to check for permissions
        self._scripts = [
            os.path.join('tools/set_common_names.sh')
        ]

    # --------------------
    ## run the check
    #
    # @return None
    def run(self):
        self._check_ostype()
        self._check_python_version()
        self._check_pypi()
        self._check_bash_scripts()
        self._check_common()

        # TODO check doxygen version >= 1.9.1; cross-platform?

    # --------------------
    ## check the OS name and platform are recognized
    #
    # @return None
    def _check_ostype(self):
        self._osname = platform.system()
        logger.line(f'osname  : {self._osname}')
        # Linux: Linux
        # Mac: Darwin
        # Windows: Windows

        logger.line(f'platform: {sys.platform}')
        # Linux: linux (lower case)
        # Mac: ??
        # Win MSYS2: msys (need to confirm)
        # Win MING : mingw64
        # WIN WSL  : linux2

    # --------------------
    ## check the python version
    #
    # @return True if a valid version, False otherwise
    def _check_python_version(self):
        logger.start(f'python version:')
        logger.line(f'   version : {sys.version}')
        logger.line(f'   info    : {sys.version_info}')

        ok = True
        if sys.version_info.major != 3:
            ok = False
            logger.log(ok, f'python must be v3')
        elif sys.version_info.minor < 9:
            ok = False
            logger.log(ok, f'python must be v3.9 or higher')
        return ok

    # --------------------
    ## check for the existence of $HOME/.pypirc and it's content
    #
    # @return None
    def _check_pypi(self):
        home = os.path.expanduser('~')
        path = os.path.join(home, '.pypirc')
        exists = os.path.isfile(path)

        msg = f'{".pypirc exists": <15}: {exists}'
        logger.log(exists, msg)

        if exists:
            self._check_pypi_content(path)

    # --------------------
    ## check the content of the .pypirc file
    #
    # @param path the path to the file
    # @return None
    def _check_pypi_content(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        msg = ''
        ok = 'pypi' in config.sections()
        if not ok:
            msg += 'missing "pypi" section'
            logger.log(ok, msg)
            return

        msgs = []
        # check username
        if 'username' not in config['pypi']:
            msgs.append('missing pypi.username')
            ok = False
        elif config['pypi']['username'] != '__token__':
            msgs.append('pypi.username should be "__token__"')
            ok = False

        # check password
        if 'password' not in config['pypi']:
            msgs.append('missing pypi.password')
            ok = False

        logger.log_all(ok, f'{".pypirc content": <15}', msgs)

    # --------------------
    ## check permissions on the executable scripts
    #  * all scripts that start with do_*
    #  * any given in self._scripts
    #
    # @return None
    def _check_bash_scripts(self):
        scripts = glob.glob('do*')
        self._scripts.extend(scripts)
        ok = True
        for path in self._scripts:
            if not os.path.isfile(path):
                continue
            ok = ok and self._check_script(path)
        if ok:
            msg = f'execute permissions'
            logger.ok(msg)

    # --------------------
    ## checks the permissions for the given script
    #
    # @param path   the script to check
    # @return None
    def _check_script(self, path):
        ok = os.access(path, os.X_OK)
        if not ok:
            msg = f'execute permission missing: {path}'
            logger.err(msg)
        return ok

    # --------------------
    ## check values against common.py content
    #
    # @return None
    def _check_common(self):
        common.init()
        self._check_mod_names()
        self._check_manifest()
        self._check_doxyfile()

    # --------------------
    ## check module names
    #
    # @return None
    def _check_mod_names(self):
        if common.cmn_mod_name == '':
            logger.err('cmd_mod_name in tools/set_common_names.sh not set')
        elif '-' not in common.cmn_mod_name and '_' in common.cmn_mod_name:
            logger.err(f'cmd_mod_name should contain "-", not "_": {common.cmn_mod_name}')
        else:
            logger.ok(f'{"cmn_mod_name": <18}: {common.cmn_mod_name}')

        if common.cmn_mod_dir_name == '':
            logger.err('cmn_mod_dir_name in tools/set_common_names.sh not set')
        elif '_' not in common.cmn_mod_dir_name and '-' in common.cmn_mod_dir_name:
            logger.err(f'cmn_mod_dir_name should contain "_", not "-": {common.cmn_mod_dir_name}')
        else:
            logger.ok(f'{"cmn_mod_dir_name": <18}: {common.cmn_mod_dir_name}')

    # --------------------
    ## check manifest.in file
    #
    # @return None
    def _check_manifest(self):
        fname = 'MANIFEST.in'
        with open(fname, 'r') as fp:
            line1 = fp.readline().strip()

            ok = True
            if line1 != f'graft {common.cmn_mod_dir_name}':
                ok = False
                logger.err(f'{fname}: line1 is incorrect: {line1}')

            if ok:
                logger.ok(f'{fname}')

    # --------------------
    ## check Doxyfile
    #
    # @return None
    def _check_doxyfile(self):
        tag = 'Doxyfile'
        fname = os.path.join('tools', 'Doxyfile')

        found_version = False
        found_name = False
        found_exclude = False
        ok = True
        with open(fname, 'r') as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                line = line.strip()

                # PROJECT_NAME = "gui-api-tkinter Module"
                m = re.search(r'PROJECT_NAME\s*=\s*(".+")$', line)
                if m:
                    found_name = True
                    if m.group(1) != f'"{common.cmn_mod_name} Module"':
                        logger.err(f'{tag}: "PROJECT_NAME" {m.group(1)} '
                                   f'does not match "{common.cmn_mod_name} Module"')
                        ok = False

                # e.g PROJECT_NUMBER = 0.0.1
                m = re.search(r'PROJECT_NUMBER\s*=\s*([0-9.]+)', line)
                if m:
                    found_version = True
                    if m.group(1) != common.cmn_version:
                        logger.err(f'{tag}: "PROJECT_NUMBER" version {m.group(1)} '
                                   f'does not match version.json: {common.cmn_version}')
                        ok = False

                # EXCLUDE += ./gui_api_tkinter/lib/build_info.py
                m = re.search(r'EXCLUDE\s*\+=\s*(.+)/lib/build_info\.py', line)
                if m:
                    found_exclude = True
                    if m.group(1) != f'./{common.cmn_mod_dir_name}':
                        logger.err(f'{tag}: "EXCLUDE" {m.group(1)} '
                                   f'does not match expected: ./{common.cmn_mod_dir_name}/lib/build_info.py')
                        ok = False

        if not found_version:
            logger.err(f'{tag}: "PROJECT_NUMBER" line not found')
            ok = False

        if not found_name:
            logger.err(f'{tag}: "PROJECT_NAME" line not found')
            ok = False

        if not found_exclude:
            # even if the module doesn't use build_info, Doxyfile can exclude it
            logger.err(f'{tag}: "EXCLUDE" build_info line not found')
            ok = False

        if ok:
            logger.ok(f'{tag}')


# --------------------
def main():
    app = App()
    app.run()


main()
