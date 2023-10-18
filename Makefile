INPUT_EVENT_ID = 4
WORKDIR = .
PACKAGE_NAME = mechvibes

run:
	@python -m $(PACKAGE_NAME)

lint:
	@ruff $(WORKDIR) --fix
	@pre-commit run --all-files
