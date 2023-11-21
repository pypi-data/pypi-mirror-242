from setuptools import setup, find_packages

setup(
    name='hcm2py',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'requests',
    ],
)