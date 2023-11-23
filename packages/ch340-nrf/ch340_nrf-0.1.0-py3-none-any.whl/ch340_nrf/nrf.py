"""
Main nrf class for controlling nrf modules with CH340 serial adapters
"""

import time
import enum
from typing import Iterable
import serial
from . import translator


class BAUDRATE(enum.Enum):
    """A class for NRF baudrates"""

    BAUDRATE_4800 = 4800
    BAUDRATE_9600 = 9600
    BAUDRATE_14400 = 14400
    BAUDRATE_19200 = 19200
    BAUDRATE_38400 = 38400
    BAUDRATE_115200 = 115200


class RATE(enum.Enum):
    """A class for NRF transmission rates"""

    @staticmethod
    def parse_string(rate: str) -> "RATE":
        """Parses a string to a RATE enum"""

        rate = rate.lower()

        if rate == "2mbps":
            return RATE.RATE_2M
        if rate == "1mbps":
            return RATE.RATE_1M
        if rate == "250kbps":
            return RATE.RATE_250K

        raise ValueError("Invalid String")

    RATE_250K = 1
    RATE_1M = 2
    RATE_2M = 3


class Address:
    """Address class for controlling nrf modules with CH340 serial adapters"""

    def __init__(self, address: Iterable[int] = (0x00, 0x00, 0x00, 0x00, 0x00)) -> None:
        if len(address) != 5:
            raise ValueError("Invalid address")

        self.address = list(address)

    def __repr__(self) -> str:
        return f"Address({self.address})"

    def __str__(self) -> str:
        return ":".join([f"{byte:02X}" for byte in self.address])

    def __eq__(self, other: "Address") -> bool:
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __len__(self) -> int:
        return len(self.address)

    def __getitem__(self, key: int) -> int:
        return self.address[key]

    def __setitem__(self, key: int, value: int) -> None:
        self.address[key] = value


class Config:
    """Config class for controlling nrf modules with CH340 serial adapters"""

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        baudrate: BAUDRATE = BAUDRATE.BAUDRATE_9600,
        rate: RATE = RATE.RATE_1M,
        local_address: Address = Address((0x00, 0x00, 0x00, 0x00, 0x00)),
        target_address: Address = Address((0x00, 0x00, 0x00, 0x00, 0x00)),
        freq: int = 400,
        checksum: int = 16,
    ) -> None:
        self.baudrate = baudrate
        self.rate = rate
        self.local_address = local_address
        self.target_address = target_address
        self.freq = freq
        self.checksum = checksum

    def __repr__(self) -> str:
        return (
            f"Config("
            f"baudrate={self.baudrate}, "
            f"rate={self.rate}, "
            f"local_address={self.local_address}, "
            f"target_address={self.target_address}, "
            f"freq={self.freq}, "
            f"checksum={self.checksum}"
            f")"
        )

    def __str__(self) -> str:
        return (
            f"baudrate={self.baudrate}, "
            f"rate={self.rate}, "
            f"local_address={self.local_address}, "
            f"target_address={self.target_address}, "
            f"freq={self.freq}, "
            f"checksum={self.checksum}"
        )

    def __eq__(self, other: "Config") -> bool:
        return self.__dict__ == other.__dict__


