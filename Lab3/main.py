def main():
    number = 729
    print(f'Binary form of {number} is {bin(number)}')

    print('\tBinary -> Grey')
    grey = binary_to_grey(number)
    print(f'Number {bin(number)} converted to Grey code: {bin(grey)}')

    print('\tGrey -> Binary')
    binary = grey_to_binary(grey)
    print(f'Number in gray code {bin(number)} converted to binary: {bin(binary)}')


def binary_to_grey(number):
    """Convert binary to Grey code"""
    if isinstance(number, str):
        number = int(number, 2)

    return number ^ (number >> 1)


def grey_to_binary(number):
    """Convert Grey code to binary"""
    if isinstance(number, str):
        number = int(number, 2)

    mask = number >> 1
    while mask:
        number ^= mask
        mask >>= 1
    return number


if __name__ == '__main__':
    main()
