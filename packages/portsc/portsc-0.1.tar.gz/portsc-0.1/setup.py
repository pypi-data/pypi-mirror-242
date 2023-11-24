from setuptools import setup, find_packages

setup(
    name='portsc',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'argparse',  # argparse is part of the standard library, but including it here for clarity
    ],
    entry_points={
        'console_scripts': [
            'portsc=portsc:main',
        ],
    },
)
