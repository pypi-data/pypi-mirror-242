from setuptools import setup

setup(
   name='csvstat',
   version='1.1',
   description='A useful module',
   author='Wilkens Badio & Clivince Estinvil',
   author_email='wbadio693@gmail.com',
   packages=['csvstat'],  #same as name
   install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)