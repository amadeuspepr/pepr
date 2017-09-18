import getpass
from ansible_vault import Vault


password = None
def get_pass(override=False, prompts=["password"]):
	global password
	if override or password is None:
		password = None
		for prompt in prompts:
			newpass = getpass.getpass("%s: " % prompt)
			if password is None:
				password = newpass
			elif password != newpass:
				raise ValueError("Passwords do not match")
	return password

def __read_secrets(password=None):
	password = get_pass()
	vault = Vault(password)
	return vault.load(open(VAULT_FILE).read())

def __write_secrets(data, password=None):
	if password is None:
		password = get_pass()
	vault = Vault(password)
	vault.dump(data, open(VAULT_FILE, 'w'))

def pepr_key_set(config, key, value):
	data = __read_secrets()
	app_secrets = data.get('app_secrets',{})
	app_secrets[key] = value
	data["app_secrets"] = app_secrets
	__write_secrets(data)
	return pepr_key_list(config)

def pepr_key_reset(config, *key):
	data = __read_secrets()
	app_secrets = data.get('app_secrets',{})
	for akey in keys:
		if app_secrets.has_key(akey):
			del app_secrets[akey]
	data["app_secrets"] = app_secrets
	__write_secrets(data)
	return pepr_key_list(config)

def pepr_key_list(config):
	data = __read_secrets()
	app_secrets = data.get('app_secrets',{})
	print "\n".join(map(lambda x:"%s = %s"%x, app_secrets.items()))
	return config


def pepr_password_change(config):
	try:
		data = __read_secrets()
		password = get_pass(override=True, prompts=["new password", "confirm password"])
		__write_secrets(data)
		print >>sys.stderr, "Password was changed !"
	except ValueError as e:
		print >>sys.stderr, "***", e
	return config

def pepr_password_test(config):
	try:
		data = __read_secrets()
		print >>sys.stderr, "VALID !"
	except:
		print >>sys.stderr, "INVALID !"
	return config
