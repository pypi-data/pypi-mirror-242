import click
import subprocess

@click.command()
def start():
    """start your vm"""
    subprocess.run(["gcloud", "compute", "instances", "start", "--zone=europe-west1-b",  "lewagon-data-eng-vm-pavaul"])


@click.command()
def stop():
    """Stop your vm"""
    subprocess.run(["gcloud", "compute", "instances", "stop", "--zone=europe-west1-b",  "lewagon-data-eng-vm-pavau"])


@click.command()
def connect():
    """Connect to your vm in vscode inside your ~/code/pavaule/folder """
    subprocess.run(["code", "--folder-uri", "vscode-remote://ssh-remote+josephpubel@34.77.34.220/home/josephpubel/"])
