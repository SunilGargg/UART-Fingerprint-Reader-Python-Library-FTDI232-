import serial
import time
import os

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

# Download fingerprint image
def download_fingerprint_image(ser, user_id, output_folder):
    # Command structure for downloading fingerprint image
    command = bytes([0xF5, 0x31, (user_id >> 8) & 0xFF, user_id & 0xFF, 0x00, 0x00])
    checksum = calculate_checksum(command[1:7])
    command += bytes([checksum, 0xF5])
    
    # Send command to sensor
    ser.write(command)
    print("Command sent, awaiting response...")
    
    # Read the response header (8 bytes)
    response = ser.read(8)
    if len(response) < 8:
        print(f"Response too short: {response}")
        return None
    
    print(f"Response received: {response}")
    
    if response[4] != 0x00:  # Assuming 0x00 is ACK_SUCCESS
        print(f"Failed to download image, response: {response}")
        return None
    
    # Read the length of the image data
    length = (response[2] << 8) | response[3]
    print(f"Expected image data length: {length} bytes")
    
    # Read the image data
    data = ser.read(length)
    
    if len(data) != length:
        print(f"Data read length mismatch: expected {length}, got {len(data)}")
        return None
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the image data to a file
    file_path = os.path.join(output_folder, 'fingerprint_image.bin')
    with open(file_path, 'wb') as file:
        file.write(data)
    
    print(f"Fingerprint image saved to {file_path}")
    return file_path

# Example usage
def main():
    ser = connect_sensor()  # Connect to the sensor
    if ser is None:
        print("Exiting due to connection failure.")
        return
    
    user_id = 1  # Example user ID
    output_folder = 'fingerprint_images'  # Folder to save the image
    
    file_path = download_fingerprint_image(ser, user_id, output_folder)
    if file_path:
        print(f"Image successfully downloaded and saved to {file_path}.")
    else:
        print("Failed to download or save the fingerprint image.")
    
    ser.close()  # Close the serial connection

if __name__ == "__main__":
    main()
