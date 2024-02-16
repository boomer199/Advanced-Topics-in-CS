import sys
import getopt
import os
from crypto import encrypt, decrypt, gen_password 

def main(argv):
    input_file = ''
    output_file = ''
    mode = ''
    cipher_type = ""
    password_file = ''

    script_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        opts, args = getopt.getopt(argv, "hi:o:m:c:p:", ["ifile=", "ofile=", "mode=", "ctype=", "pfile="])
    except getopt.GetoptError:
        print('Usage: main.py -c <ciphertype> -i <inputfile> -o <outputfile> -m <mode> -p <passwordfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: main.py -c <ciphertype> -i <inputfile> -o <outputfile> -m <mode> -p <passwordfile>")
            print("Supported ciphers: caesar, vigenere, playfair, rsa")
            sys.exit()
        elif opt in ("-c", "--ctype"):
            cipher_type = arg
        elif opt in ("-p", "--pfile"):
            password_file = arg
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-m", "--mode"):
            mode = arg

    if not cipher_type:
        print("Error: Cipher type is required. Use -c to specify the cipher.")
        sys.exit(2)

    if cipher_type not in ["caesar", "vigenere", "playfair", "rsa"]:
        print("Cipher-type not supported, use caesar, vigenere, playfair, or rsa")
        sys.exit(2)

    if mode not in ['encrypt', 'decrypt', 'gen']:
        print('Error: Mode must be "encrypt", "decrypt", or "gen"')
        sys.exit(2)

    # handling password
    if password_file:
        with open(os.path.join(script_dir, password_file), 'r') as pf:
            password = pf.read().strip()
    else:
        password = gen_password()

    # logic for encryption and decryption
    if input_file:
        with open(os.path.join(script_dir, input_file), 'rb') as file:
            text = file.read()
            if mode == decrypt:
                text = bytearray(text, 'utf-8')
    else:
        text = input("Enter text: ")
        if mode == 'decrypt':
            text = bytearray(text, 'utf-8')


    if mode == 'encrypt':
        encrypted_text = encrypt(cipher_type, text, password)
        if output_file:
            with open(os.path.join(script_dir, output_file), 'wb') as file:
                text = bytes(encrypted_text).decode('utf-8')
                file.write(text)
        else:
            print(encrypted_text)
    elif mode == 'decrypt':
        decrypted_text = decrypt(cipher_type, text, password)
        if output_file:
            with open(os.path.join(script_dir, output_file), 'wb') as file:
                file.write(decrypted_text)
        else:
            print(decrypted_text)

if __name__ == "__main__":
   main(sys.argv[1:])
