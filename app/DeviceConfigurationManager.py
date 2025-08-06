import os


class DeviceConfigurationManager:

    def __init__(self, device):
        self.device = device
        self.config_current = None
        self.DEVICE_COMMANDS = {
            "cisco_ios_telnet": ["terminal length 0", "show run"],
            "cisco_ios": ["terminal length 0", "show run"],
            "mikrotik_routeros": ["/export"],
            "generic": ["terminal length 0", "sh run"]
        }
        self.DEVICE_MUTABLE_CONFIGURATION_LINES = {
            "cisco_ios_telnet": [r"ntp clock-period"],
            "mikrotik_routeros": [r"by RouterOS"]
        }

    def delete_lines(self, patterns):
        lines = self.config_current.splitlines()
        filtered_lines = ""
        for pattern in patterns:
            filtered_lines = [line for line in lines if pattern not in line]
        self.config_current = '\n'.join(filtered_lines)

    def get_device_configuration(self):
        device_type = self.device.device_type
        if device_type == "cisco_ios_telnet":
            self.config_current = self.device.send_commands(self.DEVICE_COMMANDS[device_type])
        elif device_type == "cisco_ios":
            self.config_current = self.device.send_commands(self.DEVICE_COMMANDS[device_type])
        elif device_type == "mikrotik_routeros":
            self.config_current = self.device.send_commands(self.DEVICE_COMMANDS[device_type])
        elif device_type == "generic":
            self.config_current = self.device.send_commands_generic_ssh(self.DEVICE_COMMANDS[device_type])

        if device_type in self.DEVICE_MUTABLE_CONFIGURATION_LINES:
            self.delete_lines(
                self.DEVICE_MUTABLE_CONFIGURATION_LINES[device_type]
            )
        return self.config_current

    @staticmethod
    def get_configuration_latest(path_tmp_config_file):
        if os.path.exists(path_tmp_config_file):
            with open(path_tmp_config_file, 'r', encoding='utf-8') as file:
                file_content = file.read()
                return str(file_content)
        else:
            return ""