class NRF:
    """
    NRF class for controlling nrf modules with CH340 serial adapters
    """

    def __init__(
        self, port: str, config: Config = Config(), translate: bool = True
    ) -> None:
        self.serial_port = serial.Serial(port=port, baudrate=config.baudrate.value)

        self.translate = translate
        self.set_config(config)

    def send_message(self, message: str) -> None:
        """Sends a message to the nrf module"""

        self.serial_port.write((message + "\r\n").encode())

    def read_message(self, system=False) -> str | None:
        """Reads a message from the nrf module"""

        if self.serial_port.in_waiting > 0:
            message = self.serial_port.readline()

            if system:
                message = message.decode("gb18030")
            else:
                message = message.decode("utf-8")

            if self.translate:
                message = translator.translate(message)

            return message
        return None

    def read_all_messages(self, system=False) -> list[str]:
        """Reads all messages from the nrf module"""

        messages = []

        while self.serial_port.in_waiting > 0:
            messages.append(self.read_message(system=system))

        return messages

    def set_baudrate(self, baudrate: BAUDRATE) -> list[str]:
        """Sets the baudrate of the serial port"""

        if baudrate not in BAUDRATE:
            raise ValueError("Invalid baudrate")

        self.send_message("AT+BAUD=" + str(baudrate.value))
        self.serial_port.baudrate = baudrate.value

        time.sleep(0.2)
        return self.read_all_messages(system=True)

    def set_rate(self, rate: RATE) -> list[str]:
        """Sets the transmission rate of the nrf module"""

        if rate not in RATE:
            raise ValueError("Invalid rate")

        self.send_message("AT+RATE=" + str(rate.value))

        time.sleep(0.2)
        return self.read_all_messages(system=True)

    def set_local_address(self, local_address: Address | tuple[int]) -> list[str]:
        """Sets the local address of the nrf module"""

        if isinstance(local_address, tuple):
            local_address = Address(local_address)

        self.send_message(
            "AT+RXA=" + ",".join([f"0x{byte:02X}" for byte in local_address])
        )

        time.sleep(0.2)
        return self.read_all_messages(system=True)

    def set_target_address(self, target_address: Address | tuple[int]) -> list[str]:
        """Sets the target address of the nrf module"""

        if isinstance(target_address, tuple):
            target_address = Address(target_address)

        self.send_message(
            "AT+TXA=" + ",".join([f"0x{byte:02X}" for byte in target_address])
        )

        time.sleep(0.2)
        return self.read_all_messages(system=True)

    def set_freq(self, freq: int) -> list[str]:
        """Sets the frequency of the nrf module"""

        if freq < 400 or freq > 525:
            raise ValueError("Invalid frequency")

        self.send_message("AT+FREQ=" + str(freq))

        time.sleep(0.2)
        return self.read_all_messages(system=True)

    def set_checksum(self, checksum: int) -> None:
        """Sets the checksum of the nrf module"""

        if checksum < 8 or checksum > 16:
            raise ValueError("Invalid checksum")

        self.send_message("AT+CRC=" + str(checksum))

        time.sleep(0.2)
        self.read_all_messages(system=True)

    def get_system_info(self) -> dict[str, str]:
        """Gets the system information of the nrf module"""

        def get_value(line: str) -> str:
            return line.split("：")[1].strip()

        self.send_message("AT?")
        time.sleep(0.5)

        data = self.read_all_messages(system=True)
        info = {}

        for line, text in enumerate(data):
            if line in [0, 1]:
                continue

            if line == 2:
                info["baudrate"] = BAUDRATE(int(get_value(text)))

            elif line == 3:
                info["target_address"] = Address(
                    [int(byte, 16) for byte in get_value(text).split(",")]
                )

            elif line == 4:
                info["local_address"] = Address(
                    [int(byte, 16) for byte in get_value(text).split(",")]
                )

            elif line == 5:
                info["freq"] = int(get_value(text).replace("GHz", "").replace("2.", ""))

            elif line == 6:
                info["checksum"] = int(get_value(text).replace("Bit CRC Check", ""))

            elif line == 7:
                info["power"] = int(get_value(text).replace("dBm", ""))

            elif line == 8:
                info["rate"] = RATE.parse_string(get_value(text))

            elif line == 9:
                info["gain"] = get_value(text)

        return info

    def set_config(self, config: Config) -> None:
        """Sets the configuration of the nrf module"""

        system_info = self.get_system_info()

        if config.baudrate != system_info["baudrate"]:
            self.set_baudrate(config.baudrate)

        if config.rate != system_info["rate"]:
            self.set_rate(config.rate)

        if config.local_address != system_info["local_address"]:
            self.set_local_address(config.local_address)

        if config.target_address != system_info["target_address"]:
            self.set_target_address(config.target_address)

        if config.freq != system_info["freq"]:
            self.set_freq(config.freq)

        if config.checksum != system_info["checksum"]:
            self.set_checksum(config.checksum)

        self._config = config

    @property
    def config(self):
        """Returns the configuration of the nrf module"""

        return self._config

    @config.setter
    def config(self, config: Config) -> None:
        """Sets the configuration of the nrf module"""

        self.set_config(config)
