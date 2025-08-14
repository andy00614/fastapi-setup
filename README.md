# Unified LLM API Gateway 🚀

A high-performance, unified API gateway for multiple Large Language Model (LLM) providers. Built with FastAPI, this service provides a single interface to interact with OpenAI GPT and Google Gemini models.

## ✨ Features

- **Multi-Provider Support**: Seamlessly switch between OpenAI and Google Gemini models
- **Unified Interface**: Single API endpoint for all LLM providers
- **Streaming Support**: Real-time streaming responses via Server-Sent Events (SSE)
- **Model Aliasing**: Use simplified model names (e.g., `gpt-4o-mini`, `gemini-flash`)
- **Async/Await**: Built on FastAPI for high-performance async operations
- **Type Safety**: Full Pydantic validation for requests and responses
- **Comprehensive Testing**: Pytest with coverage reporting

## 🎯 Supported Models

### OpenAI
- `gpt-4o-mini` - Fast and cost-effective model
- `gpt-4o` - Most capable GPT-4 model

### Google Gemini
- `gemini-flash` - Gemini 1.5 Flash (fast responses)
- `gemini-pro` - Gemini 1.5 Pro (advanced capabilities)

### Custom Models
You can also use the format `provider/model-name` for any supported provider.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- OpenAI API Key
- Google API Key (for Gemini)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/unified-llm-api.git
cd unified-llm-api
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your API keys
```

### Environment Variables

Create a `.env` file with:
```env
PROJECT_NAME=Unified LLM API
VERSION=0.1.1
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite+aiosqlite:///./app.db

OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key
```

### Running the Server

```bash
# Development mode
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📡 API Usage

### Synchronous Generation

```bash
curl -X POST "http://localhost:8000/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "gpt-4o-mini",
    "input": "Explain quantum computing in simple terms",
    "temperature": 0.7
  }'
```

### Using Messages Format

```bash
curl -X POST "http://localhost:8000/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "gemini-flash",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant"},
      {"role": "user", "content": "What is machine learning?"}
    ],
    "temperature": 0.5
  }'
```

### Streaming Response

```bash
curl -X POST "http://localhost:8000/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "gpt-4o",
    "input": "Write a short story",
    "stream": true
  }'
```

## 📊 API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

Run tests with coverage:
```bash
# Quick test run
./run_tests.sh

# Detailed with coverage
pytest --cov=app --cov-report=term-missing --cov-report=html -v

# View HTML coverage report
open htmlcov/index.html
```

Current test coverage: **81.33%**

## 📁 Project Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── api.py          # API routes
│   ├── core/
│   │   └── config.py           # Configuration
│   ├── db/
│   │   ├── base.py            # Database base
│   │   └── session.py         # Database session
│   ├── schemas/
│   │   └── llm.py             # Pydantic models
│   ├── llm.py                 # LLM integration logic
│   └── main.py                # FastAPI application
├── tests/
│   ├── conftest.py            # Test fixtures
│   ├── test_config.py         # Configuration tests
│   ├── test_llm.py            # LLM module tests
│   └── test_main.py           # API endpoint tests
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── pytest.ini                 # Pytest configuration
├── .coveragerc               # Coverage configuration
└── run_tests.sh              # Test runner script
```

## 🔧 Development

### Adding New Providers

1. Add provider configuration in `app/llm.py`:
```python
ALIASES["new-model"] = ("provider", "actual-model-name")
```

2. Implement provider-specific sync/stream functions:
```python
def _run_newprovider_sync(real_model: str, messages: List[dict], ...):
    # Implementation
```

3. Update the main generate functions to handle the new provider.

### Code Style

The project follows Python best practices:
- Type hints for all functions
- Async/await for I/O operations
- Comprehensive error handling
- Clear separation of concerns

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- LLM integrations via [LangChain](https://langchain.com/)
- Testing with [Pytest](https://pytest.org/)

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: Remember to keep your API keys secure and never commit them to version control!