INPUT_EVENT_ID = 4
PACKAGE_NAME = mechvibes

run:
	python -m $(PACKAGE_NAME)

lint:
	pre-commit run --all-files
