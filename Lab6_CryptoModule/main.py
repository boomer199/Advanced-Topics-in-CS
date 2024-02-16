import sys
import getopt
import os
from crypto import __init__ as i


def main(argv):
    input_file = ''
    output_file = ''
    mode = ''
    cipher_type = ""
    password_file = ''

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "input.txt")

    try:
        opts, args = getopt.getopt(argv, "hi:o:m:c:p:", ["ifile=", "ofile=", "mode=", "ctype=", "pfile="])
    except getopt.GetoptError:
        print('Usage: main.py -c <ciphertype> -i <inputfile> -o <outputfile> -m <mode> [-p <passwordfile>]')
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

    # Process for RSA cipher
    if cipher_type == "rsa" and mode == "gen":
        public_key, private_key = 0 # DO RSA LOGIC LMAO
        if not output_file:
            print("Public Key:", public_key)
            print("Private Key:", private_key)
        else:
            with open(output_file + ".public", 'w') as pub_file:
                pub_file.write(public_key)
            with open(output_file + ".private", 'w') as priv_file:
                priv_file.write(private_key)
        sys.exit(0)

    # If cipher is not RSA and mode is gen, generate a random password
    if cipher_type != "rsa" and mode == "gen":
        if not output_file:
            print(i.generate_random_password())
        else:
            with open(output_file, 'w') as file:
                file.write(i.generate_random_password())
        sys.exit(0)

    # Read input
    if input_file:
        with open(os.path.join(script_dir, input_file)) as file:
            text = file.read()
    else:
        text = input("Enter text: ")


if __name__ == "__main__":
   main(sys.argv[1:])
