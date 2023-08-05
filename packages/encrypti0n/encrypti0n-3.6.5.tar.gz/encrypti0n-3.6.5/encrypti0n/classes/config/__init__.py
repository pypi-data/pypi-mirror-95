#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, random
import syst3m, cl1
from r3sponse import r3sponse
from fil3s import Files, Formats

# source.
ALIAS = "encrypti0n"
SOURCE_NAME = "encrypti0n"
VERSION = "v1"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=4)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}/{VERSION}/", sudo=True)

# file settings.
ADMINISTRATOR = "administrator"
OWNER = os.environ.get("USER")
GROUP = "root"
if OS in ["osx"]: GROUP = "wheel"
SUDO = True
ADMIN_PERMISSION = 700
READ_PERMISSION = 750
WRITE_PERMISSION = 770

