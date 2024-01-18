def hex_to_b10(hex_string):
    if not hex_string:
        return None

    hex_chars = "0123456789ABCDEF"
    hex_string = hex_string.upper()
    b10 = 0

    hex_to_dec = {char: i for i, char in enumerate(hex_chars)}

    for char in hex_string.strip("0X"):
        if char not in hex_to_dec:
            return None
        b10 = b10 * 16 + hex_to_dec[char]

    return b10

String = "0x122"
print(hex_to_b10(String))