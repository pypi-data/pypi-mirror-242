from setuptools import setup

# Read deps
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='ivette',
    version='0.0.5',
    description='Python client for Ivette Computational chemistry and Bioinformatics project',
    author='Eduardo Bogado',
    py_modules=['ivette', 'package.IO_module', 'package.load_module', 'package.run_module', 'package.supabase_module'],  # Include 'ivette.py' as a module
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ivette=ivette:main',
        ],
    },
)

# After installation the next command should be run:
'''
echo "
# IVETTE CLI PATH
export PATH=\$PATH:/home/$USER/.local/bin" >> ~/.bashrc
sudo ~/.bashrc
'''