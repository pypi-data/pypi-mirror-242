from concurrent.futures import ProcessPoolExecutor
from importlib.metadata import version as get_version
from pathlib import Path

import typer
from turbofan import command, project

package_name = "airboss"
app = typer.Typer(add_completion=False, help=project.summary(package_name))


@app.command()
def version():
    """
    Shows the current version.
    """
    typer.echo(get_version(package_name))


projects_app = typer.Typer()
app.add_typer(projects_app, name="projects", help="Project management commands.")


@projects_app.command(
    help="Cleans all projects found in the specified path, according to the project Makefile."
)
def clean(path: Path = typer.Argument(".", help="The path to the projects.")):
    """
    Run clean executes 'make clean' in all subdirectories from the execution
    of the command.
    """
    paths = list(Path(path).glob("*/Makefile"))
    with ProcessPoolExecutor() as executor:
        executor.map(run_make_clean, paths)


def run_make_clean(path):
    typer.echo(f"Running 'make clean' in {path.parent}...")
    command.Command(["make", "-C", path.parent, "clean"]).run()


@projects_app.command(help="Runs 'all' target in projects in the specified path.")
def all(path: Path = typer.Argument(".", help="The path to the projects.")):
    paths = list(Path(path).glob("*/Makefile"))
    with ProcessPoolExecutor() as executor:
        executor.map(run_make_all, paths)


def run_make_all(path):
    typer.echo(f"Running 'make all' in {path.parent}...")
    command.Command(["make", "-C", path.parent, "all"]).run()


if __name__ == "__main__":
    app()
