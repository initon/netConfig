import os
from datetime import datetime


class Backup:

    def __init__(self, path: str, config: str, device_name: str, count_backups: int):
        self.path = path
        self.config = config
        self.device_name = device_name
        self.count_backups = count_backups

    def save_configuration_backup(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M")
        folder = os.path.join(self.path, self.device_name, "backups")
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = os.path.join(folder, f'{self.device_name}_{timestamp}.txt')
        with open(filename, 'w') as f:
            f.write(self.config)

        files = os.listdir(folder)
        files.sort()

        while len(files) > self.count_backups:
            oldest_file = files.pop(0)  # Берем самый старый файл
            os.remove(os.path.join(folder, oldest_file))

    @staticmethod
    def save_configuration_to_tmp_file(path, config):
        with open(path, 'w') as f:
            f.write(config)
