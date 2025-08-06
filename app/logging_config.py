import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,  # Уровень логирования
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("./logs/netConfig.log", encoding="utf-8"),  # Логирование в файл
            logging.StreamHandler()  # Логирование в консоль
        ]
    )
