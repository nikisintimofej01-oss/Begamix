import pickle
import os

class AuroraDB:
    def __init__(self, filename="aurora_save.dat"):
        self.filename = filename
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'rb') as f:
                    self.data = pickle.load(f)
            except Exception:
                self.data = {}

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def set(self, player_id, key, value):
        if player_id not in self.data:
            self.data[player_id] = {}
        self.data[player_id][key] = value
        # ВАЖНО: Мы убрали self.save() отсюда! 
        # Теперь сохранение на диск происходит только когда мы сами вызовем db.save()

    def get(self, player_id, key, default=None):
        return self.data.get(player_id, {}).get(key, default)

    def get_all(self, player_id):
        return self.data.get(player_id, {})
