from git import Repo
from os.path import join

URL_BOILERPLATE = "https://github.com/amadeuspepr/pepr-boilerplate.git"

def pepr_init(config, name=None):
	name = name or 'prototype'
	Repo.clone_from(URL_BOILERPLATE, name)
	return config