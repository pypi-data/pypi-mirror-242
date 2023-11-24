from setuptools import setup

name = "types-pycocotools"
description = "Typing stubs for pycocotools"
long_description = '''
## Typing stubs for pycocotools

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`pycocotools`](https://github.com/ppwwyyxx/cocoapi) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`pycocotools`.

This version of `types-pycocotools` aims to provide accurate annotations
for `pycocotools==2.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/pycocotools. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `81633e27097228a8a7eb0f963c62916ecea78abc` and was tested
with mypy 1.7.1, pyright 1.1.334, and
pytype 2023.11.21.
'''.lstrip()

setup(name=name,
      version="2.0.0.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pycocotools.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['pycocotools-stubs'],
      package_data={'pycocotools-stubs': ['__init__.pyi', 'coco.pyi', 'cocoeval.pyi', 'mask.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      python_requires=">=3.7",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
