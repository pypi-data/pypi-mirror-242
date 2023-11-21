# setup.py

from setuptools import setup, find_packages

setup(
    name='mathsmadesimpleniraj',
    version='0.3',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies your package might have
    entry_points={
        'console_scripts': [
            'mathsmadesimpleniraj = mathsmadesimpleniraj.calculator:main',  # Optional: If you want to create a command-line entry point
        ],
    },
)
