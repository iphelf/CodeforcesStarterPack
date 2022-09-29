#!/usr/bin/env python3

import subprocess as sp
from sys import argv
from codecs import open

encoding = 'utf-8'


def main():
    assert len(argv) >= 4
    pathTestee = argv[1]
    pathTestInput = argv[2]
    pathTestOracle = argv[3]

    testOutput = sp.run(
        [pathTestee],
        stdin=open(pathTestInput, 'r', encoding),
        stdout=sp.PIPE
    ).stdout.decode(encoding).rstrip()

    testOracle = open(pathTestOracle, 'r', encoding).read().rstrip()

    if testOutput == testOracle:
        print("[==> Accepted <==]")
        exit(0)
    else:
        print("[==> Wrong Answer <==]")
        print("Expected:")
        print(testOracle)
        print()
        print("Found:")
        print(testOutput)
        exit(1)


if __name__ == '__main__':
    main()
