INPUT_EVENT_ID = 4
PACKAGE_NAME = mechvibes

bai:
	isort . && black .

run:
	python -m $(PACKAGE_NAME) $(INPUT_EVENT_ID)
