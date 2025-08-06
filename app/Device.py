import logging
from logging_config import setup_logging

from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

setup_logging()
logger = logging.getLogger(__name__)


class Device:

    def __init__(self, name, device_type, host, username, password, secret, port=22):
        self.device_type = device_type
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.secret = secret
        self.port = port
        self.device_options = self.get_device_options()

    def get_device_options(self):
        return {
            "device_type": self.device_type,
            "host": self.host,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            "port": self.port
        }

    def send_commands(self, commands):
        try:
            with ConnectHandler(**self.device_options) as ssh:
                ssh.enable()
                host = self.device_options["host"]
                logger.info(f"Подкючение к устройству: {host}")
                for command in commands:
                    output = ssh.send_command(command)
                    result = output
            return result
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
            logging.error(f"Ошибка при отправке команд на устрйство: {error}")

    def send_commands_generic_ssh(self, commands):
        try:
            result = ""
            connection = ConnectHandler(**self.device_options)
            if self.device_options['secret']:
                connection.enable()
            for command in commands:
                result = connection.send_command(command)
            connection.disconnect()

            return result
        except Exception as e:
            print(f"An error occurred: {e}")

