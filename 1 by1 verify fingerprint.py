import serial
import time

# Initialize serial connection
def connect_sensor(port='COM3', baudrate=38400, timeout=2):
    return serial.Serial(port, baudrate, timeout=timeout)

# Calculate checksum (XOR from the second byte to the Len+1 byte)
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

# Verify a fingerprint with a 1:1 comparison
def verify_fingerprint(ser, user_id):
    # Create the command bytes
    command = bytes([
        0xF5,                # Start Byte
        0x0B,                # Command Code for 1:1 fingerprint comparison
        (user_id >> 8) & 0xFF,  # User ID High 8-bit
        user_id & 0xFF,        # User ID Low 8-bit
        0x00,                # Reserved
        0x00,                # Reserved
        0x00,                # Placeholder for checksum
        0xF5                 # End Byte
    ])
    
    # Calculate checksum excluding the checksum byte itself
    checksum = calculate_checksum(command[1:7])
    command = command[:6] + bytes([checksum]) + command[7:]
    
    # Send command to sensor
    ser.write(command)
    
    # Read the response
    response = ser.read(8)
    
    # Validate response length
    if len(response) < 8:
        print(f"Response too short: {response}")
        return False
    
    # Validate response checksum
    expected_checksum = response[6]
    actual_checksum = calculate_checksum(response[1:6])
    if expected_checksum != actual_checksum:
        print(f"Checksum mismatch: expected {expected_checksum}, got {actual_checksum}")
        return False
    
    # Check response status
    status_code = response[4]
    if status_code == 0x00:  # ACK_SUCCESS
        print("Fingerprint verified successfully.")
        return True
    elif status_code == 0x01:  # ACK_FAIL
        print("Fingerprint verification failed.")
        return False
    elif status_code == 0x02:  # ACK_TIMEOUT
        print("Fingerprint verification timed out.")
        return False
    else:
        print(f"Unknown response status: {response}")
        return False

# Example usage
def main():
    ser = connect_sensor()  # Connect to the sensor
    user_id = 1  # Example user ID for verification
    if verify_fingerprint(ser, user_id):
        print("Fingerprint verification successful.")
    else:
        print("Fingerprint verification failed.")
    ser.close()  # Close the serial connection

if __name__ == "__main__":
    main()
