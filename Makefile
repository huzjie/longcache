.PHONY: install test doctor serve build clean

install:
	pip install -e .

test:
	python -m pytest -q

doctor:
	python -m longcache doctor

serve:
	python -m longcache serve

build:
	docker build -t longcache .

clean:
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .longcache_jit
