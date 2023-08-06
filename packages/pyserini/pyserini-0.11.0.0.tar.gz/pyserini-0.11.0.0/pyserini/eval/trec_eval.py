import os
import subprocess
import sys

from pyserini.search import get_qrels_file
from pyserini.util import download_evaluation_script

script_path = download_evaluation_script('trec_eval')
cmd_prefix = ['java', '-jar', script_path]
args = sys.argv
if len(args) > 1:
    cmd = cmd_prefix + args[1:]
    if not os.path.exists(cmd[-2]):
        cmd[-2] = get_qrels_file(cmd[-2])
else:
    cmd = cmd_prefix
print(f'Running command: {cmd}')
process = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
if stderr:
    print(stderr.decode("utf-8"))
else:
    print('Results:')
    print(stdout.decode("utf-8"))
