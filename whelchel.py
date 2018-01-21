#!/usr/bin/env python3

import logging
import zipfile

import click
from lxml import etree


@click.group()
@click.argument('genofile', type=click.File('r+b'),
                help='The GenoPro file to modify')
@click.pass_context
def cli(ctx, genofile):
    logging.basicConfig()

    if genofile.seekable and zipfile.is_zipfile(genofile):
        with zipfile.ZipFile(genofile, 'r') as zf:
            with zf.open('Data.xml', 'rb') as xml:
                geno = etree.parse(xml)
    else:
        geno = etree.parse(genofile)

    ctx.obj = {'tree': geno}


@cli.resultcallback()
@click.pass_context
def done(ctx, changed, genofile):
    geno = ctx.obj['tree']

    if not genofile.seekable:
        geno.write(genofile)
    else:
        genofile.seek(0)
        genofile.truncate(0)
        with zipfile.ZipFile(genofile, 'w') as zf:
            with zf.open('Data.xml', 'wb') as xml:
                geno.write(xml)


if __name__ == '__main__':
    cli()
