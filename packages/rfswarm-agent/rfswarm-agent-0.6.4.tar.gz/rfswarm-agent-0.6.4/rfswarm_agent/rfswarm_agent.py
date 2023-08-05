#!/usr/bin/python
#
#	Robot Framework Swarm
#
#    Version 0.6.4
#


# https://stackoverflow.com/questions/48090535/csv-file-reading-and-find-the-value-from-nth-column-using-robot-framework

import sys
import os
import platform
import tempfile
import configparser

import hashlib
import lzma
import base64



# import robot
import pkg_resources
import random
import time
from datetime import datetime
import threading
import subprocess
import requests
import psutil
# import platform
import socket
import json
import xml.etree.ElementTree as ET
import shutil

import argparse
import inspect


class RFSwarmAgent():

	version="0.6.4"
	config = None
	isconnected = False
	isrunning = False
	isstopping = False
	run_name = None
	swarmmanager = None
	agentdir = None
	scriptdir = None
	logdir = None
	agentini = None
	listenerfile = None
	ipaddresslist = []
	agentname = None
	agentproperties = {}
	netpct = 0
	mainloopinterval = 10
	scriptlist = {}
	jobs = {}
	upload_queue = []
	robotcount = 0
	status = "Ready"
	excludelibraries = []
	args = None
	xmlmode = False
	timeout=600

	debuglvl = 0

	def __init__(self, master=None):
		self.debugmsg(0, "Robot Framework Swarm: Run Agent")
		self.debugmsg(0, "	Version", self.version)
		self.agentproperties["RFSwarmAgent: Version"] = self.version
		self.debugmsg(6, "__init__")
		self.debugmsg(6, "gettempdir", tempfile.gettempdir())
		self.debugmsg(6, "tempdir", tempfile.tempdir)

		parser = argparse.ArgumentParser()
		parser.add_argument('-g', '--debug', help='Set debug level, default level is 0')
		parser.add_argument('-v', '--version', help='Display the version and exit', action='store_true')
		parser.add_argument('-i', '--ini', help='path to alternate ini file')
		parser.add_argument('-m', '--manager', help='The manager to connect to e.g. http://localhost:8138/')
		parser.add_argument('-d', '--agentdir', help='The directory the agent should use for files')
		parser.add_argument('-r', '--robot', help='The robot framework executable')
		parser.add_argument('-x', '--xmlmode', help='XML Mode, fall back to pasing the output.xml after each iteration', action='store_true')
		parser.add_argument('-a', '--agentname', help='Set agent name')
		parser.add_argument('-p', '--property', help='Add a custom property, if multiple properties are required use this argument for each property e.g. -p property1 -p "Property 2"', action='append')
		self.args = parser.parse_args()

		self.debugmsg(6, "self.args: ", self.args)

		if self.args.debug:
			self.debuglvl = int(self.args.debug)


		if self.args.version:
			exit()


		self.config = configparser.ConfigParser()
		scrdir = os.path.dirname(__file__)
		self.debugmsg(6, "scrdir: ", scrdir)
		self.agentini = os.path.join(scrdir, "RFSwarmAgent.ini")

		if self.args.ini:
			self.debugmsg(1, "self.args.ini: ", self.args.ini)
			self.agentini = self.args.ini

		if os.path.isfile(self.agentini):
			self.debugmsg(6, "agentini: ", self.agentini)
			self.config.read(self.agentini)
		else:
			self.saveini()

		self.debugmsg(0, "	Configuration File: ", self.agentini)

		self.agentname = socket.gethostname()
		if self.args.agentname:
			self.agentname = self.args.agentname


		if 'Agent' not in self.config:
			self.config['Agent'] = {}
			self.saveini()

		if 'agentname' not in self.config['Agent']:
			self.config['Agent']['agentname'] = self.agentname
			self.saveini()
		else:
			self.agentname = self.config['Agent']['agentname']

		if 'agentdir' not in self.config['Agent']:
			self.config['Agent']['agentdir'] = os.path.join(tempfile.gettempdir(), "rfswarmagent")
			self.saveini()

		if 'xmlmode' not in self.config['Agent']:
			self.config['Agent']['xmlmode'] = str(self.xmlmode)
			self.saveini()

		self.xmlmode = self.str2bool(self.config['Agent']['xmlmode'])
		if self.args.xmlmode:
			self.debugmsg(6, "self.args.xmlmode: ", self.args.xmlmode)
			self.xmlmode = self.str2bool(self.args.xmlmode)

		self.agentdir = self.config['Agent']['agentdir']
		if self.args.agentdir:
			self.debugmsg(1, "self.args.agentdir: ", self.args.agentdir)
			self.agentdir = self.args.agentdir
		self.ensuredir(self.agentdir)

		self.scriptdir = os.path.join(self.agentdir, "scripts")
		self.ensuredir(self.scriptdir)

		self.logdir = os.path.join(self.agentdir, "logs")
		self.ensuredir(self.logdir)


		if 'excludelibraries' not in self.config['Agent']:
			self.config['Agent']['excludelibraries'] = "BuiltIn,String,OperatingSystem,perftest"
			self.saveini()

		# self.excludelibraries = ["BuiltIn", "String", "OperatingSystem", "perftest"]
		self.excludelibraries = self.config['Agent']['excludelibraries'].split(",")
		self.debugmsg(6, "self.excludelibraries:", self.excludelibraries)


		if 'properties' not in self.config['Agent']:
			self.config['Agent']['properties'] = ""
			self.saveini()


		if not self.xmlmode:
			self.debugmsg(6, "self.xmlmode: ", self.xmlmode)
			self.create_listner_file()

		t = threading.Thread(target=self.tick_counter)
		t.start()

		t = threading.Thread(target=self.findlibraries)
		t.start()



		self.agentproperties["OS: Platform"] = platform.platform()	# 'Linux-3.3.0-8.fc16.x86_64-x86_64-with-fedora-16-Verne'
		self.agentproperties["OS: System"] = platform.system()   # 'Windows'
		self.agentproperties["OS: Release"] = platform.release()  # 'XP'
		self.agentproperties["OS: Version"] = platform.version()  # '5.1.2600'

		if platform.system() == 'Windows':
			vararr= platform.version().split(".")
		else:
			vararr= platform.release().split(".")

		if len(vararr)>0:
			self.agentproperties["OS: Version: Major"] = "{}".format(int(vararr[0]))
		if len(vararr)>1:
			self.agentproperties["OS: Version: Minor"] = "{}.{}".format(int(vararr[0]), int(vararr[1]))


		if 'properties' in self.config['Agent'] and len(self.config['Agent']['properties'])>0:
			if "," in self.config['Agent']['properties']:
				proplist = self.config['Agent']['properties'].split(",")
				for prop in proplist:
					self.agentproperties["{}".format(prop.strip())] = True
			else:
				self.agentproperties["{}".format(self.config['Agent']['properties'].strip())] = True

		if self.args.property:
			self.debugmsg(7, "self.args.property: ", self.args.property)
			for prop in self.args.property:
				self.agentproperties["{}".format(prop.strip())] = True

		self.debugmsg(9, "self.agentproperties: ", self.agentproperties)


	def debugmsg(self, lvl, *msg):
		msglst = []
		prefix = ""
		# print(self.debuglvl >= lvl, self.debuglvl, lvl, *msg)
		if self.debuglvl >= lvl:
			try:
				if self.debuglvl >= 4:
					stack = inspect.stack()
					the_class = stack[1][0].f_locals["self"].__class__.__name__
					the_method = stack[1][0].f_code.co_name
					the_line = stack[1][0].f_lineno
					prefix = "{}: {}({}): [{}:{}]	".format(str(the_class), the_method, the_line, self.debuglvl, lvl)
					if len(prefix.strip())<32:
						prefix = "{}	".format(prefix)
					if len(prefix.strip())<24:
						prefix = "{}	".format(prefix)

					msglst.append(str(prefix))

				for itm in msg:
					msglst.append(str(itm))
				print(" ".join(msglst))
			except:
				pass

	def str2bool(self, instr):
		return str(instr).lower()  in ("yes", "true", "t", "1")

	def mainloop(self):
		self.debugmsg(6, "mainloop")
		prev_status = self.status
		while True:
			self.debugmsg(2, self.status, datetime.now().isoformat(sep=' ',timespec='seconds'),
				"(",int(time.time()),")",
				"isconnected:", self.isconnected,
				"isrunning:", self.isrunning,
				"isstopping:", self.isstopping,
				"robotcount:", self.robotcount,
				"\n"
				)

			if not self.isconnected:
				# self.isrunning = False # Not sure if I need this?
				# self.connectmanager()
				t = threading.Thread(target=self.connectmanager)
				t.start()
				self.isrunning = False

			self.debugmsg(5, "self.isconnected", self.isconnected)
			if self.isconnected:
				# self.updatestatus()
				t0 = threading.Thread(target=self.updatestatus)
				t0.start()

				t1 = threading.Thread(target=self.getjobs)
				t1.start()

				if self.isrunning:
					self.mainloopinterval = 2
					self.status = "Running"
					if self.isstopping:
						self.status = "Stopping"
					# else:
					t2 = threading.Thread(target=self.runjobs)
					t2.start()
				else:
					self.mainloopinterval = 10
					if len(self.upload_queue)>0:
						self.status = "Uploading ({})".format(len(self.upload_queue))
						self.debugmsg(5, "self.status:", self.status, "len(self.upload_queue):", len(self.upload_queue))
						t3 = threading.Thread(target=self.process_file_upload_queue)
						t3.start()
					else:
						self.status = "Ready"
						t2 = threading.Thread(target=self.getscripts)
						t2.start()



			if (prev_status == "Stopping" or "Uploading" in prev_status) and self.status == "Ready":
				# neet to reset something
				# I guess we can just reset the jobs disctionary?
				self.jobs = {}
				# pass

			time.sleep(self.mainloopinterval)

	def updateipaddresslist(self):
		if len(self.ipaddresslist)<1:
			self.ipaddresslist = []
			iflst = psutil.net_if_addrs()
			for nic in iflst.keys():
				self.debugmsg(6, "nic", nic)
				for addr in iflst[nic]:
					 # '127.0.0.1', '::1', 'fe80::1%lo0'
					self.debugmsg(6, "addr", addr.address)
					if addr.address not in ['127.0.0.1', '::1', 'fe80::1%lo0']:
						self.ipaddresslist.append(addr.address)

	def updatenetpct(self):
		netpctlist = []
		# self.netpct = 0
		niccounters0 = psutil.net_io_counters(pernic=True)
		time.sleep(1)
		niccounters1 = psutil.net_io_counters(pernic=True)
		nicstats = psutil.net_if_stats()
		for nic in nicstats.keys():
			if nicstats[nic].speed>0:
				self.debugmsg(6, "Speed:", nicstats[nic].speed)
				bytes_speed = nicstats[nic].speed * 1024 * 1024
				bytes_sent_sec = niccounters1[nic].bytes_sent - niccounters0[nic].bytes_sent
				bytes_recv_sec = niccounters1[nic].bytes_recv - niccounters0[nic].bytes_recv
				self.debugmsg(6, "bytes_speed:	", bytes_speed)
				self.debugmsg(6, "bytes_sent_sec:	", bytes_sent_sec)
				self.debugmsg(6, "bytes_recv:	", bytes_recv_sec)
				bytes_max_sec = max([bytes_sent_sec, bytes_recv_sec])
				self.debugmsg(6, "bytes_max_sec:	", bytes_max_sec)
				if bytes_max_sec > 0:
					netpctlist.append((bytes_max_sec/bytes_speed)*100)
				else:
					netpctlist.append(0)

		if len(netpctlist)>0:
			self.debugmsg(6, "netpctlist:	", netpctlist)
			self.netpct = max(netpctlist)
			self.debugmsg(6, "self.netpct:	", self.netpct)
		else:
			self.netpct = 0


	def updatestatus(self):
		self.debugmsg(6, "self.swarmmanager:", self.swarmmanager)
		uri = self.swarmmanager + "AgentStatus"

		# self.updateipaddresslist()
		t1 = threading.Thread(target=self.updateipaddresslist)
		t1.start()
		# self.updatenetpct()
		t2 = threading.Thread(target=self.updatenetpct)
		t2.start()

		payload = {
			"AgentName": self.agentname,
			"AgentFQDN": socket.getfqdn(),
			"AgentIPs": self.ipaddresslist,
			"CPU%": psutil.cpu_percent(),
			"MEM%": dict(psutil.virtual_memory()._asdict())["percent"],
			"NET%": self.netpct,
			"Robots": self.robotcount,
			"Status": self.status,
			"Properties": self.agentproperties
		}
		try:
			r = requests.post(uri, json=payload, timeout=self.timeout)
			self.debugmsg(8, r.status_code, r.text)
			if (r.status_code != requests.codes.ok):
				self.debugmsg(5, "r.status_code:", r.status_code, requests.codes.ok, r.text)
				self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
				self.isconnected = False
				self.debugmsg(7, "self.isconnected", self.isconnected)
		except Exception as e:
			self.debugmsg(8, "Exception:", e)
			self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
			self.isconnected = False
			self.debugmsg(5, "self.isconnected", self.isconnected)

	def connectmanager(self):
		self.debugmsg(6, "connectmanager")
		if self.swarmmanager is None:
			self.findmanager()
			if self.args.manager:
				self.debugmsg(7, "self.args.manager: ", self.args.manager)
				self.swarmmanager = self.args.manager

		if self.swarmmanager is not None:
			self.debugmsg(2, "Try connecting to", self.swarmmanager)
			self.debugmsg(6, "self.swarmmanager:", self.swarmmanager)
			try:
				r = requests.get(self.swarmmanager, timeout=self.timeout)
				self.debugmsg(8, r.status_code, r.text)
				if (r.status_code == requests.codes.ok):
					self.debugmsg(7, "r.status_code:", r.status_code, requests.codes.ok, r.text)
					self.isconnected = True
					self.debugmsg(0, "Manager Connected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
			except:
				pass

	def findmanager(self):
		self.debugmsg(6, "findmanager")
		self.debugmsg(6, "findmanager:", self.config)
		if 'Agent' in self.config:
			self.debugmsg(6, "findmanager:", self.config['Agent'])
			pass
		else:
			self.config['Agent'] = {}
			self.saveini()

		if 'swarmserver' in self.config['Agent']:
			if 'swarmmanager' not in self.config['Agent']:
				self.config['Agent']['swarmmanager'] = self.config['Agent']['swarmserver']
			del self.config['Agent']['swarmserver']
			self.saveini()

		if 'swarmmanager' in self.config['Agent']:
			self.debugmsg(6, "findmanager: Agent:swarmmanager =", self.config['Agent']['swarmmanager'])
			self.swarmmanager = self.config['Agent']['swarmmanager']
		else:
			self.config['Agent']['swarmmanager'] = "http://localhost:8138/"
			self.saveini()

	def findlibraries(self):
		found = 0
		liblst = []
		# import pkg_resources
		installed_packages = pkg_resources.working_set
		# self.debugmsg(5, "installed_packages:", installed_packages)
		for i in installed_packages:
			# self.debugmsg(5, "i:", i)
			# self.debugmsg(5, "type(i):", type(i))

			# self.debugmsg(5, "i.key:", i.key)
			# self.debugmsg(5, "i.value:", installed_packages[i])
			# self.debugmsg(5, "i value:", str(i).split(" ")[1])


			if i.key.strip() == "robotframework":
				found = 1
			if i.key.startswith("robotframework-"):
				# print(i.key)
				keyarr = i.key.strip().split("-")
				#  next overwrites previous
				self.agentproperties["RobotFramework: Library: "+keyarr[1]] = str(i).split(" ")[1]
				liblst.append(keyarr[1])

		self.debugmsg(8, "liblst:", liblst, len(liblst))
		if len(liblst)>0:
			self.debugmsg(7, "liblst:", ", ".join(liblst))
			self.agentproperties["RobotFramework: Libraries"] = ", ".join(liblst)

		if not found:
			self.debugmsg(0, "RobotFramework is not installed!!!")
			self.debugmsg(0, "RobotFramework is required for the agent to run scripts")
			self.debugmsg(0, "Perhaps try: 'pip install robotframework'")
			raise Exception("RobotFramework is not installed")


	def tick_counter(self):
		#
		# This function is simply a way to roughly measure the number of agents being used
		# without collecting any other data from the user or thier machine.
		#
		# A simple get request on this file on startup or once a day should make it appear
		# in the github insights if people are actually using this application.
		#
		# t = threading.Thread(target=self.tick_counter)
		# t.start()
		# only tick once per day
		# 1 day, 24 hours  = 60 * 60 * 24
		aday = 60 * 60 * 24
		while True:

			ver = self.version
			if ver[0] != 'v':
				ver = "v" + ver

			# https://github.com/damies13/rfswarm/blob/v0.6.2/Doc/Images/z_agent.txt
			url = "https://github.com/damies13/rfswarm/blob/"+ver+"/Doc/Images/z_agent.txt"
			try:
				r = requests.get(url, timeout=self.timeout)
				self.debugmsg(9, "tick_counter:", r.status_code)
			except:
				pass
			time.sleep(aday)


	def getscripts(self):
		self.debugmsg(6, "getscripts")
		uri = self.swarmmanager + "Scripts"
		payload = {
			"AgentName": self.agentname
		}
		self.debugmsg(6, "getscripts: payload: ", payload)
		try:
			r = requests.post(uri, json=payload, timeout=self.timeout)
			self.debugmsg(6, "getscripts: resp: ", r.status_code, r.text)
			if (r.status_code != requests.codes.ok):
				self.debugmsg(5, "r.status_code:", r.status_code, requests.codes.ok)
				self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
				self.isconnected = False

		except Exception as e:
			self.debugmsg(8, "Exception:", e)
			self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
			self.isconnected = False

		if not self.isconnected:
			return None

		try:
			jsonresp = {}
			# self.scriptlist
			jsonresp = json.loads(r.text)
			self.debugmsg(6, "getscripts: jsonresp:", jsonresp)
		except Exception as e:
			self.debugmsg(1, "getscripts: Exception:", e)

		for s in jsonresp["Scripts"]:
			hash = s['Hash']
			self.debugmsg(6, "getscripts: hash:", hash)
			if hash not in self.scriptlist:
				self.scriptlist[hash] = {'id': hash}
				t = threading.Thread(target=self.getfile, args=(hash,))
				t.start()

	def getfile(self, hash):
		self.debugmsg(6, "hash: ", hash)
		uri = self.swarmmanager + "File"
		payload = {
			"AgentName": self.agentname,
			"Action": "Download",
			"Hash": hash
		}
		try:
			r = requests.post(uri, json=payload, timeout=self.timeout)
			self.debugmsg(6, "resp: ", r.status_code, r.text)
			if (r.status_code != requests.codes.ok):
				self.debugmsg(5, "r.status_code:", r.status_code, requests.codes.ok)
				self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
				self.isconnected = False

		except Exception as e:
			self.debugmsg(8, "Exception:", e)
			self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
			self.isconnected = False

		if not self.isconnected:
			return None

		try:
			jsonresp = {}
			# self.scriptlist
			jsonresp = json.loads(r.text)
			self.debugmsg(7, "jsonresp:", jsonresp)
		except Exception as e:
			self.debugmsg(1, "Exception:", e)

		try:
			self.debugmsg(7, 'scriptdir', self.scriptdir)
			localfile = os.path.abspath(os.path.join(self.scriptdir, jsonresp['File']))
			self.debugmsg(1, 'localfile', localfile)

		except Exception as e:
			self.debugmsg(0, "Exception:", e)

		try:
			self.scriptlist[hash]['localfile'] = localfile
			self.scriptlist[hash]['file'] = jsonresp['File']

			# self.scriptlist[hash][]

			filedata = jsonresp['FileData']
			self.debugmsg(6, "filedata:", filedata)
			self.debugmsg(6, "filedata:")

			decoded = base64.b64decode(filedata)
			self.debugmsg(6, "b64decode: decoded:", decoded)
			self.debugmsg(6, "b64decode:")

			uncompressed = lzma.decompress(decoded)
			self.debugmsg(6, "uncompressed:", uncompressed)
			self.debugmsg(6, "uncompressed:")

			localfiledir = os.path.dirname(localfile)
			self.debugmsg(6, "localfiledir:", localfiledir)
			self.ensuredir(localfiledir)
			self.debugmsg(6, "ensuredir:")

			with open(localfile, 'wb') as afile:
				self.debugmsg(6, "afile:")
				afile.write(uncompressed)
				self.debugmsg(6, "write:")

		except Exception as e:
			self.debugmsg(1, "Exception:", e)

	def getjobs(self):
		self.debugmsg(6, "getjobs")
		uri = self.swarmmanager + "Jobs"
		payload = {
			"AgentName": self.agentname
		}
		self.debugmsg(9, "getjobs: payload: ", payload)
		try:
			r = requests.post(uri, json=payload, timeout=self.timeout)
			self.debugmsg(7, "getjobs: resp: ", r.status_code, r.text)
			if (r.status_code != requests.codes.ok):
				self.debugmsg(7, "r.status_code:", r.status_code, requests.codes.ok)
				self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
				self.isconnected = False

		except Exception as e:
			self.debugmsg(8, "Exception:", e)
			self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
			self.isconnected = False

		if not self.isconnected:
			return None

		try:
			jsonresp = {}
			# self.scriptlist
			self.debugmsg(7, "getjobs: r.text:", r.text)
			jsonresp = json.loads(r.text)
			self.debugmsg(7, "getjobs: jsonresp:", jsonresp)


			if jsonresp["StartTime"] < int(time.time()) < (jsonresp["EndTime"]+300):
				self.isrunning = True
				self.run_name = jsonresp["RunName"]
				for s in jsonresp["Schedule"].keys():
					self.debugmsg(6, "getjobs: s:", s)
					if s not in self.jobs.keys():
						self.jobs[s] = {}
					for k in jsonresp["Schedule"][s].keys():
						self.debugmsg(6, "getjobs: self.jobs[",s,"][",k,"]", jsonresp["Schedule"][s][k])
						self.jobs[s][k] = jsonresp["Schedule"][s][k]

				if int(time.time()) > jsonresp["EndTime"]:
					self.isstopping = True
				if self.isstopping and self.robotcount < 1:
					self.jobs = {}
					self.isrunning = False
					self.isstopping = False
			else:
				if self.robotcount < 1:
					self.isrunning = False
					self.isstopping = False
				else:
					self.isstopping = True

			self.debugmsg(7, "jsonresp[Abort]", jsonresp["Abort"])
			if jsonresp["Abort"]:
				self.isstopping = True
				self.debugmsg(5, "!!! Abort !!!")
				self.abortjobs()


			self.debugmsg(5, "getjobs: isrunning:", self.isrunning, "	isstopping:", self.isstopping)
			self.debugmsg(7, "getjobs: self.jobs:", self.jobs)



		except Exception as e:
			self.debugmsg(1, "getjobs: Exception:", e)

	def abortjobs(self):
		self.debugmsg(6, "self.jobs:", self.jobs)
		for job in self.jobs:
			try:
				self.debugmsg(6, "job:", job, self.jobs[job])
				self.debugmsg(5, "job[PID]:", self.jobs[job]["PID"])
				self.debugmsg(6, "job[Process]:", self.jobs[job]["Process"])
				p = self.jobs[job]["Process"]
				p.terminate()

			except Exception as e:
				self.debugmsg(1, "getjobs: Exception:", e)


	def runjobs(self):
		self.debugmsg(6, "runjobs: self.jobs:", self.jobs)
		workingkeys = list(self.jobs.keys())
		if not self.isstopping:
			for jobid in workingkeys:
				if jobid in self.jobs.keys():
					self.debugmsg(6, "runjobs: jobid:", jobid)
					run_t = True
					if "Thread" in self.jobs[jobid].keys():
						self.debugmsg(7, "jobid:", self.jobs[jobid])
						try:
							# if self.jobs[jobid]["Thread"].isAlive():
							# The isAlive syntax above was perviously working in python < 3.7
							# but appears to have been removed in 3.9.1? it was depricated in 2.x?
							# and the is_alive syntax below has been available since python version 2.6
							if self.jobs[jobid]["Thread"].is_alive():
								run_t = False
								self.debugmsg(7, "Thread already running run_t:", run_t)
						except Exception as e:
							run_t = False
							self.debugmsg(5, "Thread running check failed run_t:", run_t, e)

					self.debugmsg(6, "run_t:", run_t)

					if run_t:
						self.debugmsg(5, "jobid:", jobid, "run_t:", run_t, "StartTime:", self.jobs[jobid]["StartTime"], "< Now:", int(time.time()), "< EndTime:", self.jobs[jobid]["EndTime"])
						if self.jobs[jobid]["StartTime"] < int(time.time()) < self.jobs[jobid]["EndTime"]:
							t = threading.Thread(target=self.runthread, args=(jobid, ))
							t.start()
							self.jobs[jobid]["Thread"] = t
							self.debugmsg(5, "Thread started for jobid:", jobid)
						else:
							self.debugmsg(5, "Thread not started for jobid:", jobid)
				time.sleep(0.1)


	def runthread(self, jobid):
		now = int(time.time())
		if "ScriptIndex" not in self.jobs[jobid]:
			self.debugmsg(6, "runthread: jobid:", jobid)
			self.debugmsg(6, "runthread: job data:", self.jobs[jobid])
			jobarr = jobid.split("_")
			self.jobs[jobid]["ScriptIndex"] = jobarr[0]
			self.jobs[jobid]["VUser"] = jobarr[1]
			self.jobs[jobid]["Iteration"] = 0
			self.debugmsg(6, "runthread: job data:", self.jobs[jobid])

		self.jobs[jobid]["Iteration"] += 1

		hash = self.jobs[jobid]['ScriptHash']
		self.debugmsg(6, "runthread: hash:", hash)
		test = self.jobs[jobid]['Test']
		self.debugmsg(6, "runthread: test:", test)
		localfile = self.scriptlist[hash]['localfile']
		self.debugmsg(6, "runthread: localfile:", localfile)

		file = self.scriptlist[hash]['file']
		self.debugmsg(6, "runthread: file:", file)

		farr = os.path.splitext(file)
		self.debugmsg(6, "runthread: farr:", farr)


		excludelibraries = ",".join(self.excludelibraries)
		if "excludelibraries" in self.jobs[jobid]:
			# not sure if we need to do this???
			# for safety split and join string
			# ellst = self.jobs[jobid]['excludelibraries'].split(",")
			# excludelibraries = ",".join(ellst)
			excludelibraries = self.jobs[jobid]['excludelibraries']

		# self.run_name
		# scriptdir = None
		# logdir = None

		rundir = os.path.join(self.logdir, self.run_name)
		try:
			if not os.path.exists(rundir):
				os.makedirs(rundir)
		except:
			pass

		threaddirname = self.make_safe_filename("{}_{}_{}_{}".format(farr[0], jobid, self.jobs[jobid]["Iteration"], now))
		odir = os.path.join(self.logdir, self.run_name, threaddirname)
		self.debugmsg(6, "runthread: odir:", odir)
		try:
			if not os.path.exists(odir):
				os.makedirs(odir)
		except:
			pass

		oprefix = self.make_safe_filename(test)
		self.debugmsg(6, "runthread: oprefix:", oprefix)
		logFileName = os.path.join(odir, "{}.log".format(oprefix))
		self.debugmsg(6, "runthread: logFileName:", logFileName)
		outputFileName = "{}_output.xml".format(oprefix)
		outputFile = os.path.join(odir, outputFileName)
		self.debugmsg(6, "runthread: outputFile:", outputFile)


		if 'Agent' not in self.config:
			self.config['Agent'] = {}
			self.saveini()

		if 'robotcmd' not in self.config['Agent']:
			self.config['Agent']['robotcmd'] = "robot"
			self.saveini()

		robotcmd = self.config['Agent']['robotcmd']
		if self.args.robot:
			self.debugmsg(1, "runthread: self.args.robot: ", self.args.robot)
			robotcmd = self.args.robot

		cmd = [robotcmd]
		cmd.append("-t")
		cmd.append('"'+test+'"')
		cmd.append("-d")
		cmd.append('"'+odir+'"')

		cmd.append("-M agent:{}".format(self.agentname))
		if self.xmlmode:
			cmd.append("-v index:{}".format(self.jobs[jobid]["ScriptIndex"]))
			cmd.append("-v vuser:{}".format(self.jobs[jobid]["VUser"]))
			cmd.append("-v iteration:{}".format(self.jobs[jobid]["Iteration"]))
		else:
			cmd.append("-M debuglevel:{}".format(self.debuglvl))
			cmd.append("-M index:{}".format(self.jobs[jobid]["ScriptIndex"]))
			cmd.append("-M vuser:{}".format(self.jobs[jobid]["VUser"]))
			cmd.append("-M iteration:{}".format(self.jobs[jobid]["Iteration"]))
			cmd.append("-M swarmmanager:{}".format(self.swarmmanager))
			cmd.append("-M excludelibraries:{}".format(excludelibraries))
			cmd.append("--listener {}".format('"'+self.listenerfile+'"'))

		if "robotoptions" in self.jobs[jobid]:
			cmd.append("{}".format(self.jobs[jobid]['robotoptions']))

		cmd.append("-o")
		cmd.append('"'+outputFile+'"')

		cmd.append('"'+localfile+'"')

		robotexe = shutil.which(robotcmd)
		self.debugmsg(6, "runthread: robotexe:", robotexe)
		if robotexe is not None:
			self.robotcount += 1

			result = 0
			try:
				# https://stackoverflow.com/questions/4856583/how-do-i-pipe-a-subprocess-call-to-a-text-file
				with open(logFileName, "w") as f:
					self.debugmsg(3, "Robot run with command: '", " ".join(cmd), "'")
					# result = subprocess.call(" ".join(cmd), shell=True, stdout=f, stderr=f)
					try:
						proc = subprocess.Popen(" ".join(cmd), shell=True, stdout=f, stderr=subprocess.STDOUT)
						self.debugmsg(5, "runthread: proc:", proc)
						self.jobs[jobid]["Process"] = proc
						self.jobs[jobid]["PID"] = proc.pid
						self.debugmsg(5, "runthread: proc.pid:", proc.pid)
						result = proc.wait()
						self.debugmsg(5, "runthread: result:", result)
						if result != 0:
							self.debugmsg(1, "Robot returned an error (", result, ") please check the log file:", logFileName)
					except Exception as e:
							self.debugmsg(1, "Robot returned an error:", e, " \nplease check the log file:", logFileName)
							result = 1
					f.close()

				if self.xmlmode:
					if os.path.exists(outputFile):
						if self.xmlmode:
							t = threading.Thread(target=self.run_process_output, args=(outputFile, self.jobs[jobid]["ScriptIndex"], self.jobs[jobid]["VUser"], self.jobs[jobid]["Iteration"]))
							t.start()
					else:
						self.debugmsg(1, "Robot didn't create (", outputFile, ") please check the log file:", logFileName)

			except Exception as e:
				self.debugmsg(5, "Robot returned an error:", e)
				result = 1

			# Uplad any files found

			self.queue_file_upload(result, odir)

			self.robotcount += -1
		else:
			self.debugmsg(1, "Could not find robot executeable:", robotexe)


	def queue_file_upload(self, retcode, filedir):
		reldir = os.path.basename(filedir)
		self.debugmsg(7, retcode, reldir, filedir)

		filelst = self.file_upload_list(filedir)
		self.debugmsg(7, "filelst", filelst)
		# filelst
		# [
		# 	'/var/folders/7l/k7w46dm91y3gscxlswd_jm2r0000gn/T/rfswarmagent/logs/20201219_113254_11u_test_quick/OC_Demo_2_1_5_1608341588_1_1608341594/Browse_Store_Product_1.log',
		# 	'/var/folders/7l/k7w46dm91y3gscxlswd_jm2r0000gn/T/rfswarmagent/logs/20201219_113254_11u_test_quick/OC_Demo_2_1_5_1608341588_1_1608341594/log.html',
		# 	'/var/folders/7l/k7w46dm91y3gscxlswd_jm2r0000gn/T/rfswarmagent/logs/20201219_113254_11u_test_quick/OC_Demo_2_1_5_1608341588_1_1608341594/report.html',
		# 	'/var/folders/7l/k7w46dm91y3gscxlswd_jm2r0000gn/T/rfswarmagent/logs/20201219_113254_11u_test_quick/OC_Demo_2_1_5_1608341588_1_1608341594/Browse_Store_Product_1_output.xml'
		# ]
		#

		rundir = os.path.join(self.logdir, self.run_name)

		for file in filelst:
			fobj = {}
			fobj["LocalFilePath"] = file
			fobj["RelFilePath"] = os.path.relpath(file, start=rundir)
			self.upload_queue.append(fobj)
			self.debugmsg(7, "added to upload_queue", fobj)
			if retcode > 0:
				# upload now
				self.file_upload(fobj)



	def file_upload_list(self, filedir):
		retlst = []
		dirlst = os.listdir(path=filedir)
		self.debugmsg(7, "dirlst", dirlst)
		for item in dirlst:
			fullpath = os.path.join(filedir, item)
			if os.path.isfile(fullpath):
				retlst.append(fullpath)
			else:
				files = self.file_upload_list(fullpath)
				for file in files:
					retlst.append(file)
		return retlst



	def file_upload(self, fileobj):
		self.debugmsg(7, "fileobj", fileobj)

		# Hash file

		hash = self.hash_file(fileobj['LocalFilePath'], fileobj['RelFilePath'])
		self.debugmsg(7, "hash", hash)


		# 	check file exists on manager?

		uri = self.swarmmanager + "File"
		payload = {
			"AgentName": self.agentname,
			"Action": "Status",
			"Hash": hash
		}
		self.debugmsg(9, "payload: ", payload)
		try:
			r = requests.post(uri, json=payload, timeout=self.timeout)
			self.debugmsg(7, "resp: ", r.status_code, r.text)
			if (r.status_code != requests.codes.ok):
				self.debugmsg(5, "r.status_code:", r.status_code, requests.codes.ok)
				self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
				self.isconnected = False

		except Exception as e:
			self.debugmsg(8, "Exception:", e)
			self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
			self.isconnected = False

		if not self.isconnected:
			return None

		jsonresp = {}
		try:
			# self.scriptlist
			jsonresp = json.loads(r.text)
			self.debugmsg(7, "jsonresp:", jsonresp)
		except Exception as e:
			self.debugmsg(1, "Exception:", e)
			return None

		# 	If file not exists upload the file
		if jsonresp["Exists"] == "False":
			self.debugmsg(6, "file not there, so lets upload")

			payload = {
				"AgentName": self.agentname,
				"Action": "Upload",
				"Hash": hash,
				"File": fileobj['RelFilePath']
			}

			localpath = fileobj['LocalFilePath']
			buf = "\n"
			with open(localpath, 'rb') as afile:
			    buf = afile.read()
			self.debugmsg(9, "buf:", buf)
			compressed = lzma.compress(buf)
			self.debugmsg(9, "compressed:", compressed)
			encoded = base64.b64encode(compressed)
			self.debugmsg(9, "encoded:", encoded)

			payload["FileData"] = encoded.decode('ASCII')

			self.debugmsg(8, "payload: ", payload)

			try:
				r = requests.post(uri, json=payload, timeout=self.timeout)
				self.debugmsg(7, "resp: ", r.status_code, r.text)
				if (r.status_code != requests.codes.ok):
					self.debugmsg(5, "r.status_code:", r.status_code, requests.codes.ok)
					self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
					self.isconnected = False

			except Exception as e:
				self.debugmsg(8, "Exception:", e)
				self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
				self.isconnected = False

			if not self.isconnected:
				return None

			jsonresp = {}
			try:
				# self.scriptlist
				jsonresp = json.loads(r.text)
				self.debugmsg(7, "jsonresp:", jsonresp)
			except Exception as e:
				self.debugmsg(1, "Exception:", e)
				return None



		# once sucessful remove from queue
		if fileobj in self.upload_queue:
			self.upload_queue.remove(fileobj)


	def hash_file(self, file, relpath):
		BLOCKSIZE = 65536
		hasher = hashlib.md5()
		hasher.update(str(os.path.getmtime(file)).encode('utf-8'))
		hasher.update(relpath.encode('utf-8'))
		with open(file, 'rb') as afile:
			buf = afile.read(BLOCKSIZE)
			while len(buf) > 0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
		self.debugmsg(3, "file:", file, "	hash:", hasher.hexdigest())
		return hasher.hexdigest()


	def process_file_upload_queue(self):
		self.debugmsg(7, "upload_queue", self.upload_queue)
		# self.process_file_upload_queue
		for fobj in self.upload_queue:
			# probably need to make this multi-treaded
			# self.file_upload(fobj)
			t = threading.Thread(target=self.file_upload, args=(fobj,))
			t.start()
			time.sleep(0.5)


	def run_process_output(self, outputFile, index, vuser, iter):
		# This should be a better way to do this
		# https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-interface
		# https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#listener-examples

		seq = 0
		# .//kw[@library!='BuiltIn' and msg]
		# .//kw[@library!='BuiltIn' and msg]/msg
		# .//kw[@library!='BuiltIn' and msg]/status/@status
		# .//kw[@library!='BuiltIn' and msg]/status/@starttime
		# .//kw[@library!='BuiltIn' and msg]/status/@endtime
		try:
			tree = ET.parse(outputFile)
		except:
			self.debugmsg(1, "Error parsing XML file:", outputFile)
		self.debugmsg(6, "tree: '", tree)
		root = tree.getroot()
		self.debugmsg(6, "root: '", root)
		# .//kw/msg/..[not(@library='BuiltIn')]
		for result in root.findall(".//kw/msg/..[@library]"):
			self.debugmsg(6, "run_process_output: result: ", result)
			library = result.get('library')
			# if library not in ["BuiltIn", "String", "OperatingSystem", "perftest"]:
			if library not in self.excludelibraries:
				self.debugmsg(6, "run_process_output: library: ", library)
				seq += 1
				self.debugmsg(6, "result: library:", library)
				txn = result.find('msg').text
				self.debugmsg(6, "result: txn:", txn)

				el_status = result.find('status')
				status = el_status.get('status')
				self.debugmsg(6, "result: status:", status)
				starttime = el_status.get('starttime')
				self.debugmsg(6, "result: starttime:", starttime)
				endtime = el_status.get('endtime')
				self.debugmsg(6, "result: endtime:", endtime)

				# 20191026 09:34:23.044
				startdate = datetime.strptime(starttime, '%Y%m%d %H:%M:%S.%f')
				enddate = datetime.strptime(endtime, '%Y%m%d %H:%M:%S.%f')

				elapsedtime = enddate.timestamp() - startdate.timestamp()

				self.debugmsg(6, "resultname: '", txn,
						"' result'", status,
						"' elapsedtime'", elapsedtime,
						"' starttime'", starttime,
						"' endtime'", endtime, "'"
						)


				# Send result to manager
				uri = self.swarmmanager + "Result"

				self.debugmsg(6, "run_proces_output: uri", uri)

				# requiredfields = ["AgentName", "ResultName", "Result", "ElapsedTime", "StartTime", "EndTime"]

				payload = {
					"AgentName": self.agentname,
					"ResultName": txn,
					"Result": status,
					"ElapsedTime": elapsedtime,
					"StartTime": startdate.timestamp(),
					"EndTime": enddate.timestamp(),
					"ScriptIndex": index,
					"VUser": vuser,
					"Iteration": iter,
					"Sequence": seq
				}

				self.debugmsg(6, "run_proces_output: payload", payload)
				try:
					r = requests.post(uri, json=payload, timeout=self.timeout)
					self.debugmsg(6, "run_proces_output: ",r.status_code, r.text)
					if (r.status_code != requests.codes.ok):
						self.debugmsg(5, "r.status_code:", r.status_code, requests.codes.ok)
						self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
						self.isconnected = False
				except Exception as e:
					self.debugmsg(8, "Exception:", e)
					self.debugmsg(0, "Manager Disconnected", self.swarmmanager, datetime.now().isoformat(sep=' ',timespec='seconds'), "(",int(time.time()),")")
					self.isconnected = False



	def make_safe_filename(self, s):
		def safe_char(c):
			if c.isalnum():
				return c
			else:
				return "_"
		return "".join(safe_char(c) for c in s).rstrip("_")

	def saveini(self):
		with open(self.agentini, 'w') as configfile:    # save
		    self.config.write(configfile)

	def ensuredir(self, dir):
		if os.path.exists(dir):
			return True
		try:
			patharr = os.path.split(dir)
			self.debugmsg(6, "patharr: ", patharr)
			self.ensuredir(patharr[0])
			os.mkdir(dir, mode=0o777)
			self.debugmsg(5, "Directory Created: ", dir)
			return True
		except FileExistsError:
			self.debugmsg(5, "Directory Exists: ", dir)
			return False
		except Exception as e:
			self.debugmsg(1, "Directory Create failed: ", dir)
			self.debugmsg(1, "with error: ", e)
			return False

	def create_listner_file(self):
		self.listenerfile = os.path.join(self.scriptdir, "RFSListener2.py")

		fd = []
		fd.append("")
		fd.append("import os")
		fd.append("import tempfile")
		fd.append("import sys")
		fd.append("import socket")
		fd.append("from datetime import datetime")
		fd.append("import time")
		fd.append("import requests")
		fd.append("import inspect")
		fd.append("import threading")
		fd.append("")
		fd.append("class RFSListener2:")
		fd.append("	ROBOT_LISTENER_API_VERSION = 2")
		fd.append("")
		fd.append("	msg = None")
		fd.append("	swarmmanager = \"http://localhost:8138/\"")
		fd.append("	excludelibraries = [\"BuiltIn\",\"String\",\"OperatingSystem\",\"perftest\"]")
		fd.append("	debuglevel = 0")
		fd.append("	index = 0")
		fd.append("	vuser = 0")
		fd.append("	iter = 0")
		fd.append("	seq = 0")
		fd.append("")
		fd.append("	def start_suite(self, name, attrs):")
		fd.append("		if 'debuglevel' in attrs['metadata']:")
		fd.append("			self.debuglevel = int(attrs['metadata']['debuglevel'])")
		fd.append("			self.debugmsg(6, 'debuglevel: ', self.debuglevel)")
		fd.append("		if 'index' in attrs['metadata']:")
		fd.append("			self.index = attrs['metadata']['index']")
		fd.append("			self.debugmsg(6, 'index: ', self.index)")
		fd.append("		if 'iteration' in attrs['metadata']:")
		fd.append("			self.iter = attrs['metadata']['iteration']")
		fd.append("			self.debugmsg(6, 'iter: ', self.iter)")
		fd.append("		if 'vuser' in attrs['metadata']:")
		fd.append("			self.vuser = attrs['metadata']['vuser']")
		fd.append("			self.debugmsg(6, 'vuser: ', self.vuser)")
		fd.append("		if 'swarmmanager' in attrs['metadata']:")
		fd.append("			self.swarmmanager = attrs['metadata']['swarmmanager']")
		fd.append("			self.debugmsg(6, 'swarmmanager: ', self.swarmmanager)")
		fd.append("		if 'excludelibraries' in attrs['metadata']:")
		fd.append("			self.excludelibraries = attrs['metadata']['excludelibraries'].split(\",\")")
		fd.append("			self.debugmsg(6, 'excludelibraries: ', self.excludelibraries)")
		fd.append("")
		fd.append("	def log_message(self, message):")
		# fd.append("		self.debugmsg(8, 'message[\\'message\\']: ', message['message'])")
		# fd.append("		self.debugmsg(8, 'message[\\'message\\'][0:2]: ', message['message'][0:2])")
		fd.append("		if message['message'][0:2] != '${':")
		fd.append("			self.msg = None")
		fd.append("			self.msg = message")
		# fd.append("			self.debugmsg(6, 'message: ', message)")
		# fd.append("			self.debugmsg(6, 'self.msg: ', self.msg)")
		fd.append("")
		fd.append("	def end_keyword(self, name, attrs):")
		fd.append("		self.debugmsg(3, 'name: ', name)")
		fd.append("		self.debugmsg(6, 'attrs: ', attrs)")
		fd.append("		self.debugmsg(5, 'attrs[doc]: ', attrs['doc'])")
		fd.append("		self.debugmsg(5, 'self.msg: ', self.msg)")
		fd.append("		if self.msg is not None:")
		fd.append("			self.debugmsg(8, 'self.msg: attrs[libname]: ', attrs['libname'], '	excludelibraries:', self.excludelibraries)")
		fd.append("			if attrs['libname'] not in self.excludelibraries:")
		fd.append("				self.seq += 1")
		fd.append("				self.debugmsg(8, 'self.seq: ', self.seq)")
		fd.append("				startdate = datetime.strptime(attrs['starttime'], '%Y%m%d %H:%M:%S.%f')")
		fd.append("				enddate = datetime.strptime(attrs['endtime'], '%Y%m%d %H:%M:%S.%f')")
		fd.append("				self.debugmsg(6, 'ResultName: self.msg[message]: ', self.msg['message'])")
		fd.append("				payload = {")
		fd.append("					'AgentName': '"+self.agentname+"',")
		fd.append("					'ResultName': self.msg['message'],")
		fd.append("					'Result': attrs['status'],")
		fd.append("					'ElapsedTime': (attrs['elapsedtime']/1000),")
		fd.append("					'StartTime': startdate.timestamp(),")
		fd.append("					'EndTime': enddate.timestamp(),")
		fd.append("					'ScriptIndex': self.index,")
		fd.append("					'VUser': self.vuser,")
		fd.append("					'Iteration': self.iter,")
		fd.append("					'Sequence': self.seq")
		fd.append("				}")
		fd.append("				self.debugmsg(8, 'payload: ', payload)")
		# fd.append("				self.send_result(payload)")
		fd.append("				t = threading.Thread(target=self.send_result, args=(payload,))")
		fd.append("				t.start()")
		fd.append("			else:")
		fd.append("				self.debugmsg(5, attrs['libname'], 'is an excluded library')")
		fd.append("		elif 'doc' in attrs and len(attrs['doc'])>0:")
		fd.append("			self.debugmsg(8, 'attrs[doc]: attrs[libname]: ', attrs['libname'], '	excludelibraries:', self.excludelibraries)")
		fd.append("			if attrs['libname'] not in self.excludelibraries:")
		fd.append("				self.seq += 1")
		fd.append("				self.debugmsg(8, 'self.seq: ', self.seq)")
		fd.append("				startdate = datetime.strptime(attrs['starttime'], '%Y%m%d %H:%M:%S.%f')")
		fd.append("				enddate = datetime.strptime(attrs['endtime'], '%Y%m%d %H:%M:%S.%f')")
		fd.append("				self.debugmsg(8, 'attrs: ', attrs)")
		fd.append("				self.debugmsg(6, 'ResultName: attrs[doc]: ', attrs['doc'])")
		fd.append("				payload = {")
		fd.append("					'AgentName': '"+self.agentname+"',")
		fd.append("					'ResultName': attrs['doc'],")
		fd.append("					'Result': attrs['status'],")
		fd.append("					'ElapsedTime': (attrs['elapsedtime']/1000),")
		fd.append("					'StartTime': startdate.timestamp(),")
		fd.append("					'EndTime': enddate.timestamp(),")
		fd.append("					'ScriptIndex': self.index,")
		fd.append("					'VUser': self.vuser,")
		fd.append("					'Iteration': self.iter,")
		fd.append("					'Sequence': self.seq")
		fd.append("				}")
		fd.append("				self.debugmsg(8, 'payload: ', payload)")
		# fd.append("				self.send_result(payload)")
		fd.append("				t = threading.Thread(target=self.send_result, args=(payload,))")
		fd.append("				t.start()")
		fd.append("			else:")
		fd.append("				self.debugmsg(5, attrs['libname'], 'is an excluded library')")
		fd.append("		self.msg = None")
		fd.append("")
		fd.append("	def debugmsg(self, lvl, *msg):")
		fd.append("		msglst = []")
		fd.append("		prefix = \"\"")
		fd.append("		if self.debuglevel >= lvl:")
		fd.append("			try:")
		fd.append("				if self.debuglevel >= 4:")
		fd.append("					stack = inspect.stack()")
		fd.append("					the_class = stack[1][0].f_locals[\"self\"].__class__.__name__")
		fd.append("					the_method = stack[1][0].f_code.co_name")
		fd.append("					prefix = \"{}: {}: [{}:{}]	\".format(str(the_class), the_method, self.debuglevel, lvl)")
		fd.append("					if len(prefix.strip())<32:")
		fd.append("						prefix = \"{}	\".format(prefix)")
		fd.append("					if len(prefix.strip())<24:")
		fd.append("						prefix = \"{}	\".format(prefix)")
		fd.append("					msglst.append(str(prefix))")
		fd.append("				for itm in msg:")
		fd.append("					msglst.append(str(itm))")
		fd.append("				print(\" \".join(msglst))")
		fd.append("			except:")
		fd.append("				pass")
		fd.append("")
		fd.append("	def send_result(self, payload):")
		fd.append("		uri = self.swarmmanager + 'Result'")
		fd.append("		try:")
		fd.append("			r = requests.post(uri, json=payload, timeout=600)")
		fd.append("			self.debugmsg(7, 'send_result: ',r.status_code, r.text)")
		fd.append("			if (r.status_code != requests.codes.ok):")
		fd.append("				self.isconnected = False")
		fd.append("		except Exception as e:")
		fd.append("			self.debugmsg(0, 'send_result: while attempting to send result to',uri)")
		fd.append("			self.debugmsg(0, 'send_result: with payload:',payload)")
		fd.append("			self.debugmsg(0, 'send_result: ',r.status_code, r.text)")
		fd.append("			self.debugmsg(0, 'send_result: Exception:', e)")
		fd.append("			pass")
		fd.append("")


		# print("RFSwarmAgent: create_listner_file: listenerfile: ", self.listenerfile)
		with open(self.listenerfile, 'w+') as lf:
			# lf.writelines(fd)
			lf.write('\n'.join(fd))

rfsa = RFSwarmAgent()
try:
	rfsa.mainloop()
except KeyboardInterrupt:
	pass
except Exception as e:
	self.debugmsg(1, "rfsa.Exception:", e)
	pass
