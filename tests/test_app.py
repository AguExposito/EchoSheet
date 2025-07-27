import pytest
import json
import tempfile
import os
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    # Create a temporary database for testing
    db_fd, db_path = tempfile.mkstemp()
    
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path
    
    with app.test_client() as client:
        yield client
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

def test_index_page(client):
    """Test that the index page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'characters' in response.data

def test_create_page(client):
    """Test that the create character page loads successfully"""
    response = client.get('/create')
    assert response.status_code == 200
    assert b'Create Character' in response.data

def test_api_spells_endpoint(client):
    """Test the spells API endpoint"""
    response = client.get('/api/spells/wizard')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'spells' in data

def test_api_playstyles_endpoint(client):
    """Test the playstyles API endpoint"""
    response = client.get('/api/playstyles/wizard')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'playstyles' in data

def test_character_creation(client):
    """Test character creation via API"""
    character_data = {
        'name': 'Test Character',
        'race': 'Human',
        'char_class': 'Wizard',
        'background': 'Sage',
        'level': 1
    }
    
    response = client.post('/create', 
                          data=json.dumps(character_data),
                          content_type='application/json')
    
    # Should redirect to character page or return success
    assert response.status_code in [200, 302]

def test_spell_validation(client):
    """Test spell validation endpoint"""
    spell_data = {
        'char_class': 'Wizard',
        'cantrips': ['Fire Bolt'],
        'spells': ['Magic Missile', 'Burning Hands']
    }
    
    response = client.post('/api/spells/validate',
                          data=json.dumps(spell_data),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data
    assert data['success'] == True
    assert 'validation' in data

if __name__ == '__main__':
    pytest.main([__file__]) 