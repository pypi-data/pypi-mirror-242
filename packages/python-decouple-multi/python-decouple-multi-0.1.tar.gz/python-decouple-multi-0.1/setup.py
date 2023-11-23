from setuptools import setup, find_packages

setup(
  setup_requires='git-versiointi',
  name='python-decouple-multi',
  description='Usean asetustiedoston tuki python-decouple-pakettiin',
  url='https://github.com/an7oine/python-decouple-multi.git',
  author='Antti Hautaniemi',
  author_email='antti.hautaniemi@pispalanit.fi',
  licence='MIT',
  py_modules=['decouple_multi'],
  install_requires=['python-decouple'],
)
