import click
import json

from packages import process_module
from packages import run_tests_module

@click.group(
        help="""
        Collection of utilities to help convert dbt projects into Ascend dataflows.
        """)
def cli():
    pass

def ascend_options(f):
    f = click.option('--hostname', required=True, help='Ascend hostname')(f)
    f = click.option('--data-service', required=True, help='Ascend data service name')(f)
    f = click.option('--dataflow', required=True, help='Ascend dataflow name')(f)
    return f

def load_json(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    try:
        with open(value, 'r') as f:
            manifest = json.load(f)
        ctx.ensure_object(dict)
        ctx.obj['manifest'] = manifest
    except Exception as e:
        raise click.BadParameter(f"Could not load JSON file: {e}")
    return value

def manifest_options(f):
    f = click.option('--manifest-file', required=True, help='Path to the manifest JSON file.', type=click.Path(exists=True), callback=load_json)(f)
    return f


@click.command()
@click.pass_context
@ascend_options
@manifest_options
@click.option('--default-seed', required=False, help='Default seed to connect hanging models to. Defaults to one of the nodes in the dataflow.')
def merge(ctx, **kwargs):
    """Process the compiled dbt manifest and SQL files and create/update/delete Ascend dataflow transforms."""
    process_module.merge_cmd(ctx, **kwargs)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def update_sql(ctx, **kwargs):
    """Update the SQL of existing Ascend dataflow transforms."""
    process_module.update_sql_cmd(ctx, **kwargs)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def delete(ctx, **kwargs):
    """Delete all dbt models from an Ascend dataflow."""
    process_module.delete_cmd(ctx, **kwargs)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def validate(ctx, **kwargs):
    """Validate the seeds and sources are present in the dataflow."""
    process_module.validate_cmd(ctx, **kwargs)

@click.command()
@click.pass_context
@manifest_options
def show(ctx, **kwargs):
    """Show the dependencies of dbt models."""
    process_module.show_cmd(ctx, **kwargs)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def deploy_tests(ctx, **kwargs):
    """Create and run all dbt tests against the deployed models in Ascend."""
    run_tests_module.deploy_tests_cmd(ctx, **kwargs)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def delete_tests(ctx, **kwargs):
    """Delete all dbt tests against the deployed models in Ascend."""
    run_tests_module.delete_tests_cmd(ctx, **kwargs)

@click.command()
@click.pass_context
@ascend_options
@manifest_options
def check_test_results(ctx, **kwargs):
    """Check the results of all dbt tests against the deployed models in Ascend."""
    run_tests_module.check_test_results_cmd(ctx, **kwargs)

cli.add_command(merge)
cli.add_command(delete)
cli.add_command(validate)
cli.add_command(show)
cli.add_command(deploy_tests)
cli.add_command(delete_tests)
cli.add_command(check_test_results)
cli.add_command(update_sql)

if __name__ == "__main__":
    cli(prog_name='ascend_dbt_transform')