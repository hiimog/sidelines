import click as c
import log as l

log = l.Log("main")


@c.group()
def util():
    pass


@c.command()
def info():
    c.echo("in click")


if __name__ == "__main__":
    log.debug("f4dd0d93-33a0-4928-8637-58be4bd2e452", "Util starting")
    util()
