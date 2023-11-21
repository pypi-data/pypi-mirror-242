from enum import Enum
import os
import sys
import requests
import time
import rich
from loguru import logger

from flowdeploy.keys import get_key

FLOWDEPLOY_BASE_URL = os.environ.get("FLOWDEPLOY_API_URL", "https://api.toolche.st")


class States(str, Enum):
    QUEUED = 'QUEUED',
    INITIALIZING = 'INITIALIZING',
    RUNNING = 'RUNNING',
    PAUSED = 'PAUSED',
    COMPLETE = 'COMPLETE',
    EXECUTOR_ERROR = 'EXECUTOR_ERROR',
    SYSTEM_ERROR = 'SYSTEM_ERROR',
    CANCELED = 'CANCELED',
    UNKNOWN = 'UNKNOWN',


TERMINAL_STATES = [
    States.COMPLETE,
    States.EXECUTOR_ERROR,
    States.SYSTEM_ERROR,
    States.CANCELED,
    States.UNKNOWN,
]


def create_headers(**kwargs):
    api_key = get_key(kwargs.get('cli', False))
    return {
        "Authorization": f"Key {api_key}",
        "Content-Type": "application/json",
    }


def fetch_task(task_id, **kwargs):
    headers = create_headers(**kwargs)
    response = requests.get(f"{FLOWDEPLOY_BASE_URL}/tes/v1/tasks/{task_id}", headers=headers)
    if response.status_code not in [200]:
        error_json = response.json()
        error = error_json.get('error', 'Unknown')
        raise RuntimeError(f"Failed to get task information. Error: {error}")
    return response.json()


def start_pipeline(type_key, payload, is_async, **kwargs):
    headers = create_headers(**kwargs)
    response = requests.post(f"{FLOWDEPLOY_BASE_URL}/flowdeploy/{type_key}", json=payload, headers=headers)

    if response.status_code not in [200, 201]:
        error_json = response.json()
        error = error_json['error'] or 'Unknown'
        raise RuntimeError(f"Failed to create FlowDeploy instance. Error: {error}")

    task_id = response.json()["id"]
    run = {"id": task_id, "state": States.QUEUED}
    logger.info(f"FlowDeploy instance created. Task ID: {task_id}")
    logger.info(f"You can view the running job at https://app.flowdeploy.com/dashboard/{task_id}?runType=1")

    if is_async:
        logger.info("Async run initiated!")
        return run

    counter = 0
    while run["state"] not in TERMINAL_STATES:
        if counter % 5 == 0:  # Check state every 5 seconds
            run = fetch_task(task_id, **kwargs)

        status_message = f"State: {run['state']} ({'*' * (counter % 5 + 1)}) "

        sys.stdout.write(
            f"\r{status_message}".ljust(120),
        )
        sys.stdout.flush()

        counter += 1
        time.sleep(1)

    sys.stdout.write(
        f"\rState: {run['state']}".ljust(120) + '\n',
    )
    sys.stdout.flush()
    logger.info("FlowDeploy run finished.")
    return run


def nextflow(pipeline, outdir, release=None, branch=None, inputs=None, cli_args="", export_location=None, profiles=None,
             run_location=None, is_async=False, **kwargs):
    try:
        if export_location is not None and export_location.startswith('fd://'):
            raise ValueError("Export location is for locations outside FlowDeploy. "
                             "Use 'outdir' to place results where you want in the shared file system.")
        if not outdir:
            raise ValueError("outdir must be set for Nextflow pipelines.")
        if not outdir.startswith('fd://'):
            raise ValueError("Path in outdir must be within the shared file system.")
        if not release and not branch:
            raise ValueError("Either the git release or branch must be set.")
        if release and branch:
            raise ValueError("Only one of the git release or branch can be set.")
        payload = {
            "pipeline": pipeline,
            "inputs": inputs,
            "cli_args": cli_args,
            "pipeline_version": release or branch,
            "outdir": outdir,
            "export_location": export_location,
            "profiles": profiles,
            "run_location": run_location,
            "use_git_release": release is not None,
        }
        return start_pipeline("nf", payload, is_async, **kwargs)
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")


def snakemake(pipeline, release=None, branch=None, inputs=None, cli_args="", export_location=None,
              export_location_source=None, profiles=None, is_async=False, run_location=None, targets=None,
              snakemake_folder=None, snakefile_location='workflow/Snakefile', **kwargs):
    try:
        if export_location is not None and export_location.startswith('fd://'):
            raise ValueError("Export location is for locations outside FlowDeploy.")
        if export_location is not None and export_location_source is None:
            raise ValueError("Export location source must be provided when exporting results.")
        if not release and not branch:
            raise ValueError("Either the git release or branch must be set.")
        if release and branch:
            raise ValueError("Only one of the git release or branch can be set.")
        payload = {
            "pipeline": pipeline,
            "pipeline_version": release or branch,
            "inputs": inputs,
            "cli_args": cli_args,
            "snakemake_targets": [targets] if isinstance(targets, str) else targets,
            "snakemake_folder": snakemake_folder or pipeline,
            "snakefile_location": snakefile_location,
            "export_location": export_location,
            "export_location_source": export_location_source,
            "profiles": profiles,
            "run_location": run_location,
            "use_git_release": release is not None,
        }
        return start_pipeline("sm", payload, is_async, **kwargs)
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")


def transfer(transfers, is_async=False, **kwargs):
    try:
        payload = {
            "transfers": transfers,
        }
        return start_pipeline("transfer", payload, is_async, **kwargs)
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")


def get_state(task_id, **kwargs):
    try:
        return fetch_task(task_id, **kwargs)
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")
