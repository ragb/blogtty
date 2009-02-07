
from distutils.core import setup

""" blogtty instalation script """
setup(
    name = 'blogtty',
    description = 'Command line blogging tool',
    author = 'Rui Batista',
    version = '0.1.0a2',
    author_email = 'rui.batista@ist.utl.pt',
    packages = ['blogapi'],
    scripts = ['blogtty.py']
    )
