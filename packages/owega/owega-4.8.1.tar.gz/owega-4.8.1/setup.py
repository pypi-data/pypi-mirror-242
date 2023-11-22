#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from owega.changelog import OwegaChangelog as oc


desc = open('README.md').read()
desc += '\n\n'
desc += "## CHANGELOG: "
desc += '\n```\n'
desc += oc.log
desc += '\n```\n'

requirements = [
	req.strip() for req in open('requirements.txt', 'r').read().split('\n')
	if req.strip()
]

setup(
	name='owega',
	version='4.8.1',
	packages=[
		'owega',
		'owega.changelog',
		'owega.config',
		'owega.OwegaFun',
		'owega.conversation',
	],
	install_requires=requirements,
	scripts=[
		'scripts/owega',
	],
	long_description=desc,
	long_description_content_type='text/markdown',
	project_urls={
		'Source': 'https://git.pyrokinesis.fr/darkgeem/owega',
	},
)
