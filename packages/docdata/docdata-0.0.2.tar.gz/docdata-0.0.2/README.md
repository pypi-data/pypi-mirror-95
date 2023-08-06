<!--
<p align="center">
  <img src="docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  Docdata
</h1>

<p align="center">
    <a href="https://github.com/cthoyt/docdata/actions?query=workflow%3ATests">
        <img alt="Tests" src="https://github.com/cthoyt/docdata/workflows/Tests/badge.svg" />
    </a>
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-python--package-yellow" /> 
    </a>
    <a href="https://pypi.org/project/docdata">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/docdata" />
    </a>
    <a href="https://pypi.org/project/docdata">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/docdata" />
    </a>
    <a href="https://github.com/cthoyt/docdata/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/docdata" />
    </a>
    <a href='https://docdata.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/docdata/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://zenodo.org/badge/latestdoi/340714491">
        <img src="https://zenodo.org/badge/340714491.svg" alt="DOI">
    </a>
</p>

Add structured information to the end of your python docstrings.

## 💪 Getting Started

Use this package to add structured data to your docstrings in YAML. Just add a `---` delimiter at the bottom, and the
rest is parsed as YAML.

```python
from docdata import parse_docdata, get_docdata


@parse_docdata
class MyClass:
    """This is my class.

    ---
    author: Charlie
    motto:
    - docs
    - are
    - cool
    """


assert {'author': 'Charlie', 'motto': ['docs', 'are', 'cool']} == get_docdata(MyClass)
```

If you want to get the data directly, go for `MyClass.__docdata__`. If you want to change the way docdata is parsed,
like changing the delimiter, use keyword arguments like in:

```python
from docdata import parse_docdata, get_docdata


@parse_docdata(delimiter='****')
class MyClass:
    """This is my class.

    ****
    author: Charlie
    motto:
    - docs
    - are
    - cool
    """


assert {'author': 'Charlie', 'motto': ['docs', 'are', 'cool']} == get_docdata(MyClass)
```

## ⬇️ Installation

The most recent release can be installed from
[PyPI](https://pypi.org/project/docdata/) with:

```bash
$ pip install docdata
```

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/cthoyt/docdata.git
```

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/cthoyt/docdata.git
$ cd docdata
$ pip install -e .
```

## ⚖️ License

The code in this package is licensed under the MIT License.

## 🙏 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.rst](https://github.com/cthoyt/docdata/blob/master/CONTRIBUTING.rst) for more information on getting
involved.

## 🍪 Cookiecutter Acknowledgement

This package was created with [@audreyr](https://github.com/audreyr)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-python-package](https://github.com/cthoyt/cookiecutter-python-package) template.

## 🛠️ Development

The final section of the README is for if you want to get involved by making a code contribution.

### ❓ Testing

After cloning the repository and installing `tox` with `pip install tox`, the unit tests in the `tests/` folder can be
run reproducibly with:

```shell
$ tox
```

Additionally, these tests are automatically re-run with each commit in
a [GitHub Action](https://github.com/cthoyt/docdata/actions?query=workflow%3ATests).
