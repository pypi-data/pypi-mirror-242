import os
from configparser import ConfigParser
from getpass import getpass
from pathlib import Path
from urllib.parse import urljoin

import requests
import typer
from rich import print

from . import dataset, image, job
from .common import BASE_URL, is_logged_in
from .fs import app

app.add_typer(dataset.app, name="dataset")
app.add_typer(image.app, name="image")
app.add_typer(job.app, name="job")

config_path = os.path.join(Path.home(), ".pflops.config")


@app.command()
def login():
    if is_logged_in():
        print("[yellow]Already logged in.")
        return

    config = ConfigParser()
    username = input("Username: ")
    password = getpass()
    r = requests.post(
        url=urljoin(BASE_URL, "/auth/login"),
        data={
            "username": username,
            "password": password,
        },
    )
    if r.status_code in [200, 201]:
        with open(config_path, "a") as config_file:
            config["Authentication"] = {
                "token": r.json()["token"],
            }
            config.write(config_file)
        print("[green]Logged in.")
    else:
        print("[red]Wrong username or password.")


@app.command()
def logout():
    if not is_logged_in():
        print("[yellow]Already logged out.")
        return

    config = ConfigParser()
    with open(config_path, "w") as config_file:
        config.remove_section("Authentication")
        config.write(config_file)
    print("[green]Logged out.")
