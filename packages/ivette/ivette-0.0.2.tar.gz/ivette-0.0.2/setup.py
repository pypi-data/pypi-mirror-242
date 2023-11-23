from setuptools import setup

setup(
    name='ivette',
    version='0.0.2',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    py_modules=['ivette', 'package.IO_module', 'package.load_module', 'package.run_module', 'package.supabase_module'],  # Include 'runJob.py' as a module
    entry_points={
        'console_scripts': [
            'ivette=ivette:main',
        ],
    },
)