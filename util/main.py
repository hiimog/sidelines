import sys
import click as c
import logging as l
import seqlog
import orjson

seqlog.log_to_seq(server_url="http://127.0.0.1:5341",
                  level=l.DEBUG,
                  batch_size=1,
                  override_root_logger=True)
logger = l.getLogger()


@c.group()
def util():
    pass


@c.command()
def info():
    c.echo("in click")


if __name__ == "__main__":
    util()
