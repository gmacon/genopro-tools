#!/usr/bin/env python2

import argparse
import logging
import sys
import zipfile

import bs4

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Whelchel GenoPro tools")
    parser.add_argument("genofile", help='The GenoPro file to modify')
    parser.add_argument("command", help="The command to run")
    args, rest = parser.parse_known_args()
    
    logging.basicConfig()

    # Read input
    if args.genofile == '-':
        geno = bs4.BeautifulSoup(sys.stdin, "xml")
    elif zipfile.is_zipfile(args.genofile):
        with zipfile.ZipFile(args.genofile, 'r') as z:
            with z.open('Data.xml', 'r') as d:
                geno = bs4.BeautifulSoup(d, 'xml')
    else:
        with open(args.genofile, 'r') as d:
                geno = bs4.BeautifulSoup(d, 'xml')
    
    # Execute command
    __import__("commands." + args.command)
    change = sys.modules["commands." + args.command].main(geno, rest)
    
    # Write output
    if change:
        if args.genofile == '-':
            sys.stdout.write(str(geno))
        else:
            with zipfile.ZipFile(args.genofile, 'w') as z:
                print "Writing back"
                z.writestr("Data.xml", str(geno), zipfile.ZIP_DEFLATED)