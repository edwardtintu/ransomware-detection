from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

# Function to encrypt the file
def encrypt_file(file_path, key):
    # Open the file to read its data
    with open(file_path, 'rb') as f:
        data = f.read()
    
    # Generate a random IV (Initialization Vector)
    iv = os.urandom(16)  # 16 bytes IV for AES-128/192/256
    
    # Create a Cipher object with AES algorithm and CFB mode using the generated IV
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    
    # Write the IV and encrypted data back to the file
    with open(file_path, 'wb') as f:
        f.write(iv)  # Write IV first
        f.write(encrypted_data)  # Then write encrypted data
    
    print(f"File successfully encrypted: {file_path}")

# Function to get the key from the user
def get_key_from_user(key_size):
    while True:
        key = input(f"Enter a {key_size}-byte key for encryption (exact length): ")
        key = key.encode('utf-8')  # Convert input to bytes
        
        # Check if the key length matches the selected size
        if len(key) == key_size:
            return key
        else:
            print(f"Invalid key length. The key must be exactly {key_size} bytes long.")

# Main function to handle file encryption based on user input
def main():
    print("Welcome to the File Encryption Script!")
    
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
    file_path = input("Enter the full file path to encrypt (e.g., C:\\Users\\EDWARD\\Downloads\\yourfile.pdf): ").strip()

    # Encrypt the file
    encrypt_file(file_path, key)

    print("Encryption completed successfully.")

  
# Run the main function
if __name__ == '__main__':
    main()
