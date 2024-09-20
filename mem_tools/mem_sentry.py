#!/usr/bin/env python

# Description:
# monitor system memory usage, capture the memory usage and write to 
# log file while the memory usage is above the threshold

# update:
# 2024-09-19     Initial release
import io
import os
import sys
import time
import subprocess
import argparse
import datetime
import logging
from logging.handlers import RotatingFileHandler

PAGESIZE = os.sysconf("SC_PAGE_SIZE") / 1024

class Proc:
    def __init__(self):
        uname = os.uname()
        if uname[0] == "FreeBSD":
            self.proc = '/compat/linux/proc'
        else:
            self.proc = '/proc'

    def path(self, *args):
        return os.path.join(self.proc, *(str(a) for a in args))

    def open(self, *args):
        try:
            if sys.version_info < (3,):
                return open(self.path(*args))
            else:
                return open(self.path(*args), errors='ignore')
        except (IOError, OSError):
            if type(args[0]) is not int:
                raise
            val = sys.exc_info()[1]
            if (val.errno == errno.ENOENT or # kernel thread or process gone
                val.errno == errno.EPERM or
                val.errno == errno.EACCES):
                raise LookupError
            raise

proc = Proc()

def get_mem_free():
    mem_info = {}
    try:
        mem_info = proc.open('meminfo').readlines()
    except IOError as e:
        pass
    
    for line in mem_info:
        if line.startswith("MemFree:"):
            free_kb = int(line.split()[1])
            return free_kb

def setup_logger(path='./'):
    if not os.path.exists(path):
        os.mkdir(path)
    log_name = "mem_sentry_" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + ".log"
    full_name = os.path.join(path, log_name)
    logger = logging.getLogger(full_name)
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(full_name, maxBytes=1024*1024*10, backupCount=3, encoding='utf-8')
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

def get_args():
    help_msg = 'Capture memory usage of processes'
    parser = argparse.ArgumentParser(prog='mem_sentry', description=help_msg)
    parser.add_argument(
        '-t', '--threshold',
        dest='thd',
        default=200,
        help='Threshold trigger capture, in MB',
    )
    parser.add_argument(
        '-out_path', '--output',
        dest='out_path',
        default='./',
        help='Output to file',
    )
    return parser.parse_args()

def main(args):
    car_thd = int(args.thd) * 1024
    log_path = args.out_path
    logger = setup_logger(log_path)

    curr_free = get_mem_free()
    try:
        sentry = True
        while sentry:
            try:
                free_kb = get_mem_free()
            except RuntimeError:
                continue
        
            if abs(curr_free - free_kb) > car_thd:
                curr_free = free_kb
                # capture
                output = subprocess.check_output('top -b -o %MEM -d1 -n2', shell=True)
                logger.info(output.decode('utf-8'))
            time.sleep(1)

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    args = get_args()
    main(args)
