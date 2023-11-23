"""Provide main CLI parser."""

import argparse
import sys
from pathlib import Path
from typing import Dict, Any, NoReturn

import colorama

from spotter.client.commands import (
    login,
    logout,
    register,
    suggest,
    set_policies,
    clear_policies,
    get_config,
    set_config,
    clear_config,
)
from spotter.client.commands import scan
from spotter.client.utils import PrintCurrentVersionAction, UsagePrefixRawDescriptionHelpFormatter
from spotter.library.api import ApiClient
from spotter.library.storage import Storage
from spotter.library.utils import validate_url


class ArgParser(argparse.ArgumentParser):
    """An argument parser that displays help on error."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._positionals.title = "Arguments"  # pylint: disable=protected-access
        self._optionals.title = "Options"  # pylint: disable=protected-access

    def error(self, message: str) -> NoReturn:
        """
        Overridden the original error method.

        :param message: Error message
        """
        print(f"Error: {message}\n", file=sys.stderr)
        self.print_help()
        sys.exit(2)

    def add_subparsers(self, **kwargs: Dict[str, Any]) -> argparse._SubParsersAction:  # type: ignore
        """Overridden the original add_subparsers method (workaround for http://bugs.python.org/issue9253)."""
        subparsers = super().add_subparsers()
        subparsers.required = True
        subparsers.dest = "command"
        self._positionals.title = "Commands"  # pylint: disable=protected-access
        return subparsers


def create_parser() -> ArgParser:
    """
    Create argument parser for CLI.

    :return: Parser as argparse.ArgumentParser object
    """
    parser = ArgParser(
        formatter_class=lambda prog: UsagePrefixRawDescriptionHelpFormatter(
            prog,
            usage_prefix="Steampunk Spotter - Ansible Playbook Platform that scans, analyzes, enhances, and "
            "provides insights for your playbooks.",
            max_help_position=48,
        ),
        epilog="Additional information:\n"
        "  You will need Steampunk Spotter account to be able to use the CLI.\n"
        "  Create one with spotter register command or at https://spotter.steampunk.si/.\n\n"
        "  To log in to Steampunk Spotter, you should provide your API token or username and password:\n"
        "    - using spotter login command;\n"
        "    - via --api-token/-t option;\n"
        "    - by setting SPOTTER_API_TOKEN environment variable;\n"
        "    - via --username/-u and --password/-p global options;\n"
        "    - by setting SPOTTER_USERNAME and SPOTTER_PASSWORD environment variables.\n\n"
        "  What do you think about Spotter? Share your thoughts at "
        "https://spotter.steampunk.si/feedback.\n"
        "  Need more help or having other questions? Contact us at https://steampunk.si/contact/.",
        add_help=False,
        usage="spotter [OPTIONS] <COMMAND>",
    )

    parser.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    parser.add_argument(
        "-v",
        "--version",
        action=PrintCurrentVersionAction,
        nargs=0,
        help="Display the version of Steampunk Spotter CLI",
    )
    parser.add_argument(
        "-e",
        "--endpoint",
        type=validate_url,
        help=f"Steampunk Spotter API endpoint (instead of default {ApiClient.DEFAULT_ENDPOINT})",
    )
    parser.add_argument(
        "-s",
        "--storage-path",
        type=lambda p: Path(p).absolute(),
        help=f"Storage folder location (instead of default {Storage.DEFAULT_PATH})",
    )
    parser.add_argument("-t", "--api-token", type=str, help="Steampunk Spotter API token")
    parser.add_argument("-u", "--username", type=str, help="Steampunk Spotter username")
    parser.add_argument("-p", "--password", type=str, help="Steampunk Spotter password")
    parser.add_argument("--timeout", type=int, help="Steampunk Spotter API timeout (in seconds)")
    parser.add_argument("--no-color", action="store_true", help="Disable output colors")
    parser.add_argument("--no-colors", dest="no_color", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")

    subparsers = parser.add_subparsers()
    subparsers_metavar = ""
    cmds = [
        (register.__name__.rsplit(".", maxsplit=1)[-1], register),
        (login.__name__.rsplit(".", maxsplit=1)[-1], login),
        (logout.__name__.rsplit(".", maxsplit=1)[-1], logout),
        (scan.__name__.rsplit(".", maxsplit=1)[-1], scan),
        (suggest.__name__.rsplit(".", maxsplit=1)[-1], suggest),
        (set_policies.__name__.rsplit(".", maxsplit=1)[-1], set_policies),
        (clear_policies.__name__.rsplit(".", maxsplit=1)[-1], clear_policies),
        (get_config.__name__.rsplit(".", maxsplit=1)[-1], get_config),
        (set_config.__name__.rsplit(".", maxsplit=1)[-1], set_config),
        (clear_config.__name__.rsplit(".", maxsplit=1)[-1], clear_config),
    ]
    for command_name, module in cmds:
        # FIXME: Remove this if we decide that suggest command can be used standalone
        if command_name != "suggest":
            subparsers_metavar += f"{command_name.replace('_', '-')},"
        module.add_parser(subparsers)

    subparsers.metavar = f"{{{subparsers_metavar.rstrip(',')}}}"

    return parser


def main() -> None:
    """Create main CLI parser and parse arguments."""
    parser = create_parser()
    args = parser.parse_args()
    # init colorama if only when using colors
    if not args.no_color:
        colorama.init(autoreset=True)
    # check if any of the arguments is empty
    args_dict = vars(args)
    for k in args_dict:
        if args_dict[k] == "":
            print(
                f"Error: --{k.replace('_', '-')} argument is empty. "
                f"Please set the non-empty value or omit the argument if it is not needed.",
                file=sys.stderr,
            )
            sys.exit(2)
    args.func(args)


if __name__ == "__main__":
    main()
