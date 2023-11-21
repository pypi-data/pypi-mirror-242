import json
import subprocess

import rich
import typer
from enum import Enum
from typing import List
from typing_extensions import Annotated

import flowdeploy
from flowdeploy import nextflow, set_key, snakemake

app = typer.Typer(pretty_exceptions_show_locals=False, rich_markup_mode="rich")


class WorkflowManager(str, Enum):
    snakemake = 'snakemake'
    nextflow = 'nextflow'


def parse_json_file(path):
    if path:
        with open(path, 'r') as file:
            return json.load(file)
    return None


@app.command()
def run(
    workflow_manager: Annotated[
        WorkflowManager,
        typer.Argument(help="Specify if the pipeline being run is a Nextflow or Snakemake pipeline.")
    ],
    pipeline: Annotated[str, typer.Argument(help="The name of the pipeline")],
    git_release: Annotated[str, typer.Option(
        '--release', '-r',
        help="The git release tag to use for execution of the pipeline. Either --release or --branch must be set."
    )] = None,
    git_branch: Annotated[str, typer.Option(
        '--branch', '-b',
        help="The git branch to use for execution of the pipeline. Either --release or --branch must be set."
    )] = None,
    outdir: Annotated[
        str, typer.Option(
            '--outdir',
            '-o',
            help="Set the output directory to store the results from the pipeline run. "
                 "Note that the path must be a FlowDeploy file path. Required with Nextflow only.")
    ] = None,
    input_file: Annotated[
        str, typer.Option('--input-file', '-i', help="The path to a JSON file that contains all inputs.")
    ] = None,
    cli_args: Annotated[
        str, typer.Option(help="Used to pass raw command line arguments to the workflow manager (must be in quotes).")
    ] = '',
    export_location: Annotated[
        str, typer.Option(help="An S3 location to export results.")
    ] = None,
    export_location_source: Annotated[
        str,
        typer.Option(
            help="Exports the contents of this path to the --export-location destination. Must be a shared file."
        )
    ] = None,
    profiles: Annotated[
        List[str],
        typer.Option(
            '--profile',
            help="Workflow manager configuration profiles. To add multiple profiles, add --profile multiple times."
        )
    ] = None,
    run_location: Annotated[
        str, typer.Option(help="A FlowDeploy path to use as the working directory for the pipeline.")
    ] = None,
    snakemake_folder: Annotated[
        str, typer.Option(
            help="Snakemake's working directory, relative to the run location. Defaults to the pipeline name.")
    ] = None,
    snakefile_location: Annotated[
        str, typer.Option(
            help="Snakefile location, relative to the Snakemake folder name. Defaults to 'workflow/Snakefile'.")
    ] = 'workflow/Snakefile',
    targets: Annotated[
        List[str], typer.Option('--target', help="Snakemake targets. "
                                                 "To add multiple targets, add --target multiple times.")
    ] = None,
    is_async: Annotated[
        bool,
        typer.Option("--is-async", help="If set, exits immediately after spawning a FlowDeploy instance.")
    ] = False,
    flowdeploy_key: Annotated[
        str,
        typer.Option(help="FlowDeploy API key to authenticate the run (can also be set in the environment)")
    ] = None,
):
    """
    Runs a pipeline with FlowDeploy. Full documentation: https://flowdeploy.com/docs/reference/cli#flowdeploy-run.
    """
    try:
        if flowdeploy_key:
            set_key(flowdeploy_key)
        inputs = parse_json_file(input_file)
        if profiles:
            profiles = list(filter(lambda profile: profile != '', profiles))
        if workflow_manager == WorkflowManager.snakemake:
            snakemake(
                pipeline=pipeline,
                release=git_release,
                branch=git_branch,
                inputs=inputs,
                cli_args=cli_args,
                export_location=export_location,
                export_location_source=export_location_source,
                profiles=profiles,
                run_location=run_location,
                targets=targets,
                snakemake_folder=snakemake_folder or pipeline,
                snakefile_location=snakefile_location,
                is_async=is_async,
                cli=True,
            )
        else:
            nextflow(
                pipeline=pipeline,
                outdir=outdir,
                release=git_release,
                branch=git_branch,
                inputs=inputs,
                cli_args=cli_args,
                export_location=export_location,
                profiles=profiles,
                run_location=run_location,
                is_async=is_async,
                cli=True,
            )
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")


@app.command()
def transfer(
    input_file: Annotated[
        str, typer.Option('--input-file', '-i', help="The path to a JSON file that contains all transfers.")
    ],
    is_async: Annotated[
        bool,
        typer.Option("--is-async", help="Exits immediately after spawning the FlowDeploy instance if set")
    ] = False,
    flowdeploy_key: Annotated[
        str,
        typer.Option(help="FlowDeploy API key to authenticate the run (can also be set in the environment)")
    ] = None,
):
    """
    Transfers files to and from the shared file system. Full documentation: \
https://flowdeploy.com/docs/reference/cli#transfer
    """
    try:
        if flowdeploy_key:
            set_key(flowdeploy_key)
        transfers = parse_json_file(input_file)
        flowdeploy.transfer(transfers, is_async, cli=True)
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")


@app.command('set-key')
def set_flowdeploy_key(
    flowdeploy_key: Annotated[str, typer.Argument(help="Sets your FlowDeploy key in your environment")],
    config_file: Annotated[
        str, typer.Option(
            '--config',
            '-c',
            help="Specify the path to the configuration file where the key should be set. "
                 "It defaults to ~/.zshenv on macOS and ~/.bashrc on Linux.")
    ] = None,
):
    """
    Appends FLOWDEPLOY_KEY to the end of the shell environment config file. \
Defaults to '~/.zshenv' on macOS and '~/.bashrc' on Linux.
    """
    config_location = config_file
    try:
        if not config_file:
            uname = subprocess.run("uname", capture_output=True, shell=True).stdout.strip().decode('utf-8')
            config_location = '~/.zshenv' if uname == 'Darwin' else '~/.bashrc'
        subprocess.run(f'echo "export FLOWDEPLOY_KEY={flowdeploy_key}" >> {config_location}', text=True, shell=True)\
            .check_returncode()
        success_message = f"Key is now set in {config_location}. " \
                          f"Restart your terminal or run `source {config_location}` to use the key."
        print(success_message)
    except subprocess.CalledProcessError as err:
        raise ValueError(f"Failed to set key in {config_location}\n", err.output)
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")


@app.command('status')
def get_state(
    run_id: Annotated[str, typer.Argument(help="The FlowDeploy ID for the run.")],
    flowdeploy_key: Annotated[
        str,
        typer.Option(help="FlowDeploy API key to authenticate the run (can also be set in the environment)")
    ] = None,
):
    """
    Checks the state of a FlowDeploy pipeline or transfer run.
    """
    try:
        if flowdeploy_key:
            set_key(flowdeploy_key)
        run = flowdeploy.get_state(task_id=run_id, cli=True)
        rich.print(f"[bold blue]State:[/bold blue] {run['state']}")
    except Exception as e:
        rich.print(f"[bold red]{type(e).__name__}:[/bold red] {e}")
