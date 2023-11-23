import argparse
import pathlib
import sys

from tools.debug_logger import DebugLogger as logger
from tools.publish.gen_build_info import GenBuildInfo

# --------------------
## generate the build information file
parser = argparse.ArgumentParser()
parser.add_argument('path', type=pathlib.Path)
parser.add_argument('--no_log', dest='log', action='store_false', default=True)
args = parser.parse_args()

binfo = GenBuildInfo()
binfo.init(args.path, args.log)
rc = binfo.gen()
binfo.term()

if rc != 0:
    logger.err(f'GenBuildInfo failed with rc={rc}, exiting')
    sys.exit(rc)
