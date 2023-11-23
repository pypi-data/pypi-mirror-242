# -*- coding: utf-8 -*-
import sys

from dding.notify import notify_dding


def main():
    group = 'default'
    if len(sys.argv) == 1:
        usage()
        sys.exit(1)

    if len(sys.argv) > 2:
        _, group, content = sys.argv
    else:
        content = sys.argv[1]
    notify_dding(group, content)


def usage():
    print("usage: dding group=[custom name] contenet=hello")
    print("example: dding helloworld")


if __name__ == '__main__':
    main()
