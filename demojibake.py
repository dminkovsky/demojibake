#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'dminkovsky'

import argparse
import codecs
import os
import sys
from utils import get_mutagen_id3, get_files
# from chardet import detect

mojibaked_frames = {
    'TALB': {
        'description': 'Album',
        'weight': 3
    },
    'TPE1': {
        'description': 'Artist',
        'weight': 2
    },
    'TIT2': {
        'description': 'Title',
        'weight': 1
    },
    'COMM': {
        'description': 'Comment',
        'weight': 4
    }
}

def demojibake(file_path, wrong, right, commit=True):
    id3 = get_mutagen_id3(file_path)

    for encoding in (wrong, right):
        # Throws a LookupError, must be handled in calling code
        codecs.lookup(encoding)

    results = {}
    for frame in id3.itervalues():
        if frame.FrameID not in mojibaked_frames.keys():
            continue

        results[frame.FrameID] = []
        results[frame.FrameID].append(frame.text[0])
        try:
            frame.text[0] = frame.text[0].encode(wrong).decode(right)
            frame.encoding = 3
            results[frame.FrameID].append(frame.text[0])
        except:
            pass

    if commit:
        id3.save()

    return results

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('wrong_encoding', help="specify the wrong (incorrect) encoding that is currently in place")
    argparser.add_argument('right_encoding', help="specify the right (correct) desired encoding")
    argparser.add_argument('-d', '--dry-run', help="dry run: do not save changes (default: save changes)", action="store_true", default=False)
    argparser.add_argument('-i', '--interactive', help="interactive: display changes and prompt to continue after each file (default: non-interactive)", action="store_true", default=False)
    argparser.add_argument('-r', '--recurse', help="recurse through subdirectories of the root directory (default: do not recurse)", action="store_true", default=False)
    args = argparser.parse_args()

    for file_path in get_files(os.getcwd(), args.recurse):
        print '\nDemojibaking `{}`:'.format(file_path)

        try:
            commit = not args.dry_run
            results = demojibake(file_path, args.wrong_encoding, args.right_encoding, commit)

            for FrameID in sorted(mojibaked_frames, cmp=lambda x,y: cmp(mojibaked_frames[x]['weight'], mojibaked_frames[y]['weight'])):
                before = results[FrameID][0]
                try:
                    # results[FrameID][1] may not be set if demojibaking failed
                    after = results[FrameID][1]
                except:
                    after = before

                print u'{:>10}'.format(mojibaked_frames[FrameID]['description'])
                print u'{:>20}: {}'.format('Before', before)
                print u'{:>20}: {}'.format('After', after)

            if args.interactive:
                raw_input("Next file...")

        except LookupError as e:
            print "Fatal Error: {} is not compatible with this program.".format(e.message)
            sys.exit(255)