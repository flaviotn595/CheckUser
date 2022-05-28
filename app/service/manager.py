import os
import sys


class ServiceManager:
    CONFIG_SYSTEMD_PATH = '/etc/systemd/system/'
    CONFIG_SYSTEMD = 'user_check.service'

    @property
    def config(self) -> str:
        return os.path.join(self.CONFIG_SYSTEMD_PATH, self.CONFIG_SYSTEMD)

    @property
    def is_created(self) -> bool:
        return os.path.exists(self.config)

    @property
    def is_enabled(self) -> bool:
        return os.system('systemctl is-enabled %s >/dev/null' % self.CONFIG_SYSTEMD) == 0

    def status(self) -> str:
        command = 'systemctl status %s' % self.CONFIG_SYSTEMD
        result = os.popen(command).readlines()
        return ''.join(result)

    def start(self):
        status = self.status()
        if 'Active: active' not in status:
            os.system('systemctl start %s' % self.CONFIG_SYSTEMD)
            return True

        return False

    def stop(self):
        status = self.status()
        if 'Active: inactive' not in status:
            os.system('systemctl stop %s' % self.CONFIG_SYSTEMD)
            return True

        return False

    def restart(self) -> bool:
        command = 'systemctl restart %s' % self.CONFIG_SYSTEMD
        return os.system(command) == 0

    def remove_service(self):
        os.system('systemctl stop %s' % self.CONFIG_SYSTEMD)
        os.system('systemctl disable %s' % self.CONFIG_SYSTEMD)
        os.system('rm %s' % self.config)
        os.system('systemctl daemon-reload')

    def create_systemd_config(self):
        config_template = ''.join(
            [
                '[Unit]\n',
                'Description=User check service\n',
                'After=network.target\n\n',
                '[Service]\n',
                'Type=simple\n',
                'ExecStart=%s %s --run\n' % (sys.executable, os.path.abspath(__file__)),
                'Restart=always\n',
                'User=root\n',
                'Group=root\n\n',
                '[Install]\n',
                'WantedBy=multi-user.target\n',
            ]
        )

        config_path = os.path.join(self.CONFIG_SYSTEMD_PATH, self.CONFIG_SYSTEMD)
        if not os.path.exists(config_path):
            try:
                with open(config_path, 'w') as f:
                    f.write(config_template)
            except PermissionError:
                return

            os.system('systemctl daemon-reload >/dev/null')

    def enable_auto_start(self) -> bool:
        if not self.is_enabled:
            os.system('systemctl enable %s >/dev/null' % self.CONFIG_SYSTEMD)

        return self.is_enabled

    def disable_auto_start(self) -> bool:
        if self.is_enabled:
            os.system('systemctl disable %s >/dev/null' % self.CONFIG_SYSTEMD)

        return not self.is_enabled

    def create_service(self) -> bool:
        self.create_systemd_config()
        return self.is_created
