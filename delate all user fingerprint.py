import serial

# Initialize serial connection
def connect_sensor(port='COM3', baudrate=38400, timeout=2):
    return serial.Serial(port, baudrate, timeout=timeout)

# Calculate checksum (XOR from the second byte to the Len+1 byte)
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

# Delete all users from the fingerprint sensor
def delete_all_users(ser):
    # Command structure to delete all users
    command = bytes([0xF5, 0x05, 0x00, 0x00, 0x00, 0x00])
    checksum = calculate_checksum(command[1:7])  # Calculate checksum from CMD to the 6th byte
    command += bytes([checksum, 0xF5])
    
    # Send the command to the sensor
    ser.write(command)
    
    # Read the response from the sensor
    response = ser.read(8)
    
    if len(response) < 8:
        print(f"Response too short: {response}")
        return False
    
    if response[4] == 0x00:  # Check for ACK_SUCCESS
        print("All users deleted successfully.")
        return True
    else:
        print(f"Failed to delete users, response: {response}")
        return False

# Example usage
def main():
    ser = connect_sensor()
    
    # Delete all users
    if delete_all_users(ser):
        print("Ready to register new users.")
    else:
        print("Failed to delete users, please check the sensor.")
    
    ser.close()

if __name__ == "__main__":
    main()
