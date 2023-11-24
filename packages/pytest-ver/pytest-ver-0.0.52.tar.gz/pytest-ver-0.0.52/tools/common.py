import json
import os
from pathlib import Path

# the module name (with dashes)
# note: set the name in set_common_names.sh
cmn_mod_name = 'unset_cmn_mod_name'

# the local directory name for the module (with underscores)
# note: set the name in set_common_names.sh
cmn_mod_dir_name = 'unset_cmn_mod_dir_name'

# the license for the module
cmn_license = 'MIT'

# the license string for the classifier section
cmn_classifier_license = 'License :: OSI Approved :: MIT License'

# the url for the homepage link
cmn_homepage_url = f'https://bitbucket.org/arrizza-public/{cmn_mod_name}/src/master'
# the url for the download link
cmn_download_url = f'https://bitbucket.org/arrizza-public/{cmn_mod_name}/get/master.zip'

# the author name
cmn_author = 'JA'

# the contact email
cmn_email = 'cppgent0@gmail.com'

# the version string held in cmn_mod_dir_name/lib/version.json
cmn_version = 'unknown'
# the long version of the version string
cmn_long_version = 'unknown'
# the long description of the module (usually content of README)
cmn_long_desc = 'unknown'
# the format of the long desc (usually markdown)
cmn_long_desc_type = 'unknown'


# --------------------
## get the version string from the module's version.json file
# get the long desc i.e. the README.md content
#
#  note: must not use Constants here; causes the install/setup to fail
#
# @return the version string and the long version of it
def init():
    global cmn_version
    global cmn_long_version
    global cmn_long_desc
    global cmn_long_desc_type
    global cmn_mod_name
    global cmn_mod_dir_name

    import subprocess

    out = subprocess.check_output('tools/set_common_names.sh report', shell=True)
    names = out.decode().strip().split(':')
    cmn_mod_name = names[0]
    cmn_mod_dir_name = names[1]
    # uncomment to debug
    # print(f'DBG cmn_mod_name    : {cmn_mod_name}')
    # print(f'DBG cmn_mod_dir_name: {cmn_mod_dir_name}')

    root_dir = Path('..').parent
    cmn_version = None
    path = os.path.join(root_dir, cmn_mod_dir_name, 'lib', 'version.json')
    with open(path, 'r', encoding='utf-8') as fp:
        j = json.load(fp)
        cmn_version = j['version']

    cmn_long_version = cmn_version.replace('.', '_')

    cmn_long_desc = (root_dir / 'README.md').read_text()
    cmn_long_desc_type = 'text/markdown'
