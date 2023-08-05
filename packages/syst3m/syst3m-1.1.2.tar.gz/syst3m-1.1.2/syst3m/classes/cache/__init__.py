#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import objects

# the cache object class.
class Cache(objects.Thread):
	def __init__(self, path=None):
		if path == None: path = f"{HOME}/.cache/"
		if not os.path.exists(path): os.mkdir(path)
		objects.Thread.__init__(self)
		self.assign({
			"path":path,
		})
	def set(self, value=None, group=None, id=None, format="str"):
		if id == None:
			value_path = f"{self.path}/{group}"
		else:
			value_path = f"{self.path}/{group}/"+id.replace("/", "\\")
			base = Formats.FilePath(value_path).base()
			if not os.path.exists(base): os.system(f"mkdir {value_path}")
		if format in [str, "str", "string", int, float, "int", "integer", "float", "double"]:
			Files.save(value_path, str(value), format="str")
		elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
			Files.save(value_path, str(value), format="json")
		else:
			raise ValueError(f"Unkown format: {format}.")
	def get(self, group=None, id=None, format="str"):
		if id == None:
			value_path = f"{self.path}/{group}"
		else:
			value_path = f"{self.path}/{group}/"+id.replace("/", "\\")
			base = Formats.FilePath(value_path).base()
			if not os.path.exists(base): os.system(f"mkdir {value_path}")
		def load():
			if format in [str, "str", "string"]:
				return Files.load(value_path, format="str")
			elif format in [int, "int", "integer"]:
				return int(Files.load(value_path, format="str"))
			elif format in [float, "float", "double"]:
				return float(Files.load(value_path, format="str"))
			elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
				return Files.load(value_path, format="json")
			else:
				raise ValueError(f"Unkown format: {format}.")
		try:
			loaded = load()
		except FileNotFoundError:
			self.set(id=id, value="None", group=group, format=format)
			loaded = load()
		if loaded in ["None","none","null"]: loaded = None
		return loaded
