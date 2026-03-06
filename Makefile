.PHONY: check-venv
check-venv:
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "Error:仮想環境内で実行してください"; \
		exit 1; \
	fi

.PHONY: install
install: check-venv
	pip install -r requirements.txt

.PHONY: run
run:
	python3 a_maze_ing.py config.txt

.PHONY: debug
debug:
	python3 -m pdb a_maze_ing.py config.txt

.PHONY: clean
clean:
	find . -name "*.pyc" -type f -delete -print
	find . -type d  -name "__pycache__" -delete -print
	rm -rf .mypy_cache
	rm -rf dist/
	rm -rf mazegen.egg-info/

.PHONY: lint
lint:
	-flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: build
build: check-venv
	python3 -m build

.PHONY: lint-strict
lint-strict:
	-flake8 .
	mypy . --strict
