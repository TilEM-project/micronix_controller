import logging

import serial
import serial.tools.list_ports

from .commands import Commands
from .errors import ErrorMessages

logging.basicConfig(level=logging.INFO)


class MicronixSerialConnection:
    def __init__(
        self,
        port,
        baudrate=38400,
        bytesize=serial.EIGHTBITS,
        timeout=0.020,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
    ):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout = timeout
        self.parity = parity
        self.stopbits = stopbits
        self.connection = None

    def __enter__(self):
        try:
            self.connection = serial.Serial(
                self.port,
                self.baudrate,
                bytesize=self.bytesize,
                timeout=self.timeout,
                parity=self.parity,
                stopbits=self.stopbits,
            )
            logging.info(f"Connected to {self.port}")
            return self
        except serial.SerialException as e:
            logging.error(f"Failed to connect: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_open:
            self.connection.close()
            logging.info("Disconnected Serial Connection")

    def send_command(self, axis, command, *parameters):
        if not self.connection or not self.connection.is_open:
            raise RuntimeError("Serial connection is not open")

        if not isinstance(command, Commands):
            raise ValueError("Invalid command")

        param_str = ",".join(map(str, parameters))
        full_command = f"{axis}{command.command}{param_str}\r"
        logging.info(f"Sending command: {full_command.strip()} - {command.details}")
        self.connection.write(full_command.encode())

    def read_response(self):
        response = self.connection.readline().decode().strip()
        logging.info(f"Received response: {response}")
        return response

    def send_and_receive(self, axis, command, *parameters):
        self.send_command(axis, command, *parameters)
        return self.read_response()

    def check_for_errors(self, response):
        try:
            error_code = int(response.split()[0])
            if error_code in ErrorMessages._value2member_map_:
                error_message = ErrorMessages(error_code)
                logging.error(error_message.message)
                raise Exception(error_message.message)
        except ValueError:
            logging.info("No error code in response")

    def execute_command(self, axis, command, *parameters):
        response = self.send_and_receive(axis, command, *parameters)
        self.check_for_errors(response)
        return response
    
    def poll_values(self, axis, command):
        if not self.connection or not self.connection.is_open:
            raise RuntimeError("Serial connection is not open")

        if not isinstance(command, Commands):
            raise ValueError("Invalid command")

        send_command = f"{axis}{command.command}?\r"
        self.connection.write(send_command.encode())

        response = ""
        while True:
            check_response = self.connection.read(1).decode("utf-8")
            if check_response == "":
                break
            else:
                response += check_response

        response = response.replace("#", "").strip()
        if response != "":
            return response
        logging.info("No Response or Invalid")
        return False


if __name__ == "__main__":
    port = "/dev/ttyUSB0"  # Example port
    with MicronixSerialConnection(port) as conn:
        pass
        # conn.execute_command("1", Commands.MOT, 1)
        # conn.execute_command("1", Commands.MVA, 1000)

        