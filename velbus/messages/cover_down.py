"""
:author: Tom Dupré <gitd8400@gmail.com>
"""
import json
import logging
import struct
import velbus

COMMAND_CODE = 0x06


class CoverDownMessage(velbus.Message):
    """
    sent by:
    received by: VMB2BLE
    """

    def __init__(self, address=None):
        velbus.Message.__init__(self)
        self.channel = 0
        self.delay_time = 0
        self.set_defaults(address)

    def populate(self, priority, address, rtr, data):
        """
        :return: None
        """
        assert isinstance(data, bytes)
        self.needs_high_priority(priority)
        self.needs_no_rtr(rtr)
        self.needs_data(data, 4)
        self.set_attributes(priority, address, rtr)
        self.channel = self.byte_to_channel(data[0])
        self.needs_valid_channel(self.channel, 2)
        (self.delay_time,) = struct.unpack('>L', bytes([0]) + data[1:])

    def to_json(self):
        """
        :return: str
        """
        json_dict = self.to_json_basic()
        json_dict['channel'] = self.channel
        json_dict['delay_time'] = self.delay_time
        return json.dumps(json_dict)

    def set_defaults(self, address):
        if address is not None:
            self.set_address(address)
        self.set_high_priority()
        self.set_no_rtr()

    def data_to_binary(self):
        """
        :return: bytes
        """
        return bytes([
            COMMAND_CODE,
            self.channels_to_byte([self.channel])
        ]) + struct.pack('>L', self.delay_time)[-3:]


class CoverDownMessage2(velbus.Message):
    """
    sent by:
    received by: VMB1BL VMB2BL
    """

    def __init__(self, address=None):
        velbus.Message.__init__(self)
        self.channel = 0
        self.delay_time = 0
        self.logger = logging.getLogger('velbus')
        self.set_defaults(address)

    def populate(self, priority, address, rtr, data):
        """
        :return: None
        """
        assert isinstance(data, bytes)
        self.needs_high_priority(priority)
        self.needs_no_rtr(rtr)
        self.needs_data(data, 4)
        self.set_attributes(priority, address, rtr)
        # 00000011 = channel 1
        # 00001100 = channel 2
        # so shift 1 bit to the right + and with 03
        tmp = (data[0] >> 1) & 0x03
        print(tmp)
        self.channel = self.byte_to_channel(tmp)
        self.needs_valid_channel(self.channel, 2)
        (self.delay_time,) = struct.unpack('>L', bytes([0]) + data[1:])

    def to_json(self):
        """
        :return: str
        """
        json_dict = self.to_json_basic()
        json_dict['channel'] = self.channel
        json_dict['delay_time'] = self.delay_time
        return json.dumps(json_dict)

    def set_defaults(self, address):
        if address is not None:
            self.set_address(address)
        self.set_high_priority()
        self.set_no_rtr()

    def data_to_binary(self):
        """
        :return: bytes
        """
        return bytes([
            COMMAND_CODE,
            self.channels_to_byte([self.channel])
        ]) + struct.pack('>L', self.delay_time)[-3:]

velbus.register_command(COMMAND_CODE, CoverDownMessage, 'VMB1BLE')
velbus.register_command(COMMAND_CODE, CoverDownMessage, 'VMB2BLE')
velbus.register_command(COMMAND_CODE, CoverDownMessage2, 'VMB1BL')
velbus.register_command(COMMAND_CODE, CoverDownMessage2, 'VMB2BL')
