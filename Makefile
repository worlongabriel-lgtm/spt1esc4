.PHONY: install run test clean help

# Default Python executable
PYTHON := python3
VENV_PYTHON := .venv/bin/python
VENV_ACTIVATE := .venv/bin/activate

# Check if virtual environment exists
VENV_EXISTS := $(shell test -d .venv && echo "yes" || echo "no")

# Use virtual environment Python if it exists, otherwise use system Python
ifeq ($(VENV_EXISTS), yes)
	PYTHON_CMD := $(VENV_PYTHON)
else
	PYTHON_CMD := $(PYTHON)
endif

# Install dependencies
install:
	@echo "Installing dependencies..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv .venv; \
	fi
	@echo "Activating virtual environment and installing packages..."
	@. $(VENV_ACTIVATE) && pip install -r requirements.txt
	@echo "Installation complete!"

# Run the API server
run:
	@echo "Starting API server..."
	@if [ "$(VENV_EXISTS)" = "yes" ]; then \
		. $(VENV_ACTIVATE) && $(VENV_PYTHON) -m uvicorn app.main:app --reload; \
	else \
		echo "Warning: No virtual environment found. Using system Python."; \
		$(PYTHON_CMD) -m uvicorn app.main:app --reload; \
	fi

# Run tests
test:
	@echo "Running tests..."
	@if [ "$(VENV_EXISTS)" = "yes" ]; then \
		. $(VENV_ACTIVATE) && $(VENV_PYTHON) -m pytest -q; \
	else \
		echo "Warning: No virtual environment found. Using system Python."; \
		$(PYTHON_CMD) -m pytest -q; \
	fi

# Run tests with verbose output
test-verbose:
	@echo "Running tests with verbose output..."
	@if [ "$(VENV_EXISTS)" = "yes" ]; then \
		. $(VENV_ACTIVATE) && $(VENV_PYTHON) -m pytest -v; \
	else \
		echo "Warning: No virtual environment found. Using system Python."; \
		$(PYTHON_CMD) -m pytest -v; \
	fi

# Clean up virtual environment and cache files
clean:
	@echo "Cleaning up..."
	@rm -rf .venv
	@rm -rf __pycache__
	@rm -rf .pytest_cache
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "Cleanup complete!"

# Show help
help:
	@echo "Available commands:"
	@echo "  install      - Create virtual environment and install dependencies"
	@echo "  run          - Start the API server with auto-reload"
	@echo "  test         - Run tests quietly"
	@echo "  test-verbose - Run tests with verbose output"
	@echo "  clean        - Remove virtual environment and cache files"
	@echo "  help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make install"
	@echo "  make run"
	@echo "  make test"
	@echo ""
	@echo "Note: Commands will automatically use the virtual environment if it exists."
