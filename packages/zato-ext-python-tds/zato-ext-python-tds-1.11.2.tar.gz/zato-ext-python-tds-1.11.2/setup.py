import os
import setuptools
from setuptools import setup

# The version of this library at the time of forking it
_version = '1.11.2'

requirements = list(open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r').readlines())

print(setuptools.find_packages('src'))

setup(name='zato-ext-python-tds',
      version=_version,
      description='A vendor copy of python-tds.',
      author='Zato Source',
      author_email='info@zato.io',
      url='https://zato.io',
      license="MIT",
      packages=['pytds'],
      package_dir={'': 'src'},
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
      ],
      zip_safe=True,
      install_requires=requirements,
      )
