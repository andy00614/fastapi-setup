"""
Test LLM module functionality
"""
import pytest
from unittest.mock import Mock, patch
from app.llm import (
    resolve_model, 
    normalize_messages, 
    to_lc_messages,
    generate_sync,
    sse_event
)
from app.schemas.llm import GenerateRequest, Message


class TestModelResolution:
    """Test model resolution and aliasing"""
    
    def test_resolve_known_alias(self):
        """Test resolution of known model aliases"""
        provider, model = resolve_model("gpt-4o-mini")
        assert provider == "openai"
        assert model == "gpt-4o-mini"
        
        provider, model = resolve_model("gemini-flash")
        assert provider == "google"
        assert model == "gemini-1.5-flash"
    
    def test_resolve_slash_format(self):
        """Test resolution of provider/model format"""
        provider, model = resolve_model("openai/custom-model")
        assert provider == "openai"
        assert model == "custom-model"
    
    def test_resolve_unknown_model(self):
        """Test that unknown models raise ValueError"""
        with pytest.raises(ValueError, match="未知模型名"):
            resolve_model("unknown-model")


class TestMessageNormalization:
    """Test message normalization functionality"""
    
    def test_normalize_with_messages(self):
        """Test normalization when messages are provided"""
        req = GenerateRequest(
            model_name="gpt-4o-mini",
            messages=[Message(role="user", content="Hello")]
        )
        normalized = normalize_messages(req)
        assert len(normalized) == 1
        assert normalized[0]["role"] == "user"
        assert normalized[0]["content"] == "Hello"
    
    def test_normalize_with_input(self):
        """Test normalization when only input is provided"""
        req = GenerateRequest(
            model_name="gpt-4o-mini",
            input="Hello"
        )
        normalized = normalize_messages(req)
        assert len(normalized) == 1
        assert normalized[0]["role"] == "user"
        assert normalized[0]["content"] == "Hello"
    
    def test_normalize_no_input(self):
        """Test that error is raised when no input is provided"""
        req = GenerateRequest(model_name="gpt-4o-mini")
        with pytest.raises(ValueError, match="messages 或 input 至少提供一个"):
            normalize_messages(req)


class TestLangchainConversion:
    """Test conversion to Langchain message format"""
    
    def test_convert_user_message(self):
        """Test conversion of user message"""
        messages = [{"role": "user", "content": "Hello"}]
        lc_messages = to_lc_messages(messages)
        assert len(lc_messages) == 1
        assert lc_messages[0].content == "Hello"
    
    def test_convert_system_message(self):
        """Test conversion of system message"""
        messages = [{"role": "system", "content": "You are helpful"}]
        lc_messages = to_lc_messages(messages)
        assert len(lc_messages) == 1
        assert lc_messages[0].content == "You are helpful"
    
    def test_convert_mixed_messages(self):
        """Test conversion of mixed message types"""
        messages = [
            {"role": "system", "content": "You are helpful"},
            {"role": "user", "content": "Hello"}
        ]
        lc_messages = to_lc_messages(messages)
        assert len(lc_messages) == 2
        assert lc_messages[0].content == "You are helpful"
        assert lc_messages[1].content == "Hello"


class TestGenerateSync:
    """Test synchronous generation"""
    
    @patch('app.llm.ChatOpenAI')
    def test_generate_sync_openai(self, mock_openai):
        """Test synchronous generation with OpenAI"""
        # Setup mock
        mock_response = Mock()
        mock_response.content = "Test response"
        mock_response.finish_reason = "stop"
        mock_response.usage_metadata = {
            "input_tokens": 10,
            "output_tokens": 20,
            "total_tokens": 30
        }
        mock_openai.return_value.invoke.return_value = mock_response
        
        # Mock dict conversion
        mock_response.__iter__ = Mock(return_value=iter([]))
        
        # Test
        req = GenerateRequest(
            model_name="gpt-4o-mini",
            input="Hello"
        )
        
        response = generate_sync(req)
        
        # Assertions
        assert response.provider == "openai"
        assert response.model == "gpt-4o-mini"
        assert len(response.choices) == 1
        assert response.choices[0].content == "Test response"
        assert response.usage.prompt_tokens == 10
        assert response.usage.completion_tokens == 20
        assert response.usage.total_tokens == 30
    
    @patch('app.llm.ChatGoogleGenerativeAI')
    def test_generate_sync_gemini(self, mock_gemini):
        """Test synchronous generation with Gemini"""
        # Setup mock
        mock_response = Mock()
        mock_response.content = "Gemini response"
        mock_response.finish_reason = "stop"
        mock_response.usage_metadata = {
            "prompt_token_count": 15,
            "candidates_token_count": 25,
            "total_token_count": 40
        }
        mock_gemini.return_value.invoke.return_value = mock_response
        
        # Mock dict conversion
        mock_response.__iter__ = Mock(return_value=iter([]))
        
        # Test
        req = GenerateRequest(
            model_name="gemini-flash",
            input="Hello"
        )
        
        response = generate_sync(req)
        
        # Assertions
        assert response.provider == "google"
        assert response.model == "gemini-1.5-flash"
        assert len(response.choices) == 1
        assert response.choices[0].content == "Gemini response"
        assert response.usage.prompt_tokens == 15
        assert response.usage.completion_tokens == 25
        assert response.usage.total_tokens == 40
    
    def test_generate_sync_unsupported_provider(self):
        """Test that unsupported provider raises error"""
        req = GenerateRequest(
            model_name="anthropic/claude-3",
            input="Hello"
        )
        
        with pytest.raises(ValueError, match="暂不支持的 provider"):
            generate_sync(req)


class TestSSEEvent:
    """Test SSE event formatting"""
    
    def test_sse_event_formatting(self):
        """Test SSE event is properly formatted"""
        event = sse_event("test", {"message": "hello"})
        assert "event: test\n" in event
        assert 'data: {"message": "hello"}\n\n' in event
    
    def test_sse_event_with_unicode(self):
        """Test SSE event with unicode characters"""
        event = sse_event("test", {"message": "你好"})
        assert "event: test\n" in event
        assert '"message": "你好"' in event