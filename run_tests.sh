#!/bin/bash

# Run tests with coverage
echo "Running tests with coverage..."
pytest --cov=app --cov-report=term-missing --cov-report=html -v

# Show coverage summary
echo ""
echo "Coverage report generated in htmlcov/index.html"
echo "Run 'open htmlcov/index.html' to view detailed HTML report"