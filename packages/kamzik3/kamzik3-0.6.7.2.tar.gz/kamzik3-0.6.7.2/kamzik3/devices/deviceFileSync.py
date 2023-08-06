import os
import time

from kamzik3 import DeviceError
from kamzik3.constants import *
from kamzik3.devices.device import Device


class DeviceFileSync(Device):

    def __init__(self, filepath, device_id=None, config=None):
        self.filepath = filepath
        super(DeviceFileSync, self).__init__(device_id, config)
        self.connect()

    def _init_attributes(self):
        super(DeviceFileSync, self)._init_attributes()
        self.create_attribute(ATTR_FILEPATH, set_function=self.set_filepath, readonly=True)
        self.create_attribute(ATTR_CONTENT, set_function=self.set_content)

    def handle_configuration(self):

        start_at = time.time()

        self._config_commands()
        self._config_attributes()
        self.set_value(ATTR_FILEPATH, self.filepath)
        self.set_status(STATUS_CONFIGURED)
        self.logger.info(u"Device configuration took {} sec.".format(time.time() - start_at))

    def command(self, command, callback=None, with_token=False, returning=True):
        raise DeviceError("Device does not accept any commands.")

    def set_filepath(self, value):
        if not os.path.exists(value):
            raise DeviceError("File {} does not exists".format(value))
        else:
            with open(value, "r") as fp:
                file_content = "".join(fp.readlines())
                self.set_raw_value(ATTR_CONTENT, file_content)

    def set_content(self, value):
        with open(self.get_value(ATTR_FILEPATH), "w") as fp:
            fp.write(value)
