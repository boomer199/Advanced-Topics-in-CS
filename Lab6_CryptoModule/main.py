import sys
import getopt
import os
from crypto import __init__

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "input.txt")

def main(argv):
    input_file = ''
    output_file = ''
    mode = ''
    cipher_type = ""
    try:
        opts, args = getopt.getopt(argv, "hi:o:m:", ["ifile=", "ofile=", "mode=", "ctype="])
    except getopt.GetoptError:
        print('Error in command line arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: main.py -c <ciphertype> -i <inputfile> -o <outputfile> -m <mode>')
            sys.exit()
        elif opt in ("-c", "--ctype"):
            cipher_type = arg
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-m", "--mode"):
            mode = arg

    if cipher_type not in ["caesar", "vigenere", "playfair", "rsa"]:
        print("Cipher-type not supported, use caesar, vigenere, playfair, or rsa")
        sys.exit(2)

    if mode not in ['encrypt', 'decrypt']:
        print('Error: Mode must be "encrypt" or "decrypt"')
        sys.exit(2)

    # Read input
    if input_file:
        with open(os.path.join(script_dir, input_file)) as file:
            text = file.read()
    else:
        text = input("Enter text: ")

    # Process
    cipher = 0#TODO:

if __name__ == "__main__":
   main(sys.argv[1:])
