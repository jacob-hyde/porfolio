"""Test authentication functionality."""
import json
import pytest
from app.models.models import User


def test_login(client, db):
    """Test user login functionality."""
    # Create a test user
    user = User(username='testuser')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()

    # Test successful login
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['message'] == 'Login successful'

    # Test invalid credentials
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'wrongpass'
    })
    assert response.status_code == 401

    # Test missing credentials
    response = client.post('/api/login', json={})
    assert response.status_code == 400


def test_check_auth(client, db):
    """Test authentication check functionality."""
    # Create a test user
    user = User(username='testuser')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()

    # Login to get token
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    token = json.loads(response.data)['token']

    # Test with valid token
    response = client.get('/api/check-auth', headers={
        'Authorization': f'Bearer {token}'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['authenticated'] is True
    assert data['user']['username'] == 'testuser'

    # Test with invalid token
    response = client.get('/api/check-auth', headers={
        'Authorization': 'Bearer invalid-token'
    })
    assert response.status_code == 401

    # Test without token
    response = client.get('/api/check-auth')
    assert response.status_code == 401
