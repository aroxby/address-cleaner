#!/usr/bin/env python
"""
Clean and format mailing addresses
"""
import sys
import re


def title_case(s):
    """
    Converts a string to title case without breaking on "'"s
    Taken from Python docs
    """
    def _title(match):
        return match.group(0)[0].upper() + match.group(0)[1:].lower()

    regex = r"[A-Za-z]+('[A-Za-z]+)?"
    return re.sub(regex, _title, s)


def clean(line):
    """
    Cleans a single line address
    """
    num_regexs = ['1st', '2nd', '3rd', r'\d+th']
    street_regexs = ['^street$', '^st$',  '^road$', '^rd$', '^drive$', '^dr$', '^avenue$', 'ave$']
    street_regexs += ['^place$', '^pl$', '^boulevard$', '^blvd$', '^court$', '^ct$', '^lane$', '^ln$']
    street_regexs += ['^way$', '^wy$', '^grove$', '^gr$', '^circle$', '^cr$']
    street_regexs += ['^trl$', '^broadyway$', '^center$']
    apt_regexs = ['^'+_+'$' for _ in num_regexs]
    apt_regexs += ['^apt$', '^unit$', '^#$', '^floor$', '^building$']
    zip_regexs = [r'^\d{5}([-\s]\d{4})?$']
    po_regexs = ['(p\W?o box )(\d+)']

    line = line.replace(',', ' ').replace('.', ' ').lower()
    parts = [_.strip() for _ in line.split() if _]  # Nonempty line portions
    arr = []  # Parsed address tokens
    idx = 0  # Array write index
    greedy = False  # Always grab the next part with parsing
    skip = False  # Always increase the index after the next section
    has_street = False  # Remember if we found a street
    has_appt = False  # Remember if we found an apartment
    has_zip = False  # Remember if we found a zip code
    has_po = False  # Remember if address is a PO box
    has_any = False  # Remember if the loop as run yet
    for part in parts:
        if has_zip:
            raise ValueError('Information after zip code \'{}\' for \'{}\''.format(part, line))
        if not greedy:
            if has_street:
                # We have to find a street before we can find an apartment
                for regex in apt_regexs:
                    if re.match(regex, part):
                        idx += 1
                        greedy = True
                        has_appt = True
            if has_any:
                for regex in zip_regexs:
                    if re.match(regex, part):
                        idx += 1
                        has_zip = True
            for regex in street_regexs:
                if re.match(regex, part):
                    skip = True
                    has_street = True
        else:
            greedy = False
            skip = True
        while idx >= len(arr):
            arr.append('')
        arr[idx] += '{} '.format(part)
        if skip:
            idx += 1
            skip = False
        has_any = True

    if not arr:
        raise ValueError('No address')

    for po_regex in po_regexs:
        arr[0], count = re.subn(po_regex, 'P.O. Box \\2,', arr[0], flags=re.IGNORECASE)
        if count > 0:
            arr = arr[0].split(',') + arr[1:]
            has_po = True

    if not has_street and not has_po:
        raise ValueError('Missing street name for \'{}\''.format(line.strip()))

    if not has_zip:
        raise ValueError('Missing zip code for \'{}\''.format(line.strip()))

    if len(arr) < 2:
        raise ValueError('Nothing before zip code for \'{}\''.format(line.strip()))

    arr = [_ for _ in arr if _]
    for idx in range(len(arr)):
        arr[idx] = title_case(arr[idx].strip())
        # All this just to fix .title() from producing things like (3Rd Floor)
        for regex in num_regexs:
            arr[idx] = re.sub(regex, lambda s: s[0].lower(), arr[idx], flags=re.IGNORECASE)

    assembled = ', '.join(_ for _ in arr)

    return assembled


def bulk_clean(inp, outp, errp=sys.stderr):
    """
    Cleans all lines of a file
    """
    for line in inp:
        try:
            cleaned = clean(line)
        except Exception as e:
            print(e, file=errp)
            print(line.strip(), file=outp)
        print(cleaned, file=outp)


def main(argv):
    """
    Program Entry Point
    """
    input_file = sys.stdin
    output_file = sys.stdout
    bulk_clean(input_file, output_file)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
