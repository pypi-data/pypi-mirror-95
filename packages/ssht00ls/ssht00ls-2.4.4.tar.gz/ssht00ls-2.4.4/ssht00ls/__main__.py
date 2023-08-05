#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
import os, sys, syst3m ; sys.path.insert(1, syst3m.defaults.get_source_path(__file__, back=2))
from ssht00ls.classes.config import *
import ssht00ls

# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# defaults.
		cl1.CLI.__init__(self,
			modes={
				"Aliases:":"",
				"    --create-alias":"Create a ssh alias.",
				"        --server myserver":"Specify the server's name.",
				"        --username myuser":"Specify the username.",
				"        --ip 0.0.0.0":"Specify the server's ip.",
				"        --port 22":"Specify the server's port.",
				"        for ssh keys:":"",
				"        --key /path/to/key/private_key":"Specify the path to the private key.",
				"        --passphrase 'MyPassphrase123'":"Specify the keys pasphrase (optional).",
				"        for smart cards:":"",
				"        --smart-cards":"Enable the smart cards boolean.",
				"        --pin 123456":"Specify the smart cards pin code (optional).",
				"Keys:":"",
				"    --generate":"Generate a ssh key.",
				"        --path /keys/mykey/":"Specify the keys directory path.",
				"        --passphrase Passphrase123":"Specify the keys passphrase.",
				"        --comment 'My Key'":"Specify the keys comment.",
				"Sessions:":"",
				"    --command <alias> 'ls .'":"Execute a command over ssh.",
				"    --session <alias>":"Start a ssh session.",
				"        --options '' ":"Specify additional ssh options (optional).",
				"Push & pull:":"",
				"    --pull <path> <alias>:<remote>":"Pull a file / directory.",
				"        --delete":"Also update the deleted files (optional).",
				"        --safe":"Enable version control.",
				"        --forced":"Enable forced mode.",
				"    --push <alias>:<remote> <path>":"Push a file / directory.",
				"        --delete":"Also update the deleted files (optional).",
				"        --safe":"Enable version control.",
				"        --forced":"Enable forced mode.",
				"Mounts:":"",
				"    --mount <alias>:<remote> <path>":"Mount a remote directory.",
				"    --unmount <path>":"Unmount a mounted remote directory.",
				"        --sudo":"Root permission required.",
				"        --forced":"Enable forced mode.",
				"    --index <path> / <alias>:<remote>":"Index the specified path / alias:remote.",
				"Agent:":"",
				"    --start-agent":"Start the ssht00ls agent manually.",
				"    --stop-agent":"Stop the ssht00ls agent.",
				"Daemons:":"",
				"    --start-daemon <alias>:<remote> <path>":"Start a ssync daemon manually.",
				"    --stop-daemon <path>":"Stop a ssync daemon.",
				"Basic:":"",
				"    --kill <identifier>":"Kill all ssh processes that include the identifier.",
				"    --config":"Edit the ssht00ls configuration file (nano).",
				"    -h / --help":"Show the documentation.",
			},
			options={
				"-j / --json":"Print the response in json format.",
			},
			notes={
				"SSHT00LS_CONFIG":"Specify the $SSHT00LS_CONFIG environment variable to use a different ssht00ls config file.",
			},
			alias=ALIAS,
			executable=__file__,
		)

		#
	def start(self):
		
		# check arguments.
		self.arguments.check(json=JSON)

		# help.
		if self.arguments.present(['-h', '--help']):
			self.docs(success=True, chapter=None, json=JSON)

		# check create ssh config.
		elif self.arguments.present('--create-alias'):
			
			# create an ssh alias for the key.
			if not self.arguments.present('--smart-card'):
				key = self.arguments.get('--key')
				response = ssht00ls.aliases.create( 
					# the alias.
					alias=self.arguments.get('--alias'), 
					# the username.
					username=self.arguments.get('--username'), 
					# the public ip of the server.
					public_ip=self.arguments.get('--public-ip'),
					# the public port of the server.
					public_port=self.arguments.get('--public-port'),
					# the private ip of the server.
					private_ip=self.arguments.get('--private-ip'),
					# the private port of the server.
					private_port=self.arguments.get('--private-port'),
					# the path to the private key.
					key=key,
					passphrase=getpass.getpass("Enter the passphrase of key [{key}]:"),
					# smart card.
					smart_card=False,)

			# create an ssh alias for a smart card.
			else:
				response = ssht00ls.aliases.create( 
					# the alias.
					alias=self.arguments.get('--alias'), 
					# the username.
					username=self.arguments.get('--username'), 
					# the public ip of the server.
					public_ip=self.arguments.get('--public-ip'),
					# the public port of the server.
					public_port=self.arguments.get('--public-port'),
					# the private ip of the server.
					private_ip=self.arguments.get('--private-ip'),
					# the private port of the server.
					private_port=self.arguments.get('--private-port'),
					# the path to the private key.
					key=smart_card.path,
					# smart card.
					smart_card=True,
					pin=self.arguments.get('--pin', required=False, default=None), )

			# log to console.
			self.stop(response=response, json=JSON)

		# check create ssh config.
		elif self.arguments.present('--generate'):
			
			# generate a key.
			passphrase = self.get_passphrase(required=False)
			if passphrase in ["", None, "null", "None", "none"]: passphrase = None
			response = ssht00ls.key.generate(
				path=self.arguments.get("--path"), 
				passphrase=passphrase, 
				comment=self.arguments.get("--comment"),)
			self.stop(response=response, json=JSON)

		# kill ssh processes.
		elif self.arguments.present('--kill'):
			response = ssht00ls.utils.kill_ssh(
				identifier=self.arguments.get("--kill"), 
				sudo=self.arguments.present("--sudo"),)
			self.stop(response=response, json=JSON)

		# pull.
		elif self.arguments.present('--pull'):
			remote = self.arguments.get("--pull", index=1)
			path = self.arguments.get("--pull", index=2)
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path> format.", 
					chapter="push & pull", 
					mode="--pull", 
					json=JSON,)
			alias,remote = remote.split(":")
			exclude = None
			if self.arguments.present("--exclude"): 
				exclude = self.arguments.get("--exclude").split(",")
			elif self.arguments.present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.pull(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.arguments.present("--forced"), 
				delete=self.arguments.present("--delete"), 
				safe=self.arguments.present("--safe"), )
			self.stop(response=response, json=JSON)

		# push.
		elif self.arguments.present('--push'):
			path = self.arguments.get("--push", index=1)
			remote = self.arguments.get("--push", index=2)
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="push & pull", 
					mode="--push", 
					json=JSON,)
			alias,remote = remote.split(":")
			exclude = None
			if self.arguments.present("--exclude"): 
				exclude = self.arguments.get("--exclude").split(",")
			elif self.arguments.present("--no-exclude"): exclude = []
			response = ssht00ls.ssync.push(
				alias=alias, 
				remote=remote, 
				path=path,
				exclude=exclude, 
				forced=self.arguments.present("--forced"), 
				delete=self.arguments.present("--delete"), 
				safe=self.arguments.present("--safe"), )
			self.stop(response=response, json=JSON)

		# mount.
		elif self.arguments.present('--mount'):
			remote = self.arguments.get("--mount", index=1)
			path = self.arguments.get("--mount", index=2)
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="mounts", 
					mode="--mount", 
					json=JSON,)
			alias,remote = remote.split(":")
			response = ssht00ls.ssync.mount(
				alias=alias, 
				remote=remote, 
				path=path,
				forced=self.arguments.present("--forced"), )
			self.stop(response=response, json=JSON)

		# unmount.
		elif self.arguments.present('--unmount'):
			path = self.arguments.get("--unmount", index=1)
			response = ssht00ls.ssync.unmount(
				path=path,
				forced=self.arguments.present("--forced"), 
				sudo=self.arguments.present("--sudo"), )
			self.stop(response=response, json=JSON)

		# index.
		elif self.arguments.present('--index'):
			index = self.arguments.get("--index")
			if ":" in index:
				alias,remote = index.split(":")
				response = ssht00ls.ssync.index(path=remote, alias=alias)
			else:
				response = ssht00ls.ssync.index(path=index)
			self.stop(response=response, json=JSON)

		# start daemon.
		elif self.arguments.present('--start-daemon'):
			remote = self.arguments.get("--start-daemon", index=1)
			path = self.arguments.get("--start-daemon", index=2)
			if ":" not in remote:
				self.docs(
					error=f"Invalid <alias>:<remote> <path>.", 
					chapter="mounts", 
					mode="--mount", 
					json=JSON,)
			alias,remote = remote.split(":")
			response = ssht00ls.ssync.daemon(alias=alias, remote=remote, path=path)
			self.stop(response=response, json=JSON)

		# stop daemon.
		elif self.arguments.present('--stop-daemon'):
			path = self.arguments.get("--stop-daemon", index=1)
			response = ssht00ls.ssync.stop_daemon(path)
			self.stop(response=response, json=JSON)

		# config.
		elif self.arguments.present('--config'):
			if JSON:
				print(CONFIG.dictionary)
			else:
				os.system(f"nano {CONFIG.file_path.path}")

		# invalid.
		else: self.invalid()

		#
	def get_passphrase(self, required=True):
		return self.arguments.get("--passphrase", required=required).replace("\\", "").replace("\ ", "")
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
