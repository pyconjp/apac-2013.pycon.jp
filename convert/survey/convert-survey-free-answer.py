# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
import io
import csv

def convert(src_filename, out_filename):
    out = io.open(out_filename, 'wt', encoding='utf-8')
    for row in csv.reader(open(src_filename, 'rt', encoding='utf-8')):
        txt = ' '.join(x.strip() for x in row[1].splitlines())
        if txt:
            out.write('* {0}\n'.format(txt))
    out.close()


def main():
    src_filename = sys.argv[1]
    out_filename = os.path.splitext(src_filename)[0] + '.in'
    convert(src_filename, out_filename)


if __name__ == '__main__':
    main()
