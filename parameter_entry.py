class ParameterConverter:
    @staticmethod
    def int_to_hex_string(value, bits=16):
        try:
            # Convert the input value to an integer
            numeric_value = int(value)

            # If the value is negative, compute its 2's complement
            if numeric_value < 0:
                numeric_value = ~abs(numeric_value) + 1

            # Mask the result to fit within the specified number of bits
            numeric_value &= (1 << bits) - 1

            # Format to 4 hexadecimal digits with leading zeros
            hex_value = format(numeric_value, '04X')

            # Insert space between every 2 digits
            formatted_hex = ' '.join(hex_value[i:i+2] for i in range(0, len(hex_value), 2))

            return formatted_hex
        except ValueError:
            # Return None or raise an error if the input is not a valid integer
            return None
            
    @staticmethod
    def convert_and_negate(parameter):
        try:
            # Convert the string to an integer
            numeric_value = int(parameter)

            # Negate the value (make it negative)
            return -abs(numeric_value)
        except ValueError:
            # Handle the error if the input is not a valid number
            print("Invalid input: not a number")
            return None
