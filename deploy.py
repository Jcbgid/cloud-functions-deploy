import os
import subprocess
import sys

from dev_deploy_def import deploy_vars as dev_deploy_vars, deploy_spec as dev_deploy_spec, GCLOUD_UTIL_CONFIG

DEPLOY_DIRECTORY = "_temp_cf_deploy"
LIB_DIRECTORY = "deps"

"""

This script should live in the same directory as the cloud function directory and library director
* The lib and deploy temp directory are defined above

* first arg = cloud function name
* second arg = dev or prod

The gcloud config will be set automatically for deploy

"""


def main():
    dep_env = sys.argv[2]
    cloud_function_name = sys.argv[1]

    if dep_env == "dev":
        env_vars = dev_deploy_vars
        deploy_spec = dev_deploy_spec
        gcloud_util_config = DEV_GCLOUD_UTIL_CONFIG
    else:
        raise Exception

    subprocess.call("rm -r {}".format(DEPLOY_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("mkdir {}".format(DEPLOY_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp -a {}/. {}".format(cloud_function_name, DEPLOY_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp -a {} {}".format(LIB_DIRECTORY, DEPLOY_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    subprocess.call("cp -a {} {}".format("requirements.txt", DEPLOY_DIRECTORY), shell=True, stdout=subprocess.PIPE)

    os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/{}".format(DEPLOY_DIRECTORY))

    allow_unauthenticated_clause = "--allow-unauthenticated" if deploy_spec[cloud_function_name][
        'allow_unauthenticated'] else ""

    env_vars_clause = "--set-env-vars "
    for k, v in env_vars.items():
        env_vars_clause += "{}={},".format(k, v)

    subprocess.call("gcloud config configurations activate {}".format(gcloud_util_config), shell=True,
                    stdout=subprocess.PIPE)

    print("Deploying {}... {}".format(cloud_function_name, allow_unauthenticated_clause))
    proc = subprocess.call("gcloud functions deploy {} --entry-point {} --runtime python39 --trigger-http {} {}"
                           "".format(cloud_function_name, cloud_function_name, env_vars_clause,
                                     allow_unauthenticated_clause), shell=True,
                           stdout=subprocess.PIPE)


if __name__ == "__main__":
    main()
