from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="cube",
    version="0.1dev",
    packages=find_packages(),
    license="MIT",
    install_requires=requirements,
    extras_require={
        "develop": ["pytest", "pre-commit", "black", "prospector", "pylint"]
    },
    long_description=open("README.md").read(),
)
