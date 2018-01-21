"""
remove_old_custom.py

Remove the old custom tags X_ATTEND, X_FAMILY, and X_LINNUM.
Transition X_ATTEND to X_NORMAL
"""

def main(geno, rest):
    for ind in geno("Individual"):
        attend = ind.X_ATTEND
        if attend is not None:
            attend = attend.extract()
            normal = geno.new_tag('X_NORMAL')
            if int(attend.string, 0):
                normal.string = '1'
            else:
                normal.string = '0'
            ind.append(normal)
        linnum = ind.X_LINNUM
        if linnum is not None:
            linnum.extract()
        family = ind.X_FAMILY
        if family is not None:
            family.extract()
    return True