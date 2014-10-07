import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()

requires = [
    'blinker',
    'cqlengine',
    'six',
    ]

setup(name='cqlengine_signal',
      version='0.1',
      description='A limitted signal sytem for cqlengine',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python 3",
        ],
      author='Tarzan',
      author_email='hoc3010@gmail.com',
      url='https://github.com/tarzanjw/cqlengine_signal',
      keywords='cqlengine signal',
      packages=['cqlengine_signal',],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="cqlengine_signal",
      entry_points="""\
      """,
      )
