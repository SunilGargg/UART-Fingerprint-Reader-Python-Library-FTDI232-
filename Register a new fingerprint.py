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

# Register a new fingerprint
def register_finger(ser, user_id):
    # Step through the registration process
    for step in [0x01, 0x02, 0x03]:  # Steps may vary depending on the sensor's protocol
        # Create the command bytes
        command = bytes([0xF5, step, (user_id >> 8) & 0xFF, user_id & 0xFF, 0x01, 0x00])
        checksum = calculate_checksum(command[1:7])  # XOR from CMD to the 6th byte
        command += bytes([checksum, 0xF5])
        
        # Send command to sensor
        ser.write(command)
        
        # Read the response
        response = ser.read(8)
        
        # Validate response
        if len(response) < 8:
            print(f"Response too short: {response}")
            return False
        
        # Check if the response indicates success
        if response[4] != 0x00:  # Assuming 0x00 is ACK_SUCCESS
            print(f"Registration step {step} failed, response: {response}")
            return False
        
        # Wait for a short period before sending the next command
        time.sleep(1)
    
    print("Fingerprint registration successful.")
    return True

# Example usage
def main():
    ser = connect_sensor()  # Connect to the sensor
    user_id = 1  # Example user ID
    if register_finger(ser, user_id):
        print("Fingerprint registered successfully.")
    else:
        print("Failed to register fingerprint.")
    ser.close()  # Close the serial connection

if __name__ == "__main__":
    main()
