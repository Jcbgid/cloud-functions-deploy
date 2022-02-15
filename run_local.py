import os
import signal
import subprocess
import sys
from dev_deploy_def import dev_deploy_vars

RUN_DIRECTORY = "_temp_run_local"
LIB_DIRECTORY = ""


def main():
    cloud_function_name = sys.argv[1]

    subprocess.call("rm -r {}".format(RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("mkdir {}".format(RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp -a {}/. {}".format(cloud_function_name, RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp -a {} {}".format(LIB_DIRECTORY, RUN_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/{}".format(RUN_DIRECTORY))

    for k,v in dev_deploy_vars.items():
        subprocess.call("export '{}={}'".format(k, v), shell=True, stdout=subprocess.PIPE)

    # This is causing problems.s
    # proc = subprocess.Popen("functions_framework --target={} --signature-type=http".format(cloud_function_name), shell=True, stdout=subprocess.PIPE)
    # for line in proc.stdout:
    #     print(line)

    print("functions_framework --target={} --signature-type=http".format(cloud_function_name))

if __name__ == "__main__":
    # try:
    main()
    # finally:
    #     os.killpg(0, signal.SIGKILL)
