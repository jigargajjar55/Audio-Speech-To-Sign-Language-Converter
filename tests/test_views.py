import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User
from src.core.models import TranslationHistory

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword123')

@pytest.mark.django_db
def test_dashboard_requires_login(client):
    """Ensure the dashboard requires authentication."""
    url = reverse('dashboard')
    response = client.get(url)
    
    # Should redirect to login
    assert response.status_code == 302
    assert '/login/' in response.url

@pytest.mark.django_db
def test_dashboard_authenticated(client, user):
    """Ensure authenticated users can view the dashboard."""
    client.login(username='testuser', password='testpassword123')
    
    # Create some history
    TranslationHistory.objects.create(
        user=user, 
        input_text="hello world", 
        stitched_video_path="/fake/path.mp4"
    )
    
    url = reverse('dashboard')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'history' in response.context
    assert len(response.context['history']) == 1

@pytest.mark.django_db
def test_animation_view_get(client, user):
    """Test loading the animation page."""
    client.login(username='testuser', password='testpassword123')
    url = reverse('animation')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'text' not in response.context
    assert 'words' not in response.context
