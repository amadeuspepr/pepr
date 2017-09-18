import os, pkg_resources
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import subprocess


MODULES = pkg_resources.resource_string(__name__, "data/modules.yaml")

def pepr_module_add(config, *module):
	if not config.has_key("modules") or type(config["modules"]) != list:
		config["modules"] = []
	for m in module:
		config["modules"].append(m)
		__pepr_install_module(m)
	config["modules"] = list(set(config["modules"]))
	return pepr_module_list(config)

def pepr_module_remove(config, *module):
	if config.has_key("modules") and type(config["modules"]) == list:
		config["modules"] = filter(lambda x:x not in module, config["modules"])
	return pepr_module_list(config)

def pepr_module_list(config):
	print "\n".join(config.get("modules",[]))
	return config

def pepr_module_all(config):
	modules = yaml.load(MODULES, Loader=Loader) if MODULES else {}
	print "\n".join(modules.keys())
	return config


def __pepr_install_module(module):
	modules = yaml.load(MODULES, Loader=Loader) if MODULES else {}
	struct = modules.get(module)
	if struct:
		pkg = struct.get("pkg", module)
		pip = struct.get("pip")
		if pip:
			process = subprocess.Popen(("pip", "install", pip), stdout=subprocess.PIPE)
			output, error = process.communicate()
			print output
			print error
