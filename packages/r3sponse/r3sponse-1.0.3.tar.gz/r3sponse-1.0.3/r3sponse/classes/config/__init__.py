#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, requests, ast, json, pathlib, glob, platform, subprocess, random

# inc imports.
from fil3s import Files, Formats
import syst3m

# source.
ALIAS = "r3sponse"
SOURCE_NAME = "r3sponse"
VERSION = "v1"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=4)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
#syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}/{VERSION}/")

# universal variables.
OWNER = os.environ.get("USER")
GROUP = "root"
HOME_BASE = "/home/"
HOME = f"/home/{os.environ.get('USER')}/"
MEDIA = f"/media/{os.environ.get('USER')}/"
if OS in ["osx"]: 
	HOME_BASE = "/Users/"
	HOME = f"/Users/{os.environ.get('USER')}/"
	MEDIA = f"/Volumes/"
	GROUP = "wheel"
