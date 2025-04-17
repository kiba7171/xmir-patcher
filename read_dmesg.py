#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import platform

import xmir_base
import gateway
from gateway import die


gw = gateway.Gateway()

fn_old    = 'outdir/dmesg_old.txt'
fn_local  = 'outdir/dmesg.txt'
fn_remote = '/tmp/dmesg.txt'

if os.path.exists(fn_local): 
    if os.path.exists(fn_old):
        os.remove(fn_old)
    os.rename(fn_local, fn_old)

print("Send command...")
try:
    gw.run_cmd("dmesg > " + fn_remote)
    print("File {} created!".format(fn_remote))

    print("Downloading data to a computer...")
    gw.download(fn_remote, fn_local)

    gw.run_cmd("rm -f " + fn_remote)

    with open(fn_local, "r", encoding='utf-8', errors='replace') as file:
        data = file.read()
    with open(fn_local, "w", encoding='utf-8') as file:
        file.write(data)

    print("Kernel logs written to file {}".format(fn_local))
except Exception as e:
    print(f"Error processing dmesg: {str(e)}")

fn_old    = 'outdir/syslog_old.txt'
fn_local  = 'outdir/syslog.txt'
fn_remote = '/tmp/syslog.txt'
if os.path.exists(fn_local): 
    if os.path.exists(fn_old):
        os.remove(fn_old)
    os.rename(fn_local, fn_old)

try:
    gw.run_cmd("cat /data/usr/log/messages /tmp/messages > " + fn_remote)
    gw.download(fn_remote, fn_local)
    gw.run_cmd("rm -f " + fn_remote)

    with open(fn_local, "r", encoding='utf-8', errors='replace') as file:
        data = file.read()
    with open(fn_local, "w", encoding='utf-8') as file:
        file.write(data)

    print("System logs are written to a file {}".format(fn_local))
except Exception as e:
    print(f"Error processing syslog: {str(e)}")
