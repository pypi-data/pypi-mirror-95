# -*- coding: utf-8 -*-
"""Install pype's autocompletion and aliases."""

import click

from pype.core import PypeCore
from pype.util.cli import fname_to_name, print_success


@click.command(name=fname_to_name(__file__), help=__doc__)
def main() -> None:
    """Script's main entry point."""
    core = PypeCore()
    core.install_to_shell()
    print_success('Done. Please source your rc-file or open a new shell.')
