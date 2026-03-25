import pytest
from main import app, music_box, NOTES

@pytest.fixture
def client():
    """Фікстура для Flask test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Перевірка головної сторінки"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Піксельна Музична Шкатулка' in response.data

def test_get_state(client):
    """Перевірка /api/state"""
    response = client.get('/api/state')
    assert response.status_code == 200
    data = response.get_json()
    assert 'pixels' in data
    assert 'width' in data
    assert 'height' in data
    assert 'notes' in data
    assert data['width'] == music_box.width
    assert data['height'] == music_box.height

def test_toggle_pixel(client):
    """Перевірка /api/toggle"""
    row, col = 0, 0
    # Спочатку піксель вимкнений
    assert music_box.pixels[row][col] == 0

    response = client.post('/api/toggle', json={'row': row, 'col': col})
    data = response.get_json()
    assert data['success'] is True
    assert music_box.pixels[row][col] == 1

    # Перемикаємо знову
    response = client.post('/api/toggle', json={'row': row, 'col': col})
    data = response.get_json()
    assert data['success'] is True
    assert music_box.pixels[row][col] == 0

def test_clear_pixels(client):
    """Перевірка /api/clear"""
    # Вмикаємо кілька пікселів
    music_box.toggle_pixel(0,0)
    music_box.toggle_pixel(1,1)
    response = client.post('/api/clear')
    data = response.get_json()
    assert data['success'] is True
    # Всі пікселі вимкнені
    assert all(all(col == 0 for col in row) for row in music_box.pixels)

def test_set_bpm(client):
    """Перевірка /api/set_bpm"""
    response = client.post('/api/set_bpm', json={'bpm': 200})
    data = response.get_json()
    assert data['success'] is True
    assert music_box.bpm == 200

    # Тестування меж BPM
    response = client.post('/api/set_bpm', json={'bpm': 500})
    data = response.get_json()
    assert music_box.bpm == 240  # обмеження max

    response = client.post('/api/set_bpm', json={'bpm': 10})
    data = response.get_json()
    assert music_box.bpm == 40  # обмеження min

def test_get_sequence(client):
    """Перевірка /api/sequence"""
    music_box.clear()
    # Вмикаємо один піксель
    music_box.toggle_pixel(0, 0)
    response = client.get('/api/sequence')
    data = response.get_json()
    sequence = data['sequence']
    assert len(sequence) == music_box.width
    # Перша колонка має піксель
    assert len(sequence[0]) == 1
    assert sequence[0][0]['note'] == NOTES[0]['note']
    # Інші колонки порожні
    for col in sequence[1:]:
        assert col == []