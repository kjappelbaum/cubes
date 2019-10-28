from distutils.core import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    
setup(
    name="Cubes",
    version="0.1dev",
    packages=["cube"],
    license="MIT",
     install_requires=requirements,
    long_description=open("README.md").read(),
)
