# -*- coding: utf-8 -*-
"""
gpssnr_cl.py
command line python code to run gpssnr (fortran) translator 
kristine larson
"""
import argparse
import os
import sys
from numpy import array
# this is the fortran code KL wrote 
import gpssnrpy.gpssnr as gpssnr
import time



def binary(string):
    """
    changes python string to bytes for use in
    fortran code using f2py via numpy
    input is a string, output is bytes with null at the end
    """
    j=bytes(string,'ascii') + b'\0\0'

    return array(j)


def main():
    """
    command line interface for running gpssnr from python
    inputs are the three filenames (input obs, output obs, navigation file), snr choice, and decimation
    if decimation is zero, then no decimation is done
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("rinex", help="rinexname", type=str)
    parser.add_argument("output", help="outputfile", type=str)
    parser.add_argument("nav", help="navfile", type=str)
    parser.add_argument("filetype",   help="e.g. 50, 66, 88, 99", type=str)
    parser.add_argument("-dec", default=None,help="decimation factor in seconds. default is none", type=str)

    args = parser.parse_args()

#   assign inputs to normal variable names
    rinexfile = args.rinex 
    snrname = args.output
    orbit = args.nav 
    snrtype = args.filetype

    if args.dec == None:
        dec = '0'
    else:
        dec = args.dec

    # these are allowed choices
    if snrtype not in ['99', '66','50','88']:
        print('Illegal snrtype choice',  snrtype)
        sys.exit()

    # check that inputs exist before calling code
    if os.path.isfile(rinexfile) and os.path.isfile(orbit):
        in1 = binary(rinexfile); in2 = binary(snrname);
        in3 = binary(orbit); in4 = binary(snrtype)
        in5= binary(dec)
        t1 = time.time()
        gpssnr.foo(in1,in2,in3,in4,in5)
        t2 = time.time()
        if os.path.isfile(snrname):
            print('SUCCESS: SNR file created',snrname, ' Exec time:', '{0:4.2f}'.format(t2-t1))
    else:
        if not os.path.isfile(rinexfile):
            print('RINEX file does not exist', rinexfile)
        if not os.path.isfile(orbit):
            print('Orbit file does not exist', orbit)
        sys.exit()


if __name__ == "__main__":
    main()
