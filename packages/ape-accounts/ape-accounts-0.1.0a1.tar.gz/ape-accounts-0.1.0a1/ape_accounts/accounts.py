from typing import Iterator, List, Optional
from pathlib import Path
import json

import click
from eth_account import Account  # type: ignore
from eth_account.messages import SignableMessage  # type: ignore
from eth_account.datastructures import SignedMessage, SignedTransaction  # type: ignore

from ape import config
from ape.accounts import AccountAPI, AccountControllerAPI
from ape.convert import to_address


class KeyfileAccount(AccountAPI):
    def __init__(self, keyfile: Path):
        self._keyfile = keyfile
        self.locked = True
        self.__cached_key = None

    @property
    def alias(self) -> str:
        return self._keyfile.stem

    @property
    def keyfile(self) -> dict:
        return json.loads(self._keyfile.read_text())

    @property
    def address(self) -> str:
        return to_address(self.keyfile["address"])

    @classmethod
    def generate(cls, path: Path) -> "KeyfileAccount":
        extra_entropy = click.prompt(
            "Add extra entropy for key generation...",
            hide_input=True,
        )
        a = Account.create(extra_entropy)
        passphrase = click.prompt(
            "Create Passphrase",
            hide_input=True,
            confirmation_prompt=True,
        )
        path.write_text(json.dumps(Account.encrypt(a.privateKey, passphrase)))
        return cls(path)

    @classmethod
    def from_key(cls, path: Path) -> "KeyfileAccount":
        a = Account(click.prompt("Enter Private Key", hide_input=True))
        passphrase = click.prompt(
            "Create Passphrase",
            hide_input=True,
            confirmation_prompt=True,
        )
        path.write_text(json.dumps(Account.encrypt(a.privateKey, passphrase)))
        return cls(path)

    @property
    def __key(self) -> Account:
        if self.__cached_key is not None:
            if not self.locked:
                click.echo(f"Using cached key for '{self.alias}'")
                return self.__cached_key
            else:
                self.__cached_key = None

        passphrase = click.prompt(
            f"Enter Passphrase to unlock '{self.alias}'",
            hide_input=True,
            default="",  # Just in case there's no passphrase
        )

        key = Account.decrypt(self.keyfile, passphrase)

        if click.confirm("Leave '{self.alias}' unlocked?"):
            self.locked = False
            self.__cached_key = key

        return key

    def unlock(self):
        passphrase = click.prompt(
            f"Enter Passphrase to permanently unlock '{self.alias}'",
            hide_input=True,
        )

        self.__cached_key = Account.decrypt(self.keyfile, passphrase)

    def lock(self):
        self.locked = True

    def change_password(self):
        self.locked = True  # force entering passphrase to get key
        key = self.__key

        passphrase = click.prompt(
            "Create New Passphrase",
            hide_input=True,
            confirmation_prompt=True,
        )

        self._keyfile.write_text(json.dumps(Account.encrypt(key, passphrase)))

    def sign_message(self, msg: SignableMessage) -> Optional[SignedMessage]:
        if self.locked and not click.confirm(f"Sign: {msg}"):
            return None

        return Account.sign_message(msg, self.__key)

    def sign_transaction(self, txn: dict) -> Optional[SignedTransaction]:
        if self.locked and not click.confirm(f"Sign: {txn}"):
            return None

        return Account.sign_transaction(txn, self.__key)


# TODO: LedgerAccount, TrezorAccount, etc. for hw wallets


class AccountController(AccountControllerAPI):
    @property
    def path(self) -> Path:
        return config.DATA_FOLDER.joinpath("accounts")

    @property
    def aliases(self) -> List[str]:
        return [p.stem for p in self.path.glob("*.json")]

    def load(self, alias: str) -> AccountAPI:
        for a in self:
            if isinstance(a, KeyfileAccount) and a.alias == alias:
                return a

        raise ValueError(f"Account '{alias}' not in {self.path}")

    def __len__(self) -> int:
        return len([*self.path.glob("*.json")])

    def __iter__(self) -> Iterator[AccountAPI]:
        for keyfile in self.path.glob("*.json"):
            yield KeyfileAccount(keyfile)
