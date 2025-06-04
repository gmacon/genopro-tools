import logging
import zipfile

import click
from lxml import etree


@click.group()
@click.argument("genofile", type=click.File("r+b"))
@click.pass_context
def cli(ctx, genofile):
    logging.basicConfig()

    if genofile.seekable and zipfile.is_zipfile(genofile):
        with zipfile.ZipFile(genofile, "r") as zf:
            with zf.open("Data.xml", "r") as xml:
                geno = etree.parse(xml)
    else:
        geno = etree.parse(genofile)

    ctx.obj = {"tree": geno}


@cli.result_callback()
@click.pass_context
def done(ctx, changed, genofile):
    geno = ctx.obj["tree"]

    if not genofile.seekable:
        geno.write(genofile)
    else:
        genofile.seek(0)
        genofile.truncate(0)
        with zipfile.ZipFile(genofile, "w") as zf:
            with zf.open("Data.xml", "w") as xml:
                geno.write(xml)
