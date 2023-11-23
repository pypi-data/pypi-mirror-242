import click

from lumipy.cli.commands.config import config_main
from lumipy.cli.commands.query import query_main
from lumipy.cli.commands.run import run_main
from lumipy.cli.commands.test import test_main
from lumipy.cli.commands.setup import setup_main
from typing import Optional


@click.group()
def cli():
    pass


@click.command()
@click.argument('action', required=False)
@click.option('--domain', help='the domain')
@click.option('--token', help='the token')
def config(action: Optional[str], domain: str, token: str):
    config_main(action, domain, token)


@click.command()
@click.option('--sql', help='the sql')
@click.option('--domain', help='the domain')
@click.option('--save-to', help='save to')
def query(sql: str, domain: Optional[str], save_to: Optional[str]):
    query_main(sql, domain, save_to)


@click.command()
@click.argument('target')
@click.option('--name', help='the name to give the pandas provider')
@click.option('--user', help='the name to give the pandas provider')
@click.option('--port', help='the name to give the pandas provider', default=5001, type=int)
@click.option('--domain', help='the name to give the pandas provider')
@click.option('--whitelist-me', help='the name to give the pandas provider', type=bool, is_flag=True)
def run(target: str, name: str, user, port, domain, whitelist_me):
    run_main(target, name, user, port, domain, whitelist_me)


@click.command()
@click.argument('manifest')
@click.option('--max-workers', default=16, type=int)
@click.option('--verbosity', default=2, type=int)
def test(manifest, max_workers, verbosity):
    test_main(manifest, max_workers, verbosity)


@click.command()
@click.argument('target', required=False)
@click.option('--domain')
def setup(target, domain):
    setup_main(target, domain)


cli.add_command(config)
cli.add_command(query)
cli.add_command(run)
cli.add_command(test)
cli.add_command(setup)

if __name__ == '__main__':
    cli()
