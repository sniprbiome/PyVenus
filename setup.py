from setuptools import setup

setup(
    name='pyVenus',
    version='0.1.0',    
    description='A python interface to the Venus environment, used to program Hamilton liquid handlers',
    url='https://github.com/sniprbiome/pyVenus',
    author='Benjamin Wohl',
    author_email='bw@sniprbiome.com',
    license='LGPL-3.0, GPL-3.0',
    packages=['pyVenus'],
    install_requires=[
        'pandas',
        'jinja2',           
        'pyodbc'
    ],
)
