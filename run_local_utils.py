import os


def init_local_env():
    try:
        if os.environ['LOCAL_DEV_ENV'] == "TRUE":
            import local_run_def
            for k, v in local_run_def.deploy_vars.items():
                os.environ[k] = v
    except Exception as e:
        pass
