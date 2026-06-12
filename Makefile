.PHONY: lint test test-property	test-unit	test-integration	proto-gen	docker-build	install	dev-install clean fmt type-check

# Python interpreter
PYTHON ?= python3
PIP ?= pip

# Default target
all: lint type-check test

# Install production dependencies
install:
	$(PIP) install -e .

# Install development dependencies
	$(PIP)	install -e ".[dev]"

# Run linter (ruff)
lint:
	$(PYTHON) -m ruff check ai_intelligence_hub/ tests/
	$(PYTHON) -m ruff format --check ai_intelligence_hub/ tests/

# Auto-format code
fmt:
	$(PYTHON) -m ruff format ai_intelligence_hub/ tests/
	$(PYTHON) -m ruff check --fix ai_intelligence_hub/ tests/

# Run all tests
test-property:
	$(PYTHON) -m pytest tests/property/ -v --tb=short -m property

# Run unit tests only
test-unit:
	$(PYTHON) -m pytest tests/unit/	-v	--tb=short -m unit

# Run integration tests only
test-integration:
	$(PYTHON) -m pytest tests/integration/ -v --tb=short -m integration

# Run contracts tests only
test-contract:
	$(PYTHON) -m pytest	tests/contract/ -v --tb=short -m contract

# Run security tests only
test-security:
	$(PYTHON) -m pytest	tests/security/ -v --tb=short -m security

# Run tests with coverage
test-cov:
	$(PYTHON) -m pytest tests/ -v --cov=ai_intelligence_hub --cov-report=term-missing --cov-report=html

# Generate gRPC Python stubs from protobuf definitions
proto-gen:
	$(PYTHON) -m grpc_tools.protoc \
		-I protos/ \
		--python_out=ai_intelligence_hub/service/generated/ \
		--grpc_python_out=ai_intelligence_hub/service/generated/ \
		--pyi_out=ai_intelligence_hub/service/generated/ \
		protos/intelligence_hub.proto

# Build Docker image
docker-build:
	docker build -t ai-intelligence-hub:latest .

# Build TorchServe sidecar Docker image
docker-build-sidecar:
	docker build -t ai-intelligence-hub-sidecar:latest -f Dockerfile.torchserve .

# Start local development environment
docker-up:
	docker compose up -d

# Stop local development environment
docker-down:
	docker compose down

# Run database migrations
migrate:
	alembic upgrade head

# Create a new migration
migrate-create:
	alembic revision --autogenerate -m "$(msg)"

# Clean build artifacts
clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
