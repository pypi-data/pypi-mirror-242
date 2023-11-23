#!/usr/bin/env python


import os

###############################################################################


class Eikeskog(object):

    def __init__(self, s: str):
        self.s = s

    def return_s(self):
        return self.s

###############################################################################

def aa(x):
    return x

def bb():
    TEST = os.getenv("TEST")
    e = Eikeskog(TEST)
    x = e.return_s()
    print(x)
    return x


if __name__ == '__main__':
    x = aa("A")
    y = bb()
    print(x, y)
