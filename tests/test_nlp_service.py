import pytest
import os
from unittest.mock import patch, MagicMock
from src.core.services.nlp_service import NLPService

@pytest.fixture
def nlp_service():
    """Fixture to initialize NLPService."""
    return NLPService()

def test_lemmatize_word_verb(nlp_service):
    """Test lemmatization of verbs."""
    assert nlp_service.lemmatize_word('running', 'VBG') == 'run'
    assert nlp_service.lemmatize_word('walked', 'VBD') == 'walk'

def test_lemmatize_word_adjective(nlp_service):
    """Test lemmatization of adjectives."""
    assert nlp_service.lemmatize_word('better', 'JJR') == 'good'

def test_get_tense(nlp_service):
    """Test tense identification."""
    tagged = [('I', 'PRP'), ('am', 'VBP'), ('running', 'VBG')]
    tense = nlp_service.get_tense(tagged)
    assert tense['present'] == 2
    assert tense['present_continuous'] == 1
    assert tense['past'] == 0

def test_process_text_empty(nlp_service):
    """Test processing of empty string."""
    assert nlp_service.process_text("") == []

@pytest.mark.django_db
@patch('src.core.services.nlp_service.finders.find')
def test_process_text_simple(mock_find, nlp_service):
    """Test processing of a simple sentence that yields keywords."""
    # Mock finders.find to pretend that the video file exists
    mock_find.return_value = '/fake/static/path/hello.mp4'
    
    words = nlp_service.process_text("hello there")
    assert "Hello" in words

@patch('src.core.services.nlp_service.VideoFileClip')
@patch('src.core.services.nlp_service.concatenate_videoclips')
@patch('src.core.services.nlp_service.finders.find')
def test_stitch_video(mock_find, mock_concat, mock_vfc, nlp_service):
    """Test video stitching logic"""
    # Mock the video file existence
    mock_find.return_value = '/fake/static/path/hello.mp4'
    
    # Mock MoviePy behaviors
    mock_clip = MagicMock()
    mock_concat.return_value = mock_clip
    
    words = ["hello", "bye"]
    
    # Run the stitch method
    result = nlp_service.stitch_video(words)
    
    # Should return a string path
    assert result is not None
    assert result.startswith('/static/videos/cache/stitched_')
    
    # Should have attempted to write the file
    mock_clip.write_videofile.assert_called_once()
