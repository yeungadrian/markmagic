# markmagic

convert files into markdown

Supported file types (and processing engine):
- docx ([python-docx](https://python-docx.readthedocs.io/en/latest/))
- excel ([python-calamine](https://pypi.org/project/python-calamine/))
- pdf ([pypdf](https://pypdf.readthedocs.io/en/stable/index.html))
- eml ([email](https://docs.python.org/3/library/email.html))

## Getting started
```py
from pathlib import Path
from markmagic import convert_any

with Path("tests/data/docx/msft_pr.docx").open("rb") as f:
    convert_any(filename= "msft_pr.docx", content=f)
```

## Design / Limitations
- markmagic only looks at the file extension to decide how to convert your files
- markmagic uses python-docx so cannot extract text from shapes / images (consider using [python-mammoth](https://github.com/mwilliamson/python-mammoth) + [markdownify](https://github.com/matthewwithanm/python-markdownify))
- markmagic uses pypdf, so no images are processed / layout is not considered

## Goals / Motivation
- Most consistent way of sending data to llms is in markdown
- Understand python tooling landscape and what a set of good lightweight options look like
