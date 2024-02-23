import sys
import getopt
import os
from crypto import encrypt, decrypt, gen_password, ciphers, gen

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

    password = gen_password() if not password_file else open(os.path.join(script_dir, password_file), 'r').read().strip()

    text = None
    if input_file:
        with open(os.path.join(script_dir, input_file), 'rb') as file:
            text = file.read()
            #text = bytearray(text, 'utf-8') if mode == 'decrypt' else input_text
    else:
        input_text = input("Enter text: ")
        text = bytearray(input_text, 'utf-8') if mode == 'decrypt' else input_text


    if mode == 'encrypt' or mode == 'decrypt':
        if mode == 'encrypt':
            result = encrypt(cipher_type, text, password)
        elif mode == 'decrypt':
            result = decrypt(cipher_type, text, password)

        # Writing the result for encryption or decryption
        if output_file:
            mode_flag = 'wb' if mode == 'encrypt' else 'w'
            with open(os.path.join(script_dir, output_file), mode_flag) as file:
                file.write(result)
        else:
            # Ensure proper decoding for display based on the operation
            print(result.decode('utf-8') if mode == 'encrypt' else result)
    elif mode == 'gen':
        # Key generation should not attempt to use 'result' for file operations
        if cipher_type == 'rsa':
            keys = gen(cipher_type)
            public_key, private_key = keys["public"], keys["private"]
            if output_file:
                with open(f"{output_file}.public", 'w') as pub_file:
                    pub_file.write(str(public_key))
                with open(f"{output_file}.private", 'w') as priv_file:
                    priv_file.write(str(private_key))
            else:
                print(f"Public Key: {public_key}")
                print(f"Private Key: {private_key}")
        else:
            password = gen(cipher_type)  # Generate a password for non-RSA ciphers
            if output_file:
                with open(output_file, 'w') as file:
                    file.write(password)
            else:
                print(f"Generated Password: {password}")


if __name__ == "__main__":
   main(sys.argv[1:])
