#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, ast, json, glob, platform, subprocess, random, requests, socket

# inc imports.
import syst3m, cl1
from fil3s import Files, Formats
from r3sponse import r3sponse

# source.
ALIAS = "netw0rk"
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=3)
OS = syst3m.defaults.check_operating_system(supported=["osx", "linux"])
syst3m.defaults.check_alias(alias=ALIAS, executable=f"{SOURCE_PATH}")

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

