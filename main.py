#!/usr/bin/env python
"""
Clean and format mailing addresses
"""
import sys
import re


def clean(line):
    """
    Cleans a single line address
    """
    street_regexs = ['street$', 'st$',  'road$', 'rd$', 'drive$', 'dr$', 'avenue$', 'ave$']
    street_regexs += ['place$', 'pl$', 'boulevard$', 'blvd$']
    street_regexs += ['way$', 'grove$']
    num_regexs = ['^1st', '^2nd', '^3rd', r'^\d+th']
    apt_regexs = num_regexs + ['^apt', '^unit', '^#', 'floor', 'building']
    zip_regexs = [r'^\d{5}([-\s]\d{4})?$']

    line = line.replace(',', ' ').replace('.', ' ').lower()
    parts = [_ for _ in line.split() if _]  # Nonempty line portions
    arr = []  # Parsed address tokens
    idx = 0  # Array write index
    greedy = False  # Always grab the next part with parsing
    skip = False  # Always increase the index after the next section
    for part in parts:
        if not greedy:
            for regex in apt_regexs:
                if re.match(regex, part):
                    idx += 1
                    greedy = True
            for regex in zip_regexs:
                if re.match(regex, part):
                    idx += 1
            for regex in street_regexs:
                if re.match(regex, part):
                    skip = True
        else:
            greedy = False
            skip = True
        while idx >= len(arr):
            arr.append('')
        arr[idx] += '{} '.format(part)
        if skip:
            idx += 1
            skip = False

    arr = [_ for _ in arr if _]
    for idx in range(len(arr)):
        arr[idx] = arr[idx].strip().title()
        # All this just to fix .title() from producing things like (3Rd Floor)
        for regex in num_regexs:
            if re.match(regex, arr[idx], re.IGNORECASE):
                arr[idx] = arr[idx][0] + arr[idx][1].lower() + arr[idx][2:]

    assembled = ', '.join(_ for _ in arr)
    assembled.replace('Po Box', 'P.O. Box')
    return assembled


def bulk_clean(inp, outp, errp=sys.stderr):
    """
    Cleans all lines of a file
    """
    for line in inp:
        cleaned = clean(line)
        if cleaned:
            print(cleaned, file=outp)
        else:
            print("Invalid Address\n{}\n".format(line), file=errp)


def main(argv):
    """
    Program Entry Point
    """
    input_file = sys.stdin
    output_file = sys.stdout
    bulk_clean(input_file, output_file)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
