INPUT_EVENT_ID = 4
SOURCE_DIR = .

bai:
	isort . && black .

run:
	python $(SOURCE_DIR) $(INPUT_EVENT_ID)
