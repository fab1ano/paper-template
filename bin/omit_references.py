#!/usr/bin/env python3
from pprint import pprint

from panflute import *


def omit_references(elem, doc):
    if type(elem) == Link:
        # Merge all strings that are in content
        text = ''.join([x.text for x in elem.content if type(x) == Str])

        if '[' in text:
            text = 'X'  # TODO: Fix the number of lines, listings, and large figures

        return Str(text)
    # TODO: acronyms


def main(doc=None):
    return run_filter(omit_references, doc=doc)

if __name__ == "__main__":
    main()

