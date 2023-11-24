import os
import glob
from shutil import rmtree

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class CleanCommand(setuptools.Command):
    """ Custom clean command to tidy up the project root. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        rmtree('build', ignore_errors=True)
        rmtree('dist', ignore_errors=True)
        for file in glob.glob('*.egg-info'):
            rmtree(file)


class PrepublishCommand(setuptools.Command):
    """ Custom prepublish command. """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('python setup.py clean')
        os.system('python setup.py sdist bdist_wheel')


setuptools.setup(
    cmdclass={
        'clean': CleanCommand,
        'prepublish': PrepublishCommand,
    },
    name='monutils',
    version='0.1.9',
    url='https://github.com/jmgomezsoriano/mongoutils',
    license='LGPL2',
    author='José Manuel Gómez Soriano',
    author_email='jmgomez.soriano@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='Small Python utils to deal with MongoDB.',
    packages=setuptools.find_packages(exclude=["test"]),
    package_dir={'monutils': 'monutils'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7,<4',
    install_requires=[
        'mysmallutils>=1.1.9,<2.1',
        'pymongo>=3.0,<4.0',
    ],
    entry_points={
        'console_scripts': [
            'moncopy=monutils.copy:main'
        ]
    }
)
