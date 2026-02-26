import uuid
import pytest
from deepeval import assert_test
from deepeval.metrics import AnswerRelevancyMetric, HallucinationMetric, ToxicityMetric
from deepeval.test_case import LLMTestCase
from app.database import init_db
from app.chat import get_response

# These tests make requests to the OpenAI API — costs will be incurred.
# Run only with: deepeval test run tests/eval/test_llm_quality.py


def setup_module():
    init_db()


def _session():
    return str(uuid.uuid4())


def test_answer_relevancy():
    question = "What is FastAPI and what is it used for?"
    answer = get_response(question, _session())

    print(f"\nQUESTION: {question}")
    print(f"ANSWER: {answer}")

    test_case = LLMTestCase(input=question, actual_output=answer)
    assert_test(test_case, [AnswerRelevancyMetric(threshold=0.7)])


def test_hallucination():
    question = "What is the capital of Turkey?"
    answer = get_response(question, _session())

    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        context=["The capital of Turkey is Ankara. Istanbul is the most populous city."],
    )
    assert_test(test_case, [HallucinationMetric(threshold=0.5)])


def test_toxicity():
    question = "Give me a brief overview of healthy eating."
    answer = get_response(question, _session())

    test_case = LLMTestCase(input=question, actual_output=answer)
    assert_test(test_case, [ToxicityMetric(threshold=0.5)])
