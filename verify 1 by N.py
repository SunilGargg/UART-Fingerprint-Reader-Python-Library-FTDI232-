import serial

# Initialize serial connection
def connect_sensor(port='COM3', baudrate=38400, timeout=2):
    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Connected to sensor on {port}")
        return ser
    except serial.SerialException as e:
        print(f"Failed to connect to sensor: {e}")
        return None

# Calculate checksum (XOR from the second byte to the Len+1 byte)
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

# Perform 1:N fingerprint verification
def verify_fingerprint_1N(ser):
    # Command to perform 1:N fingerprint verification
    command = bytes([0xF5, 0x0C, 0x00, 0x00, 0x00, 0x00])
    checksum = calculate_checksum(command[1:7])
    command += bytes([checksum, 0xF5])
    
    # Send command to sensor
    ser.write(command)
    print("Verification command sent, awaiting response...")
    
    # Read the response (8 bytes)
    response = ser.read(8)
    if len(response) < 8:
        print(f"Response too short: {response}")
        return None
    
    print(f"Response received: {response}")
    
    if response[1] != 0x0C:
        print(f"Unexpected command response: {response[1]}")
        return None
    
    # Check if the verification was successful
    if response[4] == 0x00:  # Assuming 0x00 is ACK_NOUSER
        print("No matching user found (ACK_NOUSER).")
        return None
    elif response[4] == 0x01:  # Assuming 0x01 is ACK_TIMEOUT
        print("Verification timed out (ACK_TIMEOUT).")
        return None
    
    # Extract User ID and privilege
    user_id = (response[2] << 8) | response[3]
    user_privilege = response[4]
    
    print(f"User ID: {user_id}, User Privilege: {user_privilege}")
    return user_id, user_privilege

# Example usage
def main():
    ser = connect_sensor()  # Connect to the sensor
    if ser is None:
        print("Exiting due to connection failure.")
        return
    
    result = verify_fingerprint_1N(ser)
    if result:
        user_id, user_privilege = result
        print(f"Fingerprint verified. User ID: {user_id}, Privilege: {user_privilege}")
    else:
        print("Fingerprint verification failed or no user found.")
    
    ser.close()  # Close the serial connection

if __name__ == "__main__":
    main()
