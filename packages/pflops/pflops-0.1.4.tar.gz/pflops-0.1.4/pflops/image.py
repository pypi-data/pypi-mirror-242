from urllib.parse import urljoin

import requests
import typer
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from rich import print
from rich.columns import Columns
from rich.progress import Progress
from typing_extensions import Annotated

from .common import FileInfo, BASE_URL, is_logged_in

app = typer.Typer()


@app.command()
def ls():
    """
    List available images.
    """
    if not is_logged_in():
        print("[red]Not authenticated. Log in first with `pflops login`.")
        return

    r = requests.get(url=urljoin(BASE_URL, "/image/list"))
    body: list[FileInfo] = r.json()
    filenames = [file["name"] for file in body]
    print(Columns(filenames, padding=(0, 6)))


@app.command()
def build(
    base: Annotated[
        str,
        typer.Option(
            help="Tag of the base Docker image. Must be public.",
        ),
    ],
    name: Annotated[
        str,
        typer.Option(
            help="Name of the image file, e.g. training.sif",
        ),
    ],
    requirements: Annotated[
        str,
        typer.Option(
            help="Path of the requirements.txt file that was uploaded to the server.",
        ),
    ],
):
    """
    Build a new Singularity image from the requirements.txt file.
    """
    if not is_logged_in():
        print("[red]Not authenticated. Log in first with `pflops login`.")
        return

    print("[green]Building the image... this might take a few minutes.")
    r = requests.post(
        url=urljoin(BASE_URL, "/image/build"),
        data={
            "image_name": name,
            "base_image": base,
            "requirements_file": requirements,
        },
    )
    if r.status_code in [200, 201]:
        print("Image was successfully built. Check with `pflops image ls`.")
    else:
        print(f"[red]Image build failed. Status code: {r.status_code}")
