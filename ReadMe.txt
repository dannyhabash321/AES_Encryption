Danny Habash
CSCE 3550 project 3
Descriptin: AES encryption. outputs step by step of the process. 

******ONLY WORKS WITH UPPERCASE LETTERS******

To compile: note: *written in python 3
    python3 AES_encryption.py

The input files are for example

Algorithm:
    1. removes punctuation, spaces, new lines
    2. creates key stream equal to plaintext length from inputted key file and adds ascii value to plaintext
    3. creates blocks of 4x4 and pads the last block with 'A's until it is a 4x4 block
    4. Shifts rows of the 4x4 blocks by different measures
    5. Checks if there is an even or odd number of 1s in the binary rep of char: if odd msb is turned into 1
    6. Multiplies the parity bits according to given instructions in mix columns
    
    
    
