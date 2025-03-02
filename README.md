# markmagic

convert files into markdown

Supported file types (and processing engine):
- docx ([python-docx](https://python-docx.readthedocs.io/en/latest/))
- eml ([email](https://docs.python.org/3/library/email.html))
- excel ([python-calamine](https://pypi.org/project/python-calamine/))
- pdf ([pypdf](https://pypdf.readthedocs.io/en/stable/index.html) / vision-language-models)
- pptx ([python-pptx](https://python-pptx.readthedocs.io/en/latest/index.html))


## Getting started
```py
from pathlib import Path
from markmagic import convert_any

with Path("tests/data/docx/msft_pr.docx").open("rb") as f:
    convert_any(filename="msft_pr.docx", file=f)
```

If you're interested in using vision language models to ocr a pdf

Create a .env file in the root directory
```
API_KEY="REPLACE"
```

```py
from pathlib import Path
from markmagic import convert_any

with Path("tests/data/pdf/msft_ar.pdf").open("rb") as f:
    settings = Settings(use_vlm=True)
    convert_any(filename="msft_ar.pdf", file=f, settings=settings)
```


## Design / Limitations
- markmagic only looks at the file extension to decide how to convert your files
- markmagic uses python-docx so cannot extract text from shapes / images (consider using [python-mammoth](https://github.com/mwilliamson/python-mammoth) + [markdownify](https://github.com/matthewwithanm/python-markdownify))

## Goals / Motivation
- Most consistent way of sending data to llms is in markdown
- Understand python tooling landscape and what a set of good lightweight options look like
- OCR is just neural nets so why not just use vision language models for ocr?
- OCRBenchmark https://github.com/open-compass/VLMEvalKit?tab=readme-ov-file

## TODOs:
- TBD
