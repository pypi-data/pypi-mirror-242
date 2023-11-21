from setuptools import setup, find_packages

setup(
    name='kwargsyay',
    version='1.0.0',
    author='Asher Cohen',
    author_email='nono@yay.com',
    description='A helper for kwargs arguements in python.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

