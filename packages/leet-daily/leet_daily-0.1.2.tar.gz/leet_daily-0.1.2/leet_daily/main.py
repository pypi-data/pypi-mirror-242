#!/usr/bin/env python3
"""This program sets up everything for the daily leetcode problems"""
from __future__ import annotations

import argparse
from typing import Sequence
import logging
from leet_daily.leet import Leet

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s [%(name)s Line:%(lineno)d] - %(message)s',
    level=logging.INFO,
)

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog='leet',
        description='leet helps with doing leetcode daily',
        epilog='Happy leetcoding'
    )
    parser.add_argument('-b', '--browser', action='store_false', help='do not open browser')
    parser.add_argument('-f', '--file', action='store_false', help='do not create a file')
    parser.add_argument('-e', '--editor', action='store_false', help='do not open editor')
    args = parser.parse_args(argv)

    leet = Leet()
    if args.file: leet.gen_leet_file()
    if args.browser: leet.open_in_browser()
    if args.editor: leet.open_in_editor()

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
