#! /usr/bin/python3

from __future__ import print_function

"""
A quick Python script to output Eagle CAD commands for automation.
"""

def wireR(x1, y1, x2, y2):
    return "wire ({0} {1})({0} {3})({2} {3})({2} {1})({0} {1})".format(x1, y1, x2, y2)

