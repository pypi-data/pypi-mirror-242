"""A cli interface for the linker."""
import mmap
import os

import click
from monistode_binutils_shared import (
    Executable,
    ExecutableFile,
    HarvardExecutableFilePair,
    ObjectManager,
)

from .linker import Linker


@click.group()
def cli():
    """The main cli group."""
    pass


@cli.command()
@click.option(
    "--input", "-i", help="The input file.", multiple=True, type=click.Path(exists=True)
)
@click.option(
    "--output",
    "-o",
    help="The output file or folder.",
    required=True,
    type=click.Path(),
)
@click.option(
    "--harvard/--no-harvard",
    "-h",
    help="Whether to use harvard architecture.",
    default=False,
)
@click.option(
    "--max-merge-distance",
    "-m",
    help="The maximum distance between two mergeable sections.",
    default=0x100,
)
def link(
    input: tuple[str, ...], output: str, harvard: bool, max_merge_distance: int
) -> None:
    """Link the input files into the output file."""
    linker = Linker()

    executable: Executable
    if os.path.isdir(output):
        if harvard:
            executable = HarvardExecutableFilePair.from_folder(output)
        else:
            raise click.BadParameter(
                "Cannot create non-harvard executable in folder.", param_hint="output"
            )
    elif os.path.exists(output):
        output_file = open(output, "rb+")
        output_file.write(bytes(ExecutableFile.empty()))
        output_file.flush()
        executable = ExecutableFile(mmap.mmap(output_file.fileno(), 0))
    elif output.endswith("/"):
        if harvard:
            os.makedirs(output)
            executable = HarvardExecutableFilePair.from_folder(output)
        else:
            raise click.BadParameter(
                "Cannot create non-harvard executable in folder.", param_hint="output"
            )
    else:
        output_file = open(output, "wb+")
        output_file.write(bytes(ExecutableFile.empty()))
        output_file.flush()
        executable = ExecutableFile(mmap.mmap(output_file.fileno(), 0))

    for file in input:
        with open(file, "rb") as f:
            linker.add_object(ObjectManager.from_bytes(f.read()))

    linker.link(
        executable,
        harvard=harvard,
        max_merge_distance=max_merge_distance,
    )


if __name__ == "__main__":
    cli()
