from pyinfra.api import FactBase


class ServiceRunning(FactBase):
    def command(self, service_name):
        return "systemctl show -p SubState --value " + service_name

    def process(self, output):
        return output[0] == "running"
