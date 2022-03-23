from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(".. include:: toc.rst\n\n", "")

# The lines below can be parsed by `docs/conf.py`.
name = "datatask"
version = "0.2.0"

setup(
    name=name,
    version=version,
    packages=[name,],
    install_requires=[],
    license="MIT",
    url="https://github.com/nthparty/datatask",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="General-purpose data structure and representation format "+\
                "for tasks (stand-alone or part of a larger data workflow) "+\
                "that involve multiple data resources.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
)
