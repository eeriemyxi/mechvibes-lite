WORKDIR = .
PACKAGE_NAME = mechvibes

run:
	@python -m $(PACKAGE_NAME)

lint:
	@black $(WORKDIR)
	@ruff $(WORKDIR) --fix
	@pre-commit run --all-files
