import click

from ape.accounts import AccountControllerAPI

from .accounts import AccountController
from ._cli import cli


def ape_get_cli_group() -> click.Group:
    return cli


def ape_get_accounts() -> AccountControllerAPI:
    return AccountController()
