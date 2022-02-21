import os
import signal
import subprocess
import sys
from dev_deploy_def import deploy_vars

RUN_DIRECTORY = "_temp_run_local"
LIB_DIRECTORY = "deps"
DEF_FILE = "local_run_def.py"


def main():
    cloud_function_name = sys.argv[1]

    subprocess.call("rm -r {}".format(RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("mkdir {}".format(RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp -a {}/. {}".format(cloud_function_name, RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp -a {} {}".format(LIB_DIRECTORY, RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp {} {}".format(DEF_FILE, RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/{}".format(RUN_DIRECTORY))

    proc = subprocess.Popen("functions_framework --target={} --signature-type=http".format(cloud_function_name), shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        print(line)


if __name__ == "__main__":
    try:
        main()
    finally:
        os.killpg(0, signal.SIGKILL)
