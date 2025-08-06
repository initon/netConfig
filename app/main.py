import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor

from app.Backup import Backup
from app.Device import Device
from app.DeviceConfigurationManager import DeviceConfigurationManager
from app.Diff import Diff
from app.MatrixBot import MatrixBot
from app.Settings import Settings
from app.logging_config import setup_logging
from dotenv import load_dotenv

load_dotenv(dotenv_path="./configs/.env")

MATRIX_SERVER = os.getenv("MATRIX_SERVER")
USERNAME = os.getenv("USERNAME_MATRIX")
PASSWORD = os.getenv("PASSWORD")
ROOM = os.getenv("ROOM")
TIMEOUT = float(os.getenv("TIMEOUT"))

bot = MatrixBot(MATRIX_SERVER, USERNAME, PASSWORD, ROOM)

setup_logging()
logger = logging.getLogger(__name__)
logging.getLogger('nio').setLevel(logging.CRITICAL)
logging.getLogger('paramiko.transport').setLevel(logging.CRITICAL)

messages = []


def process_device(device_settings):
    device = Device(**device_settings)
    manager = DeviceConfigurationManager(device)
    folder = os.path.join('./backups', device.name)
    path_tmp_file = os.path.join(folder, 'latest.txt')

    current_configuration = manager.get_device_configuration()
    if current_configuration is None:
        logger.error(f"Не удалось загрузить конфигурацию устройства {device.name}")
        return
    latest_configuration = read_latest_configuration(path_tmp_file, current_configuration)

    if current_configuration != latest_configuration:
        handle_configuration_change(device.name, latest_configuration, current_configuration)
        backup = Backup('./backups', current_configuration, device.name, count_backups=30)
        backup.save_configuration_backup()
        backup.save_configuration_to_tmp_file(path_tmp_file, current_configuration)


def read_latest_configuration(path_tmp_file, current_configuration):
    if os.path.exists(path_tmp_file):
        return DeviceConfigurationManager.get_configuration_latest(path_tmp_file)
    else:
        directory_tmp_file = os.path.dirname(path_tmp_file)
        if not os.path.exists(directory_tmp_file):
            os.makedirs(directory_tmp_file)
        with open(path_tmp_file, 'w') as f:
            f.write(current_configuration)
        return current_configuration


def handle_configuration_change(device_name, latest_configuration, current_configuration):
    diff = Diff(latest_configuration, current_configuration)
    changes = diff.get_diff_configs()
    print(changes)
    logging.info(f"Обнаружены изменения на устройстве: {device_name}")
    messages.append(MatrixBot.get_formatted_message_diff(f"Обнаружены изменения на устройстве: <u><b>"
                                                         f"{device_name}</u></b>\n", changes))


def send_messages_to_matrix_room():
    if len(messages) > 0:
        bot.send_message_with_code(messages)


def main():
    settings = Settings("configs/devices.json")
    settings.load_config()

    while True:
        messages.clear()
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(process_device, settings.config_devices["devices"])

        send_messages_to_matrix_room()
        print(f"Ждем {TIMEOUT} с.")
        time.sleep(TIMEOUT)


if __name__ == "__main__":
    main()
