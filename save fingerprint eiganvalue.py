import serial
import time

# Initialize serial connection
def connect_sensor(port='COM3', baudrate=38400, timeout=5):
    return serial.Serial(port, baudrate, timeout=timeout)

# Calculate checksum (XOR from the second byte to the Len+1 byte)
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum ^= byte
    return checksum

# Download fingerprint template
def download_fingerprint_template(ser, user_id):
    # Command to download fingerprint template
    command = bytes([0xF5, 0x31, (user_id >> 8) & 0xFF, user_id & 0xFF, 0x00, 0x00])
    checksum = calculate_checksum(command[1:7])
    command += bytes([checksum, 0xF5])
    
    print(f"Sending command: {command.hex()}")  # Debugging: print command sent
    ser.write(command)
    
    # Wait for a response
    time.sleep(1)  # Give some time for the sensor to respond
    
    # Read the response (8 bytes header)
    response = ser.read(8)
    if len(response) < 8:
        print(f"Response too short: {response.hex()}")
        return None
    
    print(f"Received response: {response.hex()}")  # Debugging: print response received
    
    # Check if the response indicates success
    if response[4] != 0x00:  # Assuming 0x00 is ACK_SUCCESS
        print(f"Failed to download template, response: {response.hex()}")
        return None
    
    # Get the length of the data to be read
    length = (response[2] << 8) | response[3]
    print(f"Data length: {length}")  # Debugging: print data length
    
    # Read the actual fingerprint data
    data = ser.read(length)
    if len(data) != length:
        print(f"Data length mismatch: expected {length}, got {len(data)}")
        return None
    
    print(f"Received fingerprint data (length {length}): {data.hex()}")  # Debugging: print data received
    return data

# Save fingerprint data to a file
def save_fingerprint_to_file(data, file_path):
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        print(f"Fingerprint data saved to {file_path}")
    except Exception as e:
        print(f"Failed to save fingerprint data: {e}")

def main():
    ser = connect_sensor()  # Connect to the sensor
    user_id = 1  # Example user ID
    fingerprint_data = download_fingerprint_template(ser, user_id)
    if fingerprint_data:
        # Save the fingerprint data to a file
        save_fingerprint_to_file(fingerprint_data, 'fingerprint_template.bin')
    else:
        print("Failed to download fingerprint template.")
    ser.close()  # Close the serial connection

if __name__ == "__main__":
    main()
