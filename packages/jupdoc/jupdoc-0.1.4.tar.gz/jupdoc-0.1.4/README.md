# JupDoc:  🚀 Automated data science documentation 🚀
[![PyPI Version](https://img.shields.io/pypi/v/jupdoc.svg)](https://pypi.org/project/jupdoc/)
[![Python Versions](https://img.shields.io/pypi/pyversions/jupdoc.svg)](https://pypi.org/project/jupdoc/)
[![License](https://img.shields.io/pypi/l/jupdoc.svg)](https://pypi.org/project/jupdoc/)
[![Downloads](https://pepy.tech/badge/jupdoc)](https://pepy.tech/project/jupdoc)
[![Downloads](https://pepy.tech/badge/jupdoc/month)](https://pepy.tech/project/jupdoc/month)
[![Downloads](https://pepy.tech/badge/jupdoc/week)](https://pepy.tech/project/jupdoc/week)

Documentation - that everybody wants it, but nobody gets it 😣! Is this all familiar to you? No longer.

JupDoc is a Python package that simplifies publishing documents from Jupyter Notebooks into multiple docx files (or other Quarto-supported formats) based on cell tags!

It embraces  __write once - publish for any <>__ where __<> = {person, role, time, format, location, style}__ paradigm!

## Table of Contents
- [About](#about)
- [Why JupDoc](#why-jupdoc)
- [What is the solution](#what-is-the-solution)
- [Core tenets](#core-tenets)
- [Features](#features)
- [Benefits](#benefits)
- [A new mindset](#a-new-mindset)
- [Installation](#installation)
- [Usage](#usage)
  - [Command Line Interface](#command-line-interface)
  - [Python API](#python-api)
- [To Do](#to-do)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contributing](#contributing)


-This package is still under development, and the documentation needs to be completed. There may be bugs, and the API may change._

## About
JupDoc is a light wrapper written in Python that simplifies publishing Jupyter notebooks into multiple docx files or other formats while applying view-based filters based on cell tags. It is based on [Quarto](https://quarto.org/).

with JupDoc
- Tag a notebook cell for a particular stakeholder
- Render the notebook into any format, filtered by the tag, for that stakeholder
- From a single notebook, create as many views/docs as needed
- Convert ipynb notebooks to docx, pdf, HTML tex, MD
- Upload the generated files to Google Drive (need service account)
- Maintain a single source of truth
- Automate document publishing
- No broken docs and constant remainders

## Why JupDoc
Different stakeholders (like Business Executives, Product Managers, and ML Scientists, among others) need information to act. Often, the format, content, and emphasis will be different. Further, they want documents that are:
- Accurate (and up to date)
- Available
- Accessible
- Reproducible
- Audutiable
- Versioned
- Serves their needs (w.r.t content, format, style, accessibility, shareability, etc.)

But, an ML Developer can only deliver on some fronts. Conventionally,
- Development and Documentation are not part of the same process. The toolset and mindset are different, even separated in time & space.
- Even a simple edit or change request requires a copy-and-paste from somewhere. If data or ask or both change, one must redo the documentation repeatedly. This is neither repeatable nor reproducible and also not sustainable.

As a result, a rigorous process oversight is needed for compliance. For example, a reporting manager may periodically check if the documentation is maintained and up to date as a part of the review processing. But this is not sustainable. We know it all too well.

## What is the solution
- Surprisingly simple. Just tag a notebook cell - who is it for?
- And take benefit of modern document publishing tools and workflows like Quarto, GitHub, GitHub actions

## Core tenets
- One content - many views
- Data + Code  + Content > should drive the documentation (format, style, purpose)
- Each stakeholder’s documentation need is just a view or a content rendering problem
- Publishing documentation =  Publishing code
- Use the same tools and mental models both for code and documents
- Single source of truth for any derived document
- Fix in only one place and only once.
- Physical and mental distance between Documentation and Code should be (close to) ZERO
- Set up once and automate subsequently
- Automate the publishing process
- No human oversight should be necessary for process compliance
- Commit code + documentation content > rendering must be automated

Result is JupDoc

## Features
- Define views using cell tags.
- Convert Jupyter Notebooks to docx, PDF, HTML, and more.
- Generate separate documents for each view.

## Benefits
Data-driven documents enable
- reproducibility, auditing, versioning, accuracy,
- When code blocks read data (e.g.,  ground truth vs. predictions), documents can be up to date also.

## A new mindset
- Writing documents is the same as writing code in the same place, space, and time.
- The stakeholder needs can be arranged in a hierarchy while authoring content via content inheritance. Executive Summary < Model Card < Solution Card < Full Report!
- To drive reports and visualization (of evaluation metrics), read data, and run code - so that whenever models/data are updated, metrics are also updated automatically!


## Installation

You can install JupDoc using pip:
```bash
pip install jupdoc
```
JupDoc is based on Quarto to convert ipynb files to other formats. The instructions to install Quarto can be found [here](https://quarto.org/docs/getting-started/installation.html).
## Usage
We support two ways to convert notebooks to docs. The first one is using the command line interface. The second one is using the Python API.

*Note:*
1. _The conversion of .ipynb is based on Quarto, and custom rending can be done by adding yaml config specific to notebooks as raw cells._
2. _All cells in the notebook should have tags (including markdown cells), and the tags should be a part of the config used to export._
3. _Quarto cheat sheet can be refered from [here](https://images.datacamp.com/image/upload/v1676540721/Marketing/Blog/Quarto_Cheat_Sheet.pdf). Details can be provided in the raw cell for customizations on reports._

### Command Line Interface
The command line interface can be used as follows:
```bash
jupdoc --config <config_file>
```
In case of the absence of the config file, the configs can be passed as command line arguments:
```bash
jupdoc --filename <filename> --tags <tags> --prefix <prefix> --output <output> --format <format> --upload <upload> --folder_url <folder_url> --creds_path <creds_path> --reference_docx <reference_docx>
```
The arguments are as follows:
- `filename`: The path to the notebook file.
- `tags`: The tags to be used for access control. Multiple tags can be passed as a comma-separated string.
- `prefix`: The prefix for the output files.
- `output`: The path to the output directory.
- `format`: File format to be exported to.
- `upload`: Upload the files to Google Drive.
- `folder_url`: The URL of the Google Drive folder to upload the files to.
- `creds_path`: The path to the Google Drive credentials file. (For Service Account)
- `reference_docx`: The path to the reference docx file. (Optional)
### Python API
The Python API can be used as follows:
```python
from jupdoc import convert
args = {
    "filename": "notebook.ipynb",
    "tags": ["tag1", "tag2"],
    "prefix": "prefix",
    "output": "output",
    "format": "docx",
    "upload": True,
    "folder_url": "https://drive.google.com/drive/folders/1Qlw7SxdPr4Ag1mKl4-cTrjgJPgZyzzYb?usp=drive_link",
    "creds_path": "creds.json"
    "reference_docx": "reference.docx"

}
convert(**args)
```
## To Do
1. Improve documentation. _WUP_
2. Add support for multiple cell tags.
3. GitHub Actions to generate reports on a push based on JupDoc configs.
## License
This project is licensed under the terms of the MIT license.
## Acknowledgements
This project is based on [Quarto](https://quarto.org/).
## Contributing
Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.
You can contribute in many ways:
- Report bugs.
- Fix bugs and submit pull requests.
- Write, clarify, or fix documentation.
- Suggest or add new features.
---
Made At [Wadhwani Institute for Artificial Intelligence](https://www.wadhwaniai.org/)
