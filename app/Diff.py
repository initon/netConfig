import difflib


class Diff:

    def __init__(self, config_latest, config_current):
        self.config_latest = config_latest
        self.config_current = config_current

    def compare_strings(self):
        lines1 = self.config_latest.splitlines()
        lines2 = self.config_current.splitlines()

        diff = difflib.ndiff(lines1, lines2)
        changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]
        return '\n'.join(changes)

    def get_diff_configs(self):
        if self.config_current != self.config_latest:
            diff_config = self.compare_strings()
            if self.config_latest != "":
                return diff_config
