import sys
import getopt
from playfair import PlayFair

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
        with open(input_file, 'r') as file:
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
        with open(output_file, 'wb' if mode == 'encrypt' else 'w') as file:
            file.write(result)
    else:
        print(result)

if __name__ == "__main__":
   main(sys.argv[1:])
