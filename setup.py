from distutils.core import setup
setup(name='Astronomical Calendar',
      version='0.1',
      packages=['modules', 'modules/adt', 'modules/application'],
      package_data={'modules':['application/*.php']},
      data_files=[('', ['README.md'])])