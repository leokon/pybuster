from setuptools import setup

setup(
    name='pybuster',
    version='0.2.0',
    description='A multithreaded brute-forcing tool for use with web URIs',
    author='Leo Kontogiorgis',
    author_email='leo@konto.dev',
    url='https://github.com/leokon/pybuster',
    packages=['pybuster'],
    entry_points={
        'console_scripts': ['pybuster=pybuster.pybuster:main']
    }
)
