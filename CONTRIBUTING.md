# Contributing
We use [uv](https://docs.astral.sh/uv/) to manage this Python package.

## Install Development Dependencies
```console
user:~$ uv sync --extra dev
```

`uv` will create a virtual environment for you under `.venv/` in the
source tree, by default. It has been ignored in the `.gitignore` and `.dockerignore` files
for you already. Also see [Development Shell](#development-shell).

## Editing/Expanding Documentation
Serve the documentation by doing:
```console
user:~$ uv run mkdocs serve
```

Then go to the address that it is serving on. It should reload the page
automatically on any change under `/docs` folder in the source tree.

> [!NOTE] 
> You need to sync with the `dev` dependency group before attempting
> this as shown [here](#install-development-dependencies).

## Running the Package
```console
user:~$ uv run mvibes --help
```

## Development Shell
You can do `uv run <shell-executable-here>` to open a shell with the right
environment setup. Examples:
* `uv run powershell`
* `uv run cmd`
* `uv run bash`
* `uv run fish`

In that shell, you should have the right `mvibes` and `mkdocs` executables from
the `.venv/bin` folder.
