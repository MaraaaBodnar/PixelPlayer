<<<<<<< HEAD
from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

# Ноти для різних рядків (частоти в Гц)
NOTES = {
    0: {"note": "C4", "freq": 261.63, "color": "#ff6b6b"},  # Червоний
    1: {"note": "D4", "freq": 293.66, "color": "#ff8c6b"},  # Помаранчевий
    2: {"note": "E4", "freq": 329.63, "color": "#ffad6b"},  # Жовтогарячий
    3: {"note": "F4", "freq": 349.23, "color": "#ffce6b"},  # Жовтий
    4: {"note": "G4", "freq": 392.00, "color": "#e6ff6b"},  # Салатовий
    5: {"note": "A4", "freq": 440.00, "color": "#6bff6b"},  # Зелений
    6: {"note": "B4", "freq": 493.88, "color": "#6bffce"},  # Бірюзовий
    7: {"note": "C5", "freq": 523.25, "color": "#6bcaff"}  # Блакитний
}


class PixelMusicBox:
    def __init__(self, width=16, height=8):
        self.width = width
        self.height = height
        self.pixels = [[0] * width for _ in range(height)]
        self.current_position = 0
        self.is_playing = False
        self.bpm = 120

    def toggle_pixel(self, row, col):
        """Перемикає стан пікселя"""
        if 0 <= row < self.height and 0 <= col < self.width:
            self.pixels[row][col] = 1 - self.pixels[row][col]
            return True
        return False

    def clear(self):
        """Очищає всі пікселі"""
        self.pixels = [[0] * self.width for _ in range(self.height)]

    def get_pattern(self):
        """Повертає поточний патерн"""
        return self.pixels

    def get_notes_at_column(self, col):
        """Повертає ноти для заданої колонки"""
        notes = []
        for row in range(self.height):
            if self.pixels[row][col] == 1:
                notes.append(NOTES[row])
        return notes

    def get_sequence(self):
        """Повертає всю послідовність нот"""
        sequence = []
        for col in range(self.width):
            sequence.append(self.get_notes_at_column(col))
        return sequence


music_box = PixelMusicBox()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state', methods=['GET'])
def get_state():
    """Повертає поточний стан музичної шкатулки"""
    return jsonify({
        'pixels': music_box.get_pattern(),
        'width': music_box.width,
        'height': music_box.height,
        'bpm': music_box.bpm,
        'notes': NOTES
    })


@app.route('/api/toggle', methods=['POST'])
def toggle_pixel():
    """Перемикає піксель за координатами"""
    data = request.json
    row = data.get('row')
    col = data.get('col')
    success = music_box.toggle_pixel(row, col)
    return jsonify({'success': success, 'pixels': music_box.get_pattern()})


@app.route('/api/clear', methods=['POST'])
def clear_pixels():
    """Очищає всі пікселі"""
    music_box.clear()
    return jsonify({'success': True, 'pixels': music_box.get_pattern()})


@app.route('/api/set_bpm', methods=['POST'])
def set_bpm():
    """Встановлює BPM"""
    data = request.json
    bpm = data.get('bpm', 120)
    music_box.bpm = max(40, min(240, bpm))
    return jsonify({'success': True, 'bpm': music_box.bpm})


@app.route('/api/sequence', methods=['GET'])
def get_sequence():
    """Повертає послідовність нот для програвання"""
    return jsonify({'sequence': music_box.get_sequence()})


if __name__ == '__main__':
    # Створюємо папку templates якщо її немає
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
=======
#
>>>>>>> a35cacb (This is my first commit)
