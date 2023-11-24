from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.24'
DESCRIPTION = 'Read/Write PDF Text, Forms, and Metadata.'
LONG_DESCRIPTION = 'A 2023+ package for reading text, metadata, and forms from PDFs with the ability to edit metadata and forms data. Based on prior work by pdfrw and pypdf2 updated for PDF forms changes in latter versions. <p>Kinetic PDF is designed to work with Kinetic Forms and Kinetic Email to provide workflows related to processing PDF Forms.'

# Setting up
setup(
    name="kineticpdf",
    version=VERSION,
    author="Kinetic Seas (Ed Honour / Joe Lehman), pdfrw, pypdf2",
    author_email="<edward.honour@kineticseas.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pycryptodome', 'pikepdf'],
    keywords=['python', 'PDF', 'PDFForms', 'extract PDF text', 'extract PDF Form fields'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
