#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'dminkovsky'

import argparse
import os.path
import sys
from utils import get_mutagen_id3

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('target', help="file from which to dump tag data")
    args = argparser.parse_args()

    file_path = os.path.abspath(args.target)
    try:
        print 'ID3 tag data in `{}`:\n'.format(file_path)
        id3 = get_mutagen_id3(file_path)
        print id3.pprint() + '\n'
        sys.exit(0)
    except IOError:
        print "Fatal Error: Cannot open {}.".format(file_path)
        sys.exit(255)