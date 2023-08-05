#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.v1.classes.config import *
from syst3m.v1.classes import objects

# the cache object class.
class Cache(objects.Thread):
	def __init__(self, path=None):
		if path == None: path = f"{HOME}/.cache/"
		if not os.path.exists(path): os.mkdir(path)
		objects.Thread.__init__(self)
		self.assign({
			"path":path,
		})
	def set(self, status=None, type=None, id=None):
		if id == None:
			status_path = f"{self.path}/{type}"
		else:
			status_path = f"{self.path}/{type}/"+id.replace("/", "\\")
			base = Formats.FilePath(status_path).base()
			if not os.path.exists(base): os.system(f"mkdir {status_path}")
		Files.save(status_path, status, format="str")
	def get(self, type=None, id=None):
		if id == None:
			status_path = f"{self.path}/{type}"
		else:
			status_path = f"{self.path}/{type}/"+id.replace("/", "\\")
			base = Formats.FilePath(status_path).base()
			if not os.path.exists(base): os.system(f"mkdir {status_path}")
		try:
			return Files.load(status_path, format="str")
		except FileNotFoundError:
			self.set(id=id, status="none", type=type)
			return Files.load(status_path, format="str")
