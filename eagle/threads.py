#!/usr/bin/python3

# Generate Eagle CAD commands for drawing threads as lines
# using thread pitch, width, length, etc.
#
#
# Example usage:
#   python3 threads.py  major_width     minor_width     "(startx, starty)"  length  pitch   [filename]

import sys
import math

class line():
    def __init__(self, start, stop):
        """'start' and 'stop' should be (x, y) pairs (tuples or lists)"""
        self.start = start
        self.stop = stop
        self.startx = start[0]
        self.starty = start[1]
        self.stopx = stop[0]
        self.stopy = stop[1]
        self.length = math.sqrt((self.stopx - self.startx)**2 + (self.stopy - self.starty)**2)

    def update(self, start, stop):
        self.start = start
        self.stop = stop
        self.startx = start[0]
        self.starty = start[1]
        self.stopx = stop[0]
        self.stopy = stop[1]

    def eaglestring(self):
        return "LINE ({:.3} {:.3}) ({:.3} {:.3})".format(self.startx, self.starty, self.stopx, self.stopy)

    def scale(self, newlength, update=False):
        #print("self.length = {:.4}\tnewlength = {:.4}".format(self.length, newlength))
        g = (self.length - newlength)/self.length
        #print("g = {:.4}".format(g))
        newStartx = self.startx + (self.stopx - self.startx)*g
        newStarty = self.starty + (self.stopy - self.starty)*g
        newStopx  = self.stopx  + (self.startx - self.stopx)*g
        newStopy  = self.stopy  + (self.starty - self.stopy)*g
        if update:
            self.update((newStartx, newStarty), (newStopx, newStopy))
        else:
            return "LINE ({:.3} {:.3}) ({:.3} {:.3})".format(newStartx, newStarty, newStopx, newStopy)

    def displace(self, dv, update=False):
        """dv = displacement vector = (dx, dy)"""
        newStartx = self.startx + dv[0]
        newStarty = self.starty + dv[1]
        newStopx  = self.stopx  + dv[0]
        newStopy  = self.stopy  + dv[1]
        if update:
            self.update((newStartx, newStarty), (newStopx, newStopy))
        else:
            return "LINE ({:.3} {:.3}) ({:.3} {:.3})".format(newStartx, newStarty, newStopx, newStopy)

def threads(major_width, minor_width, start, length, pitch):
    """
    start = (x, y) = bottom center of the threads part
    pitch = turns per unit length
    part extends in the Y axis from starty to start(y) + length
    major_width and minor_width describe the thread depth profile
    """
    full_threads = int(length * pitch)  # The number of complete threads (rounds down)
    x_center, y_center = start
    dx_major = major_width/2
    dx_minor = minor_width/2
    dy = 1/pitch
    w_diag = math.sqrt(minor_width**2 + dy**2)
    # Group the major and minor lines
    #print("dx_major = {:.4}\ndx_minor = {:.4}\ndy = {:.4}".format(dx_major, dx_minor, dy))
    #print("start = ({:.4}, {:.4})".format(start[0], start[1]))
    #print("w_diag = {}".format(w_diag))
    majorlines = []
    minorlines = []
    connectinglines = []
    for n in range(full_threads):
        startj = (x_center - dx_major, y_center + n*dy)
        stopj  = (x_center + dx_major, y_center + (n+0.5)*dy)
        minorline = line(startj, stopj)
        minorline.displace((0, 0.5*dy), update=True) # Displace vertically by dy/2
        minorline.scale(w_diag, update=True)
        majorlines.append(line(startj, stopj))
        minorlines.append(minorline)
    for n in range(len(majorlines)):
        # Now we want short connecting lines from start of major line n to start of minor line n
        # and minor line n to major line n+1
        connectinglines.append(line(majorlines[n].start, minorlines[n].start))
        connectinglines.append(line(majorlines[n].stop, minorlines[n].stop))
        if n + 1 < len(majorlines):
            connectinglines.append(line(minorlines[n].start, majorlines[n+1].start))
            connectinglines.append(line(minorlines[n].stop, majorlines[n+1].stop))
    linestrings = []
    for l in majorlines:
        linestrings.append(l.eaglestring())
    for l in minorlines:
        linestrings.append(l.eaglestring())
    for l in connectinglines:
        linestrings.append(l.eaglestring())
    return "\n".join(linestrings)

def parseTupleString(s):
    """Parse a string like '(x, y)' into the tuple (x, y)"""
    s = s.strip().strip('(').strip(')')     # Remove whitespace and enclosing parentheses
    x, y = s.split(',')
    x = float(x.strip())
    y = float(y.strip())
    return (x, y)

def write(msg, fd=None, nonl = False):
    if fd is None:
        print(msg.strip('\n'))
    else:
        if nonl:
            fd.write(msg)
        else:
            fd.write(msg + '\n')

def main():
    _fd = None
    if len(sys.argv) > 5:
        major_width = float(sys.argv[1])
        minor_width = float(sys.argv[2])
        start       = parseTupleString(sys.argv[3])
        length      = float(sys.argv[4])
        pitch       = float(sys.argv[5])
        if len(sys.argv) > 6:
            filename = sys.argv[6]
            try:
                _fd = open(filename, 'w')
            except IOError as ioe:
                print(ioe)
                _fd = None
        write(threads(major_width, minor_width, start, length, pitch), _fd)
        #threads(major_width, minor_width, start, length, pitch)
    elif len(sys.argv) > 1:
        s = parseTupleString(sys.argv[1])
        print("{} => {}".format(sys.argv[1], s))

if __name__ == "__main__":
    main()

