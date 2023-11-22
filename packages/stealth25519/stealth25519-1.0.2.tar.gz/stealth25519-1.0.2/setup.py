from setuptools import setup, find_packages

setup(
    name='stealth25519',
    version='1.0.2',
    description='The Stealth25519 Python package provides functionality for the generation, verification, and signing of stealth addresses using the standard ed25519 algorithm with the ECDH protocol.',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    entry_points={
        'console_scripts': [],
    },
)
