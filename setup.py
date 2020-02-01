from setuptools import setup

setup(
    name='pybuster',
    version='0.2.1',
    description='A multithreaded brute-forcing tool for use with web URIs',
    author='Leo Kontogiorgis',
    author_email='leo@konto.dev',
    url='https://github.com/leokon/pybuster',
    packages=['pybuster'],
    install_requires=[
        'requests',
        'tqdm'
    ],
    entry_points={
        'console_scripts': ['pybuster=pybuster.pybuster:main']
    }
)
