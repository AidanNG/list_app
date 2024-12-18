from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="list-app",
    version="0.1.0",
    author="Aidan NG",
    author_email="aidanngow@gmail.com",
    description="A simple list application built with Python and customTkinter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AidanNG/list-app",
    packages=find_packages(),
    install_requires=[
        "customtkinter",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "gui_scripts": [
            "list-app=list_app.main:main",
        ],
    },
)