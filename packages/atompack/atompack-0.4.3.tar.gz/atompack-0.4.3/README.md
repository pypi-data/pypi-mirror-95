# atompack
A flexible Python library for atomic structure generation.

## Installation

### Download from [PyPI](https://pypi.org/project/atompack/)

This is the best method for end users.

```bash
$ pip install atompack
```

### Build from source

This is the best method for contributors or anyone who is interested in modifying the code.

#### 1. Clone the source code with `git`:

```bash
$ git clone https://github.com/seatonullberg/atompack.git
$ cd atompack
```

#### 2. Download the dependencies and install as editable:

This step can be done with either `pipenv` or `pip`. I recommend using `pipenv`. If you're not familiar with the benefits of using `pipenv`, find out more about it here: https://pipenv-fork.readthedocs.io/en/latest/.

For `pipenv` users:

```bash
$ pipenv install
$ pipenv install --dev
```

For `pip` users:

```bash
$ pip install -r requirements.txt
$ pip install -e . [dev]
```

## Development

The project's [Makefile](Makefile) adds a few targets to help out with common development tasks.

* `make bench` - Run the benchmark suite.
* `make build` - Generate distribution files in `./dist`.
* `make clean` - Remove auto-generated files.
* `make document` - Build the documentation in `./docs`.
* `make format` - Enforce preferred code style.
* `make lint` - Run static analysis checks.
* `make publish` - Upload distribution files to PyPI.
* `make test` - Run the unit test suite.
