from setuptools import setup

setup(
    name='pyipmi',
    version='0.1.0',
    packages=['pyipmi',
                'pyipmi.commands',
                'pyipmi.tools'],
    description='Wrapper for IPMI clients',
    author='Calxeda',
    classifiers=[
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2.7']
)
