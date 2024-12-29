from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Function to decrypt the file
def decrypt_file(file_path, key):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    
    # Open the encrypted file to read its data
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    
    # Ensure that there is at least 16 bytes of IV
    if len(encrypted_data) < 16:
        print("Error: The file is too small to be a valid encrypted file.")
        return

    # Extract the IV (first 16 bytes)
    iv = encrypted_data[:16]
    
    # Create a Cipher object to decrypt with the same AES key and CFB mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
    
    # Write the decrypted data back to the file
    with open(file_path, 'wb') as f:
        f.write(data)
    
    print(f"File successfully decrypted: {file_path}")

# Function to get the key from the user
def get_key_from_user(key_size):
    while True:
        key = input(f"Enter a {key_size}-byte key for decryption (exact length): ")
        key = key.encode('utf-8')  # Convert input to bytes
        
        # Check if the key length matches the selected size
        if len(key) == key_size:
            return key
        else:
            print(f"Invalid key length. The key must be exactly {key_size} bytes long.")

# Main function to handle file decryption based on user input
def main():
    print("Welcome to the File Decryption Script!")
    
    # Ask the user to choose key size
    while True:
        try:
            key_size = int(input("Enter key size (16 for AES-128, 24 for AES-192, 32 for AES-256): "))
            if key_size in [16, 24, 32]:
                break  # Break if valid key size is entered
            else:
                print("Please choose 16, 24, or 32 bytes for the key size.")
        except ValueError:
            print("Invalid input. Please enter a valid number (16, 24, or 32).")
    
    # Get the key from the user
    key = get_key_from_user(key_size)
    
    # Ask the user to input the full file path
    file_path = input("Enter the full file path to decrypt (e.g., C:\\Users\\EDWARD\\Downloads\\yourfile.pdf): ").strip()

    # Decrypt the file
    decrypt_file(file_path, key)

    print("Decryption completed successfully.")

# Run the main function
if __name__ == '__main__':
    main()
