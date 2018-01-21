import logging

import click

from .base import cli

logger = logging.getLogger(__name__)


@cli.command()
@click.option('--year', type=int, help='The year to advance to')
@click.pass_context
def next_year(ctx, year):
    geno = ctx.obj['tree']

    tagyear = next(geno.iter('X_TAGYEAR'))

    if year is None:
        tagyear.text = str(int(tagyear.text) + 1)
    else:
        tagyear.text = str(year)

    for i in geno.iter('Individual'):
        if i.get('IndividualInternalHyperlink') is not None:
            continue

        normal = i.find('X_NORMAL')
        if normal is None:
            displayname = i.xpath('Name/Display')
            logger.warning(
                'Individual %s (%s) has no normal attendance.',
                i.get('ID'),
                displayname[0].text if displayname else '?')
        else:
            i.find('X_NAMTAG').text = normal.text

    return True
