# test_project.py
import pytest
import json
import main

def test_is_valid_url():
    assert main.is_valid_url("https://www.cnn.com") == True
    assert main.is_valid_url("invalid_url") == False

def test_fetch_news_headlines():
    headlines = main.fetch_news_headlines("https://www.cnn.com")
    assert isinstance(headlines, list)
    assert len(headlines) > 0

def test_save_to_json(tmp_path):
    data = [{"title": "Test", "link": "https://www.cnn.com/test"}]
    filepath = tmp_path / "test.json"
    main.save_to_json(data, filepath)
    assert filepath.exists()
    with open(filepath, 'r') as f:
        saved_data = json.load(f)
    assert saved_data == data
