from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="plomberie",
    version="0.0.4",
    author="Aaron Mamparo",
    author_email="aaronmamparo@gmail.com",
    description="Create simple pipelines by defining task dependencies in code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amamparo/plomberie",
    packages=find_packages("."),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">= 3.8",
)
