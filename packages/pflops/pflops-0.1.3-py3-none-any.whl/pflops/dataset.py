from os import path
from urllib.parse import urljoin

import requests
import typer
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from rich import print
from rich.columns import Columns
from rich.progress import Progress
from typing_extensions import Annotated

from . import config
from .common import FileInfo

app = typer.Typer()


@app.command()
def ls():
    """
    List available datasets.
    """
    r = requests.get(url=urljoin(config.BASE_URL, "/dataset/list"))
    if r.status_code != 200:
        print("[red]Failed to reach Petaflops server.")
        return
    body: list[FileInfo] = r.json()
    filenames = [file["name"] for file in body]
    print(Columns(filenames, padding=(0, 6)))


@app.command()
def upload(
    file_path: str,
    name: Annotated[
        str,
        typer.Option(
            help="If set, your dataset file will be named to this value in the server."
        ),
    ] = "",
):
    """
    Upload dataset to the server.
    """
    if path.isdir(file_path):
        print(
            f"[yellow][b]{file_path}[/b] is a directory. If you want to upload multiple files, zip it to a single file first."
        )
        return
    if not path.isfile(file_path):
        print(f"[yellow]File [b]{file_path}[/b] does not exist.")
        return
    with Progress() as progress:
        task_id = None

        def callback(monitor: MultipartEncoderMonitor):
            if task_id is not None:
                progress.update(
                    task_id, total=monitor.len, completed=monitor.bytes_read
                )

        if not name:
            name = file_path.split("/")[-1]
        encoder = MultipartEncoder(fields={name: open(file_path, "rb")})
        monitor = MultipartEncoderMonitor(encoder=encoder, callback=callback)
        task_id = progress.add_task(description="Uploading...")
        r = requests.post(
            url=urljoin(config.BASE_URL, "/dataset/upload"),
            data=monitor,
            headers={"Content-Type": monitor.content_type},
        )
        progress.remove_task(task_id)
        if r.status_code in [200, 201]:
            print("[green]Upload succeeded.")
        else:
            print(f"[red]Upload failed. Status code: {r.status_code}")
