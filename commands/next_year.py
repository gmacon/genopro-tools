"""
next_year.py

Advance the database to the next year.
"""

import argparse
import logging

logger = logging.getLogger(__name__)

def main(geno, rest):
    parser = argparse.ArgumentParser("Advance database to next year")
    parser.add_argument('--year', type=int, help='The year to advance to')
    args = parser.parse_args(rest)
    
    year = geno.X_TAGYEAR
    if args.year:
        year.string = str(args.year)
    else:
        year.string = str(int(year.string) + 1)
    
    for i in geno("Individual"):
        if i.has_attr("IndividualInternalHyperlink"):
            continue
        normal = i.X_NORMAL
        if normal is None:
            logger.warning(
                "Individual %s has no normal attendance.",
                i.Name.Display.string)
        else:
            i.X_NAMTAG.string = normal.string
    
    return True