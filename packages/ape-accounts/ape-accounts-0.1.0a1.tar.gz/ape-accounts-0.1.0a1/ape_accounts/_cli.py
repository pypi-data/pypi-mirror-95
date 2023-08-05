import shutil

from pathlib import Path

import click

from .accounts import KeyfileAccount, AccountController


@click.group(short_help="Manage local accounts")
def cli():
    """
    Command-line helper for managing local accounts. You can unlock local accounts from
    scripts or the console using the Accounts.load() method.
    """


# Different name because `list` is a keyword
@cli.command(name="list", short_help="List available accounts")
def _list():
    accounts = AccountController()

    if len(accounts) == 0:
        click.echo("No accounts found.")
        return

    elif len(accounts) >= 1:
        click.echo(f"Found {len(accounts)} accounts:")

    else:
        click.echo("Found 1 account:")

    for account in accounts:
        click.echo(account)


@cli.command(short_help="Add a new account with a random private key")
@click.argument("alias")
def generate(alias):
    accounts = AccountController()
    assert alias not in accounts.aliases
    a = KeyfileAccount.generate(accounts.path.joinpath(f"{alias}.json"))
    click.echo(f"A new account '{a.address}' has been added with the id '{alias}'")


# Different name because `import` is a keyword
@cli.command(name="import", short_help="Add a new account by entering a private key")
@click.argument("alias")
def _import(alias):
    accounts = AccountController()
    assert alias not in accounts.aliases
    a = KeyfileAccount.from_key(accounts.path.joinpath(f"{alias}.json"))
    click.echo(f"A new account '{a.address}' has been added with the id '{alias}'")


@cli.command(short_help="Import a new account via a keystore file")
@click.argument("alias", type=click.Choice(AccountController().aliases))
@click.argument("path", type=click.Path(exists=False, dir_okay=False, allow_dash=True))
def export(alias, path):
    account = AccountController().load(alias)

    dest_path = Path(path).absolute()
    if not dest_path.suffix:
        dest_path = dest_path.with_suffix(".json")

    shutil.copy(account.path, dest_path)

    click.echo(f"Account with alias '{alias}' has been exported to keystore '{dest_path}'")


@cli.command(short_help="Change the password of an existing account")
@click.argument("alias", type=click.Choice(AccountController().aliases))
def change_password(alias):
    account = AccountController().load(alias)
    account.change_password()
    click.echo(f"Password has been changed for account '{alias}'")


@cli.command(short_help="Delete an existing account")
@click.argument("alias", type=click.Choice(AccountController().aliases))
def delete(alias):
    account = AccountController().load(alias)
    account.path.unlink()
    click.echo(f"Account '{alias}' has been deleted")
