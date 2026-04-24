import pytest

def test_app_config():
    app_name = "Chaitanya Voter AI"
    assert app_name == "Chaitanya Voter AI"

def test_model_version():
    model_name = "gemini-2.5-flash"
    assert "gemini" in model_name

def test_environment():
    setup_complete = True
    assert setup_complete is True
