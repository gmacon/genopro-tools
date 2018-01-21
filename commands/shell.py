"""Run a shell with the GenoPro document loaded as a BeautifulSoup tree."""

import code
try:
    import readline
except ImportError:
    pass

def main(geno, rest):
    save_changes = False
    code.interact(
        "Whelchel GenoPro Tools Shell", raw_input,
        {
            '__name__': '__console__',
            '__doc__': None,
            'geno': geno,
            'save_changes': save_changes,
        })
    return save_changes