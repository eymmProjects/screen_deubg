import serial

class ModbusSerialSender:
    def __init__(self, port='COM3', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None

    def configure_port(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        if self.serial_connection is not None:
            self.close_connection()
            self.serial_connection = None

    def open_connection(self):
        self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        if not self.serial_connection.is_open:
            self.serial_connection.open()
            print("Serial port opened.")
        else:
            print("Serial port already open.")

    def close_connection(self):
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Serial port closed.")

    def send_data(self, data):
        if self.serial_connection is None or not self.serial_connection.is_open:
            print("Serial port is not open. Cannot send data.")
            return

        crc = self.crc16_modbus(data)
        data_with_crc = data + crc

        try:
            self.serial_connection.write(data_with_crc)
            print("Data with CRC sent successfully.")
        except Exception as e:
            print(f"Error sending data with CRC: {e}")

    @staticmethod
    def crc16_modbus(data):
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for i in range(8):
                if (crc & 1) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc.to_bytes(2, byteorder='little')
