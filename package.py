# Inspired by npm's package.json file
name              = 'hisa'
version           = '0.1.0'
release           = '0.1.0'
description       = 'A stock market predictor and model builder'
long_description  = ['README.md']
keywords          = ['neural', 'network', 'machine', 'deep',
    'learning', 'tensorflow', 'stock', 'market', 'prediction']
authors           = [
    { 'name': 'Rittika Adhikari', 'email': 'rittika.adhikari@gmail.com' },
		{ 'name': 'Sahil Modi', 'email': 'sm34524@gmail.com'},
		{ 'name': 'Utkarsh Awasthi', 'email': 'navamawasthi@gmail.com'}
]
maintainers       = [
    { 'name': 'Rittika Adhikari', 'email': 'rittika.adhikari@gmail.com' },
		{ 'name': 'Sahil Modi', 'email': 'sm34524@gmail.com'},
		{ 'name': 'Utkarsh Awasthi', 'email': 'navamawasthi@gmail.com'}
]
license           = 'MIT'
modules           = [
    'hisa',
    'hisa.config',
    'hisa.capsule',
    'hisa.learn',
    'hisa.learn.models',
    'hisa.learn.sentiment',
    'hisa._util'
]
github_username   = 'rittikaadhikari'
github_repository = 'hisa'
github_url        = '{baseurl}/{username}/{repository}'.format(
    baseurl    = 'https://github.com',
    username   = github_username,
    repository = github_repository)
