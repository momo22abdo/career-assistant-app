import pytest
from src.ai_utils import match_skills, gap_analysis, chatbot_query
import os

# Fixture to mock API key
@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    monkeypatch.setenv("RAPIDAPI_KEY", "test_key")

def test_match_skills():
    user_skills = ["Python", "SQL"]
    matches = match_skills(user_skills)
    assert len(matches) <= 5
    assert all(isinstance(m[1], float) for m in matches)
    assert all(m[1] >= 0 and m[1] <= 100 for m in matches)

def test_gap_analysis():
    user_skills = ["Python", "SQL"]
    target_career = list(careers.keys())[0] if careers else pytest.skip("No careers fetched")
    missing = gap_analysis(user_skills, target_career)
    assert isinstance(missing, list)

def test_chatbot_query():
    response = chatbot_query("Which career suits me if I love AI?")
    assert isinstance(response, str)
    assert "AI Engineer" in response or "Machine Learning" in response

# Note: analyze_resume requires a PDF; test manually
# Run with: pytest tests/test_ai_utils.py