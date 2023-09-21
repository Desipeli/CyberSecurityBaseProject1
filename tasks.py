from invoke import task
import platform
from src.build import initialize_db


pty = True
python = "python3"
if platform.system() == "Windows":
    pty = False
    python = "python"


@task
def dev(ctx):
    ctx.run("flask --app ./src/app.py run --debug", pty=pty)


@task
def build(ctx):
    initialize_db()


@task
def csrf(ctx):
    ctx.run("flask --app ./csrf_page/app.py run --port=5001 --debug", pty=pty)
