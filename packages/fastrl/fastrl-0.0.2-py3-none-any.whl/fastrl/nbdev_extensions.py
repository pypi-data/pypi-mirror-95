# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/00_nbdev_extension.ipynb (unless otherwise specified).

__all__ = ['dependencies', 'create_conda_yaml', 'create_conda_yamls']

# Cell
from nbdev.showdoc import *
from nbdev.imports import *
if not os.environ.get("IN_TEST", None):
    assert IN_NOTEBOOK
    assert not IN_COLAB
    assert IN_IPYTHON

import yaml

# Cell
def dependencies(dev:bool=False,cfg_name='settings.ini'):
    "Gets a list of dependencies in a `cfg_name` for conda compatability."
    c=Config(cfg_name)
    deps=[f'python={c.min_python}','pip','setuptools']
    if c.requirements:             deps+=c.requirements.split(' ')
    if c.conda_requirements:       deps+=c.conda_requirements.split(' ')
    if dev and c.dev_requirements: deps+=c.dev_requirements.split(' ')
    if c.pip_requirements:         deps+=[{'pip':c.pip_requirements.split(' ')}]
    return deps

# Cell
def create_conda_yaml(channels:str='conda-forge,pytorch,fastai',
                      cfg_name='settings.ini',dev:bool=False):
    "Creates a conda dictionary of the format of an env file."
    c=Config()
    return {'name':c.lib_name if not dev else c.lib_name+'_dev',
            'channels': channels.split(','),
            'dependencies': dependencies(dev=dev,cfg_name=cfg_name)}

# Cell
def create_conda_yamls(also_dev:bool=True,cfg_name='settings.ini',sub_dir=''):
    "Creates conda env for normal and development environments."
    c=Config(cfg_name)
    parent=c.config_path/Path(sub_dir) if sub_dir else c.config_path
    parent.mkdir(parents=True,exist_ok=True)
    for is_dev in ([False,True] if also_dev else [False]):
        fname=(c.lib_name+f'{"_dev" if is_dev else ""}_env.yaml')
        with open(parent/fname,'w') as f:
            d=create_conda_yaml(cfg_name=cfg_name,dev=is_dev)
            yaml.dump(d,f)