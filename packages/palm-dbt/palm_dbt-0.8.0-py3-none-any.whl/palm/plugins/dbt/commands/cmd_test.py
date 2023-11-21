import click
from typing import Optional, Tuple
from palm.plugins.dbt.dbt_palm_utils import dbt_env_vars
import sys


@click.command('test')
@click.option(
    "--clean", is_flag=True, help="Drop the test schema after the run is complete"
)
@click.option("--models", "-m", multiple=True, help="See dbt docs on models flag")
@click.option("--select", "-s", multiple=True, help="See dbt docs on select flag")
@click.option("--selector", multiple=True, help="See dbt docs on selector flag")
@click.option("--exclude", "-e", multiple=True, help="See dbt docs on exclude flag")
@click.option("--defer", "-d", is_flag=True, help="See dbt docs on defer flag")
@click.option(
    "--no-fail-fast", "-nx", is_flag=True, help="Runs all tests even if one fails"
)
@click.pass_obj
def cli(
    environment,
    clean: bool,
    no_fail_fast: bool,
    defer: bool,
    models: Optional[Tuple] = tuple(),
    select: Optional[Tuple] = tuple(),
    selector: Optional[Tuple] = tuple(),
    exclude: Optional[Tuple] = tuple(),
):
    """Tests the dbt repo"""

    if defer:
        click.secho("Running 'palm prod-artifacts'...", fg='yellow')
        exit_code, _, _ = environment.run_on_host("palm prod-artifacts")
        if exit_code == 2:
            click.secho(
                "'palm prod-artifacts' not implemented. Can't use --defer without it!",
                fg='red',
            )
            sys.exit(1)
        elif exit_code != 0:
            click.secho(
                "Something went wrong while pulling the prod artifacts.", fg='red'
            )
            sys.exit(1)

    env_vars = set_env_vars(environment, defer)

    # --select and --models are interchangeable on dbt >= v1, combine the lists of selections
    targets = list(set(models + select))

    run_cmd = build_test_command(
        no_fail_fast=no_fail_fast,
        targets=targets,
        selector=selector,
        exclude=exclude,
        defer=defer,
    )
    success, msg = environment.run_in_docker(run_cmd, env_vars)
    click.secho(msg, fg="green" if success else "red")

    if clean:
        success, msg = environment.run_in_docker(
            "dbt run-operation drop_branch_schemas", env_vars
        )
        click.secho(msg, fg="green" if success else "red")


def build_test_command(
    defer: bool = False,
    no_fail_fast: bool = False,
    targets: Optional[list] = None,
    selector: Optional[Tuple] = None,
    exclude: Optional[Tuple] = None,
) -> str:
    cmd = []

    cmd.append(f"dbt test")
    if targets:
        cmd.append('--select')
        cmd.extend(targets)
    if selector:
        cmd.append('--selector')
        cmd.extend(selector)
    if exclude:
        cmd.append('--exclude')
        cmd.extend(exclude)
    if not no_fail_fast:
        cmd.append('--fail-fast')
    if defer:
        if not targets:
            cmd.extend(["--select", "state:new", "state:modified+"])
        cmd.append("--defer")

    return " ".join(cmd)


def set_env_vars(environment, defer: bool = False) -> dict:
    plugin_config = environment.plugin_config('dbt')
    env_vars = dbt_env_vars(environment.palm.branch)

    # These env vars are renamed in dbt v1.5.0, old env vars are deprecated
    if plugin_config.is_dbt_version_greater_than("1.5.0", or_equal=True):
        defer_env_var = "DBT_DEFER"
        state_env_var = "DBT_STATE"
    else:
        defer_env_var = "DBT_DEFER_TO_STATE"
        state_env_var = "DBT_ARTIFACT_STATE_PATH"

    if defer:
        env_vars[defer_env_var] = 'true'
        env_vars[state_env_var] = plugin_config.dbt_artifacts_prod
    else:
        env_vars[state_env_var] = plugin_config.dbt_artifacts_local
    return env_vars
