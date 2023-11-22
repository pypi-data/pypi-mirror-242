from setuptools import setup, find_packages
 
setup(
    name='dilithium',
    version='1.0.5',
    plateformes = 'LINUX',
    packages=['dilithium'],
    packages_dir = {'' : 'dilithium'},
    author='eshard',
    description='CRYSTALS-Dilithium for eShard',
    install_requires=['pycryptodome>=03.14.1'],
    url='https://eshard.com',
    license='MIT',
    keywords = ["PQC", "Digital-Signatures", "Dilithium"],
    classifiers = [ "Programming Language :: Python :: 3",
                    "Development Status :: 4 - Beta",
                    "Intended Audience :: Developers",
                    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"],
    long_description=open('README.md').read()
    )