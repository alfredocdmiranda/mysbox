from setuptools import setup
import os

__version__ = '0.1'

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Topic :: Home Automation",
    "Topic :: Software Development :: Build Tools",
    "Topic :: Utilities"
    ]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='mysbox',
      version=__version__,
      description="It is a module to make easier communication with MySensor\'s network.",
      author='Alfredo Miranda',
      author_email='alfredocdmiranda@gmail.com',
      url='https://github.com/alfredocdmiranda/mysbox',
      keywords="MYS MySensors",
      license='LGPLv3',
      long_description=read('DESCRIPTION.rst'),
      classifiers=CLASSIFIERS,
      packages=['mysbox'],
      package_data={'mysbox': ['skeletons/*', 'skeletons/.*']},
      install_requires=['pyserial>=2.7',
                        'jinja2>=2.8'],
      entry_points={'console_scripts': ['mysbox = mysbox:main']})
