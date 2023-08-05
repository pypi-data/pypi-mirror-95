# datapusher

Overvåker folder og sender data i nye/endrede filer som json til sprint-webserver.

## Overvåke folder for endringer i filer

```
% pip install sprint-datapusher
% sprint_datapusher --help                                 
Usage: sprint_datapusher [OPTIONS] URL

  CLI for monitoring directory and send content of files as json to
  webserver URL.

  URL is the url to a webserver exposing an endpoint accepting your json.

  To stop the datapusher, press Control-C.

Options:
  --version                  Show the version and exit.
  -d, --directory DIRECTORY  Relative path to the directory to watch
                             [default: /home/stigbd/src/heming-
                             langrenn/sprint-excel/datapusher]

  -h, --help                 Show this message and exit.

```

## Development
### Requirements
- [pyenv](https://github.com/pyenv/pyenv-installer)
- [pipx](https://github.com/pipxproject/pipx)
- [poetry](https://python-poetry.org/)
- [nox](https://nox.thea.codes/en/stable/)
- [nox-poetry](https://github.com/cjolowicz/nox-poetry)

```
% curl https://pyenv.run | bash
% pyenv install 3.9.1
% pyenv install 3.7.9
% python3 -m pip install --user pipx
% python3 -m pipx ensurepath
% pipx install poetry
% pipx install nox
% pipx inject nox nox-poetry
```

### Install
```
% git clone https://github.com/heming-langrenn/sprint-excel.git
% cd sprint-excel/datapusher
% pyenv local 3.9.1 3.7.9
% poetry install
```
### Run all sessions
```
% nox
```
### Run all tests with coverage reporting
```
% nox -rs tests
```
## Run cli script
```
% poetry shell
% sprint_datapusher --help
```
Alternatively you can use `poetry run`:
```
% poetry run sprint_datapusher --help
```
