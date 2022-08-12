import os
import sys
from argparse import Namespace

from git import InvalidGitRepositoryError
from rich.console import Console
from rich.table import Table

from dstack.backend import load_backend
from dstack.repo import load_repo_data
from dstack.config import ConfigError


def download_func(args: Namespace):
    try:
        backend = load_backend()
        repo_data = load_repo_data()
        backend.download_run_artifact_files(repo_data.repo_user_name, repo_data.repo_name, args.run_name, args.output)
    except InvalidGitRepositoryError:
        sys.exit(f"{os.getcwd()} is not a Git repo")
    except ConfigError:
        sys.exit(f"Call 'dstack config' first")


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def list_func(args: Namespace):
    try:
        backend = load_backend()
        repo_data = load_repo_data()
        run_artifact_files = backend.list_run_artifact_files(repo_data.repo_user_name, repo_data.repo_name,
                                                             args.run_name)
        console = Console()
        table = Table()
        table.add_column("Artifact", style="bold", no_wrap=True)
        table.add_column("File")
        table.add_column("Size", style="dark_sea_green4")
        previous_artifact_name = None
        for (artifact_name, file_name, file_size) in run_artifact_files:
            table.add_row(artifact_name if previous_artifact_name != artifact_name else "",
                          file_name, sizeof_fmt(file_size))
            previous_artifact_name = artifact_name
        console.print(table)
    except InvalidGitRepositoryError:
        sys.exit(f"{os.getcwd()} is not a Git repo")
    except ConfigError:
        sys.exit(f"Call 'dstack config' first")


def register_parsers(main_subparsers):
    parser = main_subparsers.add_parser("artifacts", help="List, download, or upload artifacts")
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser("list", help="Download artifacts", )
    list_parser.add_argument("run_name", metavar="RUN", type=str, help="A name of a run")
    list_parser.set_defaults(func=list_func)

    download_parser = subparsers.add_parser("download", help="Download artifacts", )
    download_parser.add_argument("run_name", metavar="RUN", type=str, help="A name of a run")
    download_parser.add_argument("--output", "-o", help="The directory to download artifacts to. "
                                                        "By default, it's the current directory.", type=str)
    download_parser.set_defaults(func=download_func)
