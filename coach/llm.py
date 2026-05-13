"""LLM client abstraction."""
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate(
        self, prompt: str, *, system: str = None, temperature: float = 0.7
    ) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: The input prompt string.
            system: Optional system prompt for context.
            temperature: Sampling temperature (0.0-1.0).

        Returns:
            The generated text response.
        """
        raise NotImplementedError


class MockLLMClient(LLMClient):
    """Mock LLM client for testing - returns canned responses."""

    def generate(
        self, prompt: str, *, system: str = None, temperature: float = 0.7
    ) -> str:
        # If prompt contains "生成面试题" -> return mock question
        if "生成面试题" in prompt:
            # Extract topic info from prompt
            topic = "C++ 面试题"
            if "topic:" in prompt:
                start = prompt.find("topic:") + len("topic:")
                end = prompt.find(",", start)
                if end == -1:
                    end = prompt.find("\n", start)
                    if end == -1:
                        end = len(prompt)
                topic = prompt[start:end].strip()
            elif "topic_name" in prompt:
                start = prompt.find("topic_name") + len("topic_name")
                end = prompt.find(",", start)
                if end == -1:
                    end = prompt.find("\n", start)
                    if end == -1:
                        end = len(prompt)
                topic = prompt[start:end].strip().strip('"').strip("'")

            return f"请解释一下{topic}的实现原理和应用场景？"

        # If prompt contains "参考答案" -> return mock answer
        if "参考答案" in prompt:
            return "虚函数通过 vtable 实现多态。每个对象有一个 vptr 指向 vtable，运行时通过 vtable 动态绑定。"

        # If prompt contains "评估" -> return mock evaluation JSON
        if "评估" in prompt or "面试官" in prompt:
            return '''{
                "rating": "okay",
                "score_total": 0.65,
                "correctness": 0.7,
                "completeness": 0.6,
                "depth": 0.6,
                "clarity": 0.7,
                "code_accuracy": 0.6,
                "edge_case_awareness": 0.5,
                "missing_points": ["虚函数析构函数"],
                "wrong_points": [],
                "weakness_tags": ["vtable"],
                "hallucinated_points": [],
                "evaluator_confidence": 0.8
            }'''

        # Default response
        return "Mock response"


class OpenAICompatibleClient(LLMClient):
    """OpenAI-compatible API client (for later Task 9)."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = "gpt-4o",
    ):
        """Initialize the OpenAI-compatible client.

        Args:
            api_key: API key for authentication.
            base_url: Base URL of the API endpoint.
            model: Model name to use.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, *, temperature: float = 0.7) -> str:
        """Generate a response using the OpenAI-compatible API."""
        # TODO: implement in Task 9
        raise NotImplementedError("OpenAICompatibleClient will be implemented in Task 9")