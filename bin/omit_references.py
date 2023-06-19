#!/usr/bin/env python3
import re

from panflute import *
from pathlib import Path


ACRONYMS_FILE = Path(__file__).parent.parent / "headers" / "acronyms.tex"
ACROYNMS = {}


def parse_acronyms():
    with ACRONYMS_FILE.open() as f:
        for line in f:
            if line.startswith(r'\acrodef{'):
                # Parse the line \acrodef{ide}[IDE]{integrated development environment}
                match = re.match(r'\\acrodef{(?P<label>[^}]+)}\[(?P<short>[^]]+)\]{(?P<long>[^}]+)}', line)
                if match:
                    label = match.group('label')
                    short = match.group('short')
                    long = match.group('long')

                    # Add the acronym to the list
                    ACROYNMS[label] = (short, long)



def omit_references(elem, doc):
    # Simplify the reference links
    if type(elem) == Link:
        # Merge all strings that are in content
        text = ''.join([x.text for x in elem.content if type(x) == Str])

        if '[' in text:
            text = 'X'  # TODO: Fix the number of lines, listings, and large figures

        return Str(text)

    # Replace acronyms
    elif type(elem) == Span:
        if elem.attributes and 'acronym-label' in elem.attributes:
            label = elem.attributes['acronym-label']
            form = elem.attributes['acronym-form']

            quantity, length = form.split('+')

            plural = quantity == 'plural'

            # Consider short, long, and full form
            short = ACROYNMS[label][0]
            long = ACROYNMS[label][1]

            if plural:
                if long.endswith('y'):
                    long = long[:-1] + 'ies'
                elif not long.endswith('s'):
                    long += 's'

                if short.endswith('S'):
                    short += 'es'
                else:
                    short += 's'

            if length == 'short':
                text = short
            elif length == 'long':
                text = long
            else:
                text = f'{long} ({short})'

            return Str(text)

    # Remove smallcaps
    elif type(elem) == SmallCaps:
        return Str(' '.join(map(lambda e: e.text, elem.content)))


def main(doc=None):
    parse_acronyms()

    return run_filter(omit_references, doc=doc)

if __name__ == "__main__":
    main()

