app=python-service-library

poetry-container=docker run --rm -it \
		-w /mnt/app \
		-v $(shell pwd):/mnt/app \
		-v $(app)-cache:/home/python/.cache \
		merrymake/python-poetry

poetry=$(poetry-container) poetry

.PHONY:
build:
	docker build -t merrymake/python-poetry .

.PHONY:
run: .install
	$(poetry-container) bash

.install:
	make install
	touch .install

.PHONY:
install:
	$(poetry) install

.PHONY:
black: .install
	$(poetry) run black ./src/ ./tests/

.PHONY:
publish: .install guard-POETRY_PYPI_TOKEN_PYPI
	docker run --rm -it \
		-w /mnt/app \
		-v $(shell pwd):/mnt/app \
		-v $(app)-cache:/home/python/.cache \
		-e POETRY_PYPI_TOKEN_PYPI \
		merrymake/python-poetry sh -c "poetry build && poetry publish"

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi
