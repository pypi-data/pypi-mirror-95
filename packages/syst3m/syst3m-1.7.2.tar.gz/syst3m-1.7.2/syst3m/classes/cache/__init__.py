#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.classes.config import *
from syst3m.classes import objects

# the cache object class.
class Cache(objects.Object):
	def __init__(self, path=None):
		if path == None: path = f"{HOME}/.cache/"
		if not os.path.exists(path): os.mkdir(path)
		objects.Object.__init__(self)
		self.assign({
			"path":path,
		})
	def set(self, data=None, group=None, id=None, format="str"):
		if id == None:
			data_path = f"{self.path}/{group}"
		else:
			data_path = f"{self.path}/{group}/"+id.replace("/", "\\")
		base = Formats.FilePath(data_path).base()
		if not os.path.exists(base): os.system(f"mkdir -p {base}")
		if format in [str, "str", "string", int, float, "int", "integer", "float", "double"]:
			Files.save(data_path, str(data), format="str")
		elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
			Files.save(data_path, str(data), format="json")
		else:
			raise ValueError(f"Unkown format: {format}.")
	def get(self, group=None, id=None, format="str"):
		if id == None:
			data_path = f"{self.path}/{group}"
		else:
			data_path = f"{self.path}/{group}/"+id.replace("/", "\\")
		base = Formats.FilePath(data_path).base()
		if not os.path.exists(base): os.system(f"mkdir -p {base}")
		def load():
			if format in [str, "str", "string"]:
				return Files.load(data_path, format="str")
			elif format in [int, "int", "integer"]:
				return int(Files.load(data_path, format="str"))
			elif format in [float, "float", "double"]:
				return float(Files.load(data_path, format="str"))
			elif format in [dict, list, "dict", "dictionary", "list", "array", "json"]:
				return Files.load(data_path, format="json")
			else:
				raise ValueError(f"Unkown format: {format}.")
		try:
			loaded = load()
		except FileNotFoundError:
			self.set(id=id, data="None", group=group, format=format)
			loaded = load()
		if loaded in ["None","none","null"]: loaded = None
		return loaded


# the default cache.
cache = Cache()

# the webserver cache object class.
class WebServer(objects.Thread):
	def __init__(self,
		id="webserver",
		host="127.0.0.1",
		port=52379,
		path=None,
		default={},
		# do not use.
		serialized={},
	):
		objects.Thread.__init__(self)
		self.__cache__ = Cache(path=path)
		self.default = dict(default)
		self.assign({
			"sleeptime":3,
			"id":id,
			"host":host,
			"port":port,
			"cache":default,
		})
		self.assign(serialized)
		self.id = id.replace(" ","-")
		self.tag = self.id.replace(" ","_")
	def set(self, group=None, id=None, data=None):
		encoded = urllib.parse.urlencode({
			"group":group,
			"id":id,
			"data":data,
			"token":self.token(),
			"cache":self.__cache__.path,
			"cache_id":self.id,
		})
		try:
			response = requests.get(f'http://{self.host}:{self.port}/set?{encoded}')
		except Exception as e:
			return r3sponse.error_response(f"Failed to connect with {self.host}:{self.port}, error: {e}")
		try:
			response = self.__serialize__(response.json())
		except:
			return r3sponse.error_response(f"Failed to serialize {response}: {response.text}")
		return r3sponse.safe_response(response)
	def get(self, group=None, id=None):
		encoded = urllib.parse.urlencode({
			"group":group,
			"id":id,
			"token":self.token(),
			"cache":self.__cache__.path,
			"cache_id":self.id,
		})
		try:
			response = requests.get(f'http://{self.host}:{self.port}/get?{encoded}')
		except Exception as e:
			return r3sponse.error_response(f"Failed to connect with {self.host}:{self.port}, error: {e}")
		try:
			response = self.__serialize__(response.json())
		except:
			return r3sponse.error_response(f"Failed to serialize {response}: {response.text}")
		return r3sponse.safe_response(response)
	def app(self):
		app = flask.Flask(__name__)
		cli = sys.modules['flask.cli']
		cli.show_server_banner = lambda *x: None
		@app.route('/get')
		def get():
			token = flask.request.args.get('token')
			if token != Cache(path=flask.request.args.get('cache')).get(flask.request.args.get('cache_id'), id="token"):
				return r3sponse.error_response(f"Provided an invalid token {token}.").json()
			group = flask.request.args.get('group')
			id = flask.request.args.get('id')
			if id in ["none", "null", "None"]: id = None
			try:
				if id == None:
					tag = f"{group}"
					value = self.cache[group]
				else:
					tag = f"{group}:{id}"
					value = self.cache[group][id]
			except KeyError:
				return r3sponse.error_response(f"There is no data cached for {tag}.").json()
			return r3sponse.success_response(f"Successfully retrieved {tag}.", {
				"group":group,
				"id":id,
				"data":value,
			}).json()
		@app.route('/set')
		def set():
			token = flask.request.args.get('token')
			if token != Cache(path=flask.request.args.get('cache')).get(flask.request.args.get('cache_id'), id="token"):
				return r3sponse.error_response(f"Provided an invalid token {token}.").json()
			group = flask.request.args.get('group')
			id = flask.request.args.get('id')
			if id in ["none", "null", "None"]: id = None
			value = flask.request.args.get('data')
			if id == None:
				tag = f"{group}"
				self.cache[group] = value
			else:
				tag = f"{group}:{id}"
				try: self.cache[group]
				except KeyError: self.cache[group] = {}
				self.cache[group][id] = value
			return r3sponse.success_response(f"Successfully cached {tag}.").json()
		@app.route('/active')
		def active():
			token = flask.request.args.get('token')
			if token != Cache(path=flask.request.args.get('cache')).get(flask.request.args.get('cache_id'), id="token"):
				return r3sponse.error_response(f"Provided an invalid token {token}.").json()
			return r3sponse.success_response(f"Active.").json()
		#def run__(self, app, host, port):
		#	app.run(host=host, port=port)
		#self.process = multiprocessing.Process(target=app.run, args=(self, app, self.host,self.port,))
		#self.process.start()
		app.run(host=self.host, port=self.port)
	def token(self):
		if random.randrange(1, 100) <= 5: 
			self.__cache__.set(group=self.id, id="token", data=Formats.String("").generate(length=64, digits=True, capitalize=True))
		return self.__cache__.get(group=self.id, id="token")
	def running(self):
		encoded = urllib.parse.urlencode({
			"token":self.token(),
			"cache":self.__cache__.path,
			"cache_id":self.id,
		})
		try:
			requests.get(f'http://{self.host}:{self.port}/active?{encoded}')
			return True
		except requests.exceptions.ConnectionError:
			return False
	def run(self):
		self.__cache__.set(group=self.id, id="daemon", data="*running*")
		self.__cache__.set(group=self.id, id="token", data=Formats.String("").generate(length=64, digits=True, capitalize=True))
		self.app()
		self.__cache__.set(group=self.id, id="daemon", data="*stopped*")
	def fork(self):
		print(f"Starting the {self.id}.")
		serialized = self.dict()
		cache = self["cache"]
		for i in ["__cache__","cache",]:
			del serialized[i]
		serialized["path"] = cache.path
		print(f"python3 {SOURCE_PATH}classes/cache/fork.py --serialized '{serialized}' --syst3m-webserver-tag {self.tag}")
		p = subprocess.Popen(["python3", f"{SOURCE_PATH}classes/cache/fork.py", "--serialized", f"'{serialized}'", "--syst3m-webserver-tag", {self.tag}])#, "2>", "/dev/null"])
		time.sleep(3)
	def stop(self):
		if not self.running(): 
			return r3sponse.error_response(f"The {self.id} is not running.")
		processes = syst3m.processes(includes=f"--syst3m-webserver-tag {self.tag}")
		if not processes.success: return response
		if len(processes.processes) <= 1:
			return r3sponse.error_response(f"Unable to find the pid of the {self.id}.")
		for pid, info in processes.processes.items():
			if info["process"] not in ["grep"]:
				response = syst3m.kill(pid=pid)
				if not response.success: return response
		return r3sponse.error_response(f"Successfully stopped the {self.id}.")
	def __serialize__(self, dict):
		for key in list(dict.keys()):
			value = dict[key]
			if value in ["False", "false"]: dict[key] = False
			elif value in ["True", "true"]: dict[key] = True
			elif value in ["None", "none", "null", "nan"]: dict[key] = None
			else:
				try: 
					int(value)
					dict[key] = int(value)
				except: a=1
		return dict
	#def stop(self):
	#	self.process.terminate()
	#	self.process.join()
