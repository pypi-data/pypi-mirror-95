#     datasets-from-pdfs - Convert single or mass PDFs to datasets
#     Copyright (C) 2021  Daniel Whitten - danieljwhitten@gmail.com

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datasets-from-pdfs",
    version="0.0.7",
    author="Daniel Whitten",
    author_email="danieljwhitten@gmail.com",
    description=("A tool to convert single or mass PDFs to datasets for",
    "language analysis, including a toolbox of text and NLP pre-processing options"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/danieljwhitten/datasets-from-pdfs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+) ",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "datasets-from-pdfs = datasets_from_pdfs.readpdf:main"
        ]
    },
)
