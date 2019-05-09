from collections import OrderedDict as odict

def importREE(fobj):
    REE = odict()
    REElabels = odict()
    # Skip header:
    # SUBSISTEMAS X SUBMERCADOS
    # NUM|NOME SSIS.| SUBM
    # XXX|XXXXXXXXXX|  XXX
    content = [x.decode('utf-8') for x in fobj]
    for i, v in enumerate(content[3:]):
        if v.strip() != '' and v.strip() != '999':
            cols = v.strip().split()
            subsis = cols[0].strip()
            label = cols[1].strip()
            submer = cols[2].strip()
            REE[subsis] = submer
            REElabels[subsis] = label
    return REE, REElabels
