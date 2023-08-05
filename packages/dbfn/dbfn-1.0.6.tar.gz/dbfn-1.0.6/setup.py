from setuptools import setup

with open("README.md", "r") as file: description = file.read()
    
setup(
    name="dbfn",
    version="1.0.6",    
    description="Discord Bot Functions. Includes reaction books with more feature to be added",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/judev1/dbfn",
    author="Jude BC",
    author_email="jude.version1.0@gmail.com",
    license="BSD 2-clause",
    packages=["dbfn"],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
