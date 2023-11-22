# Author: Shine Jayakumar
# https://github.com/shine-jayakumar/splich
#
# MIT License

# Copyright (c) 2022 Shine Jayakumar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Adapted by frantzme@vt.edu

import os
import glob
import argparse
import hashlib
from datetime import datetime
from configparser import ConfigParser
import sys

#VERSION = 'v.1.4'

VERBOSE = False


def file_split(file, parts=None, chunk_size=None, delete_original=False, generate_hashfile=True, generate_config=True):
    '''
    Splits files into parts, or in chunk_size
    '''
    files_out = []

    if not file:
        return files_out
    if not parts and not chunk_size:
        return files_out

    fsize = os.path.getsize(file)
    
    if chunk_size and chunk_size > fsize:
        raise ValueError('Chunk size cannot be greater than file size')

    vvprint('Source file: {0}'.format(file))
    vvprint('Size: {0}'.format(fsize))

    segment_size = 0

    if parts:
        segment_size = fsize // parts
    else:
        segment_size = chunk_size
    
    if segment_size < 1:
        raise ValueError('At least 1 byte required per part')

    vvprint('Segment Size: {0}'.format(segment_size))

    fdir, fname = os.path.split(file)
    # fname = fname.split('.')[0]
    fname = os.path.splitext(fname)[0]
    
    if generate_hashfile:
        vvprint('Generating hash')
        hash = gethash(file)
        start_time = datetime.today().strftime("%m%d%Y_%H%M")

        vvprint('Hash: {0}\n\n'.format(hash))

    vvprint('Reading file: {0}'.format(file))

    with open(file,'rb') as fh:
        fpart = 1
        while fh.tell() != fsize:
            if parts:
                # check if this is the last part
                if fpart == parts:
                    # size of the file - wherever the file pointer is
                    # the last part would contain segment_size + whatever is left of the file
                    segment_size = fsize - fh.tell()

            chunk = fh.read(segment_size)
            part_filename = os.path.join(fdir, '{0}_{1}_{2}.zip'.format(fname, start_time, fpart))
            vvprint('{0} Segment size: {1} bytes'.format(part_filename, segment_size))
            files_out += [part_filename]
            with open(part_filename, 'wb') as chunk_fh:
                chunk_fh.write(chunk)
            fpart += 1

        if generate_hashfile:
        # hashfile generation
            hashfilename = '{0}_hash_{1}.hash'.format(fname, start_time)
            files_out += [hashfilename]
            hashfile_path = os.path.join(fdir, hashfilename)
            vvprint('Hashfile: {0}'.format(hashfile_path))
            with open(hashfile_path, 'w') as hashfile:
                hashfile.write(hash)

        if generate_config:
            # auto-stitch config file generation
            vvprint('Generating auto-stitch config file')
            if generate_stitch_config(filename=file, hashfile=hashfilename):
                vvprint('Saved stitch.ini')
                files_out += ["stitch.ini"]
            else:
                vvprint('Could not create auto-stitch config. Stitch files manually.')

    if delete_original:
        try:os.remove(file)
        except:pass
    
    return files_out

def file_stitch(file, outfile=None, hashfile=None):
    '''
    Stitches the parts together
    '''
    # d:\\somedir\\somefile.txt to 
    # d:\\somedir and somefile.txt

    if not file:
        return False

    fdir, fname = os.path.split(file)
    # fname = fname.split('.')[0]
    fname = os.path.splitext(fname)[0]
    
    file_parts = glob.glob(os.path.join(fdir,  '{0}_*.zip'.format(fname)))
    file_parts = sort_file_parts(file_parts)
    
    if not file_parts:
        raise FileNotFoundError('Split files not found')

    if outfile:
        # if just the filename
        if os.path.split(outfile)[0] == '':
            # create the file in input dir (fdir)
            outfile = os.path.join(fdir, outfile)
    
    write_out = outfile or file
    vvprint('Output: {0}'.format(write_out))

    with open(write_out, 'wb') as fh:
        for filename in file_parts:
            buffer = b''
            vvprint('Reading {0}'.format(filename))
            with open(filename, 'rb') as prt_fh:
                buffer = prt_fh.read()
                fh.write(buffer)

    vvprint('Written {0} bytes'.format(os.path.getsize(write_out)))
    
    if hashfile:
        print('Verifying hash')
        if checkhash(outfile or file, hashfile):
            print('Hash verified')
            return write_out
        else:
            print('Hash verification failed')
            return None
    
    return write_out


def file_stitch_by_ini(config_file='stitch.ini', clean_on_verify=True):  
    config = ConfigParser()
    config.read(config_file)
    fname = config.get('stitch', 'filename')
    hashfile = config.get('stitch', 'hashfile')
    verbose = config.getboolean('settings', 'verbose')

    if file_stitch(file=fname, outfile=fname, hashfile=hashfile):
        vvprint("Successfully stitched together")

        fdir, ffname = os.path.split(fname)
        # fname = fname.split('.')[0]
        ffname = os.path.splitext(ffname)[0]
        
        file_parts = glob.glob(os.path.join(fdir,  '{0}_*.zip'.format(ffname)))
        file_parts.extend([config_file, hashfile])

        if clean_on_verify:
            for file in file_parts:
                try:os.remove(file)
                except:pass
        return True
    return False


def gethash(file):
    '''
    Returns the hash of file
    '''
    hash = None
    with open(file, 'rb') as fh:
        hash = hashlib.sha256(fh.read()).hexdigest()
    return hash


def checkhash(file, hashfile):
    '''
    Compares hash of a file with original hash read from a file
    '''
    curhash = None
    orghash = None
    curhash = gethash(file)
    with open(hashfile, 'r') as fh:
        orghash = fh.read()

    return curhash == orghash
    

def vvprint(text):
    '''
    print function to function only when verbose mode is on
    '''
    global VERBOSE
    if VERBOSE:
        print(text)


def getpartno(filepart):
    '''
    Returns the part number from a part filename
    Ex: flask_05112022_1048_3.zip -> 3
    '''
    return int(filepart.split('_')[-1].split('.')[0])


def sort_file_parts(file_part_list):
    '''
    Returns a sorted list of part filenames based on the part number
    Ex: ['flask_05112022_1048_3.zip', 'flask_05112022_1048_1.zip', 'flask_05112022_1048_2.zip'] ->
        ['flask_05112022_1048_1.zip', 'flask_05112022_1048_2.zip', 'flask_05112022_1048_3.zip']
    '''
    # creates list of (prt_no, part)
    fparts = [(getpartno(prt), prt) for prt in file_part_list]
    fparts.sort(key=lambda x: x[0])
    fparts = [prt[1] for prt in fparts]
    return fparts
        

def generate_stitch_config(filename, hashfile):
    '''
    Generates auto-stitch config file
    '''
    try:
        with open('stitch.ini', 'w') as configfile:
            config = ConfigParser()
            config.add_section('stitch')
            config.set('stitch', 'filename', filename)
            config.set('stitch', 'hashfile', hashfile)

            config.add_section('settings')
            config.set('settings', 'verbose', 'True')
            config.write(configfile)
    except Exception as ex:
        print('Error while creating auto-stitch config file: {0}'.format(str(ex)))
        stitch_config_path = os.path.join(os.getcwd(), 'stitch.ini')
        if os.path.exists(stitch_config_path):
            os.remove(stitch_config_path)
        return False
    return True
