# Development notes

Live on <https://pypi.org/project/merrymake/>

The README.md is published on the page as well.

## Releasing

`my-token` is generated from <https://pypi.org/manage/account/>

```shell
$ export POETRY_PYPI_TOKEN_PYPI=my-token
$ make publish
# .. or interactively
$ make run
python@5789a6d613c4:/mnt/app$ poetry build
python@5789a6d613c4:/mnt/app$ export POETRY_PYPI_TOKEN_PYPI=my-token
python@5789a6d613c4:/mnt/app$ poetry publish
```

```shell
$ make run
python $ python3 ./app.py hello '{ "hello": "world" }'
```

## TODO

Figure out how `__init__.py` needs to look.
It works right now but.. it's a bit magic.
Also figure out the imports for `MerryMimetypes.txt` and
`from merrymake.merrymimetypes import MerryMimetypes`.
Like, half the time it's not needed :shrug:
