import sys
import getopt
import os
from playfair import PlayFair

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "input.txt")

def main(argv):
    input_file = ''
    output_file = ''
    mode = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:m:", ["ifile=", "ofile=", "mode="])
    except getopt.GetoptError:
        print('Error in command line arguments')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('Usage: main.py -i <inputfile> -o <outputfile> -m <mode>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
        elif opt in ("-m", "--mode"):
            mode = arg

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
    cipher = PlayFair("password") 
    if mode == 'encrypt':
        result = cipher.encrypt(text)
        print(cipher.decrypt(result))
    else:
        result = cipher.decrypt(text)

    # Output
    if output_file:
        with open(os.path.join(script_dir, output_file), 'wb' if mode == 'encrypt' else 'w') as file:
            file.write(result)
    else:
        print(result)

if __name__ == "__main__":
   main(sys.argv[1:])
