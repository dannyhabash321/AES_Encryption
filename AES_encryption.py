# Danny Habash
# CSCE 3550 project 3
# Descriptin: AES encryption. outputs step by step of the process


# input of files, loop controls to make sure 
while True:
    #opening files
    try:
        plainText= input("Enter Plaintext file name: ")
        plainTextFile= open(plainText,'r')
        break
    #catch opening error
    except IOError:
        print("Error! Could not open plain text file! Please try again!")

while True:
    #opening files
    try:
        key = input("Enter key file name: ")
        keyFile= open(key,'r')
        break
    #catch opening error
    except IOError:
        print("Error! Could not open key file! Please try again!")

#opens output file, if it doesnt exist it creates one
output = input("Enter output file name: ")
outputFile= open(output,'w')


#reading files
plainText= plainTextFile.read()
key = keyFile.read()

# a) removing punctuation and white spaces
plainText = plainText.replace(' ', '')
plainText = plainText.replace('\"', '')
plainText = plainText.replace('\'', '')
plainText = plainText.replace('(', '')
plainText = plainText.replace(')', '')
plainText = plainText.replace('.', '')
plainText = plainText.replace(',', '')
plainText = plainText.replace('?', '')
plainText = plainText.replace('!', '')
plainText = plainText.replace(';', '')
plainText = plainText.replace('-', '')
plainText = plainText.replace('\n', '')
print("Preprocessing:",file=outputFile)
print(plainText +"\n" ,file=outputFile)
print("Preprocessing:")
print(plainText +"\n")




# b) viginere cipher
keyStream="" 
#adds key to keystream until length is greater than plaintext
while len(plainText) > len(keyStream):
    keyStream += key
#makes keystream the length of the plaintext by removing last character
while len(plainText) < len(keyStream):
    keyStream = keyStream.rstrip(keyStream[-1])

vigenereCipher="" #stores result of this step
#adds plaintext and key
for c in range(len(plainText)):
    vigenereCipher+=chr((ord(plainText[c])+ ord(keyStream[c]))%26 + 65)

print("Substitution:",file=outputFile)
print("Substitution:")
print(vigenereCipher ,file=outputFile)
print( vigenereCipher)




#padding: checks whether length of cipher is divisible by 16 and add "A" if its not until it is
while not(len(vigenereCipher)/16).is_integer():
    vigenereCipher+="A"

print("\nPadding:",file=outputFile)
print("\nPadding:")

#prints the result in 4x4 blocks
for c in range(len(vigenereCipher)):
    if (c/4).is_integer() and c!=0:
        print()
        print(file=outputFile)
    if (c/16).is_integer() and c!=0:
        print()
        print(file=outputFile)
    print(vigenereCipher[c], end="")
    print(vigenereCipher[c], end="",file=outputFile)



#shiftrows:
print("\n\nShiftRows:", file= outputFile)
print("\n\nShiftRows:")
#this for loop shifts the the values in second, third and 4th row
for c in range(len(vigenereCipher)):
    if c%16 == 4:
        vigenereCipher = vigenereCipher[:c] + vigenereCipher[c+1]+ vigenereCipher[c+2] + vigenereCipher[c+3] + vigenereCipher[c] + vigenereCipher[c+4:]        
    elif c%16 == 8:
        vigenereCipher = vigenereCipher[:c] + vigenereCipher[c+2]+ vigenereCipher[c+3] + vigenereCipher[c] + vigenereCipher[c+1] + vigenereCipher[c+4:]
    elif c%16 == 12:
        vigenereCipher = vigenereCipher[:c] + vigenereCipher[c+3] + vigenereCipher[c] + vigenereCipher[c+1] + vigenereCipher[c+2] + vigenereCipher[c+4:]

#this for loop prints the blocks in blocks shape
for c in range(len(vigenereCipher)):
    if (c/4).is_integer() and c!=0:
        print()
        print(file=outputFile)
    if (c/16).is_integer() and c!=0:
        print()
        print(file=outputFile)
    print(vigenereCipher[c], end="")
    print(vigenereCipher[c], end="",file=outputFile)



#parity bit
#function to convert decimal to binary: code was borrowed from geeksforgeeks
def decimalToBinary(n):
    return "{0:b}".format(int(n))

#function to check if there is odd or even ones in a binary num
def checkOddOnes(num):
    oddOnesCount= 0
    for c in num:
        if c == '1':
            oddOnesCount+=1
    if oddOnesCount%2 == 1:
        return True
    else:
        return False

#converts binary to hexidecimal: code was borrowed from DelftStack
def binToHex(num):
    return "{0:0>2X}".format(int(num, 2))

#stores the result of the parity bit step
parityBit=""
#this for loop converts ascii value of each character into binary, check if odd number of ones and if so then adds 1 to most significant digit
for c in vigenereCipher:
    binC=decimalToBinary(ord(c))
    if checkOddOnes(binC)==True:
        num=decimalToBinary(ord(c)+128)
        parityBit+=binToHex(num)
    else:
        num=decimalToBinary(ord(c))
        parityBit+=binToHex(num)

print("\n\nParity Bit:")
print("\n\nParity Bit:", file=outputFile)
#this for loop prints out the parity bits in a formatted manner
for i in range(0, len(parityBit), 2):
    if (i/8).is_integer() and i!=0:
        print()
        print(file=outputFile)
    if (i/32).is_integer() and i!=0:
        print()
        print(file=outputFile)
    print(parityBit[i]+parityBit[i+1]+" ", end="")
    print(parityBit[i]+parityBit[i+1]+" ", end="",file=outputFile)


#mix columns
#this function preforms multilication of either 2 or 3
def rgfMul(binRep, op):
    xorOp = False # stores if something needs to be xord at the end
    xorBin= [0,0,0,1,1,0,1,1] #binary to be used for xor
    if binRep[0]==1: #if the most significant bit of x is zero the bool val is True for later operatrion
        xorOp=True
    
    #copies binrep to another location for xor in 3 multiplication operation
    op3 = binRep.copy()
    # this for loop translates each bit one spot higher
    for b in range(len(binRep)):
        if b == len(binRep)-1:
            binRep[b]=0
        else:
            binRep[b]=binRep[b+1]
    
    #xors again if op is 3
    if op == 3:
        for b in range(len(binRep)):
            binRep[b] = binRep[b]^op3[b]

    #refers to see if the most significant digit was a 1 if so it xors
    if xorOp:
        for b in range(len(binRep)):
            binRep[b]= binRep[b]^xorBin[b]
    
    return binRep

#returns binary in a vector for ease of math 
def binList(binStr):
    binList=[]
    for c in binStr:
        binList.append(int(c))
    while len(binList)!=8:
        binList.insert(0,0)
    return binList;        



#stores mix columns
mixCol =""
#preforms conversions from hex to binary and then preforms the neccessry multiplications on each 4x4 block
for hx in range(0,len(parityBit),2):
    hexRep = parityBit[hx]+parityBit[hx+1]
    binRep = decimalToBinary(int(hexRep,16))
    binList0 = binList(binRep)
    #checks if its the first row of the 4x4 blocks and preforms operations if so
    if hx%32 < 8:
        #column1 binary list
        hexRep = parityBit[hx+8]+parityBit[hx+9]
        binRep = decimalToBinary(int(hexRep,16))
        binList2 = binList(binRep)
        
        #column2 binary list
        hexRep = parityBit[hx+16]+parityBit[hx+17]
        binRep = decimalToBinary(int(hexRep,16))
        binList3 = binList(binRep)

        #column3 binary list
        hexRep = parityBit[hx+24]+parityBit[hx+25]
        binRep = decimalToBinary(int(hexRep,16))
        binList4 = binList(binRep)

        l1 = rgfMul(binList0, 2)
        l2 = rgfMul(binList2, 3)
        
        #preforms xor operation for the first row
        binResultList = "" # stores result of xoring first row
        for c in range(8):
            binResultList += str(l1[c]^l2[c]^binList3[c]^binList4[c])

        binListToHexVar=""#holds the hex rep of that result list
        #converts binary result list to hexadecimal value then adds it to result string
        for e in binResultList:
            binListToHexVar += e
        mixCol+=binToHex(binListToHexVar)
    
    #checks if its the second row of the 4x4 blocks and preforms operations if so
    if hx%32 >7 and hx%32 < 16:
        #column1 binary list
        hexRep = parityBit[hx-8]+parityBit[hx-7]
        binRep = decimalToBinary(int(hexRep,16))
        binList2 = binList(binRep)
        
        #column2 binary list
        hexRep = parityBit[hx+8]+parityBit[hx+9]
        binRep = decimalToBinary(int(hexRep,16))
        binList3 = binList(binRep)

        #column3 binary list
        hexRep = parityBit[hx+16]+parityBit[hx+17]
        binRep = decimalToBinary(int(hexRep,16))
        binList4 = binList(binRep)

        l1 = rgfMul(binList0, 2)
        l2 = rgfMul(binList3, 3)
        
        #preforms xor operation for the first row
        binResultList = "" # stores result of xoring first row
        for c in range(8):
            binResultList += str(l1[c]^l2[c]^binList2[c]^binList4[c])

        binListToHexVar=""#holds the hex rep of that result list
        #converts binary result list to hexadecimal value then adds it to result string
        for e in binResultList:
            binListToHexVar += e
        mixCol+=binToHex(binListToHexVar)
    
    #checks if its the third row of the 4x4 blocks and preforms operations if so
    if hx%32 >15 and hx%32 < 24:
        #column1 binary list
        hexRep = parityBit[hx-16]+parityBit[hx-15]
        binRep = decimalToBinary(int(hexRep,16))
        binList2 = binList(binRep)
        
        #column2 binary list
        hexRep = parityBit[hx-8]+parityBit[hx-7]
        binRep = decimalToBinary(int(hexRep,16))
        binList3 = binList(binRep)

        #column3 binary list
        hexRep = parityBit[hx+8]+parityBit[hx+9]
        binRep = decimalToBinary(int(hexRep,16))
        binList4 = binList(binRep)

        l1 = rgfMul(binList0, 2)
        l2 = rgfMul(binList4, 3)
        
        #preforms xor operation for the first row
        binResultList = "" # stores result of xoring first row
        for c in range(8):
            binResultList += str(l1[c]^l2[c]^binList2[c]^binList3[c])

        binListToHexVar=""#holds the hex rep of that result list
        #converts binary result list to hexadecimal value then adds it to result string
        for e in binResultList:
            binListToHexVar += e
        mixCol+=binToHex(binListToHexVar)
    
    #checks if its the fourth row of the 4x4 blocks and preforms operations if so
    if hx%32 >23 and hx%32 < 32:
        #column1 binary list
        hexRep = parityBit[hx-24]+parityBit[hx-23]
        binRep = decimalToBinary(int(hexRep,16))
        binList2 = binList(binRep)
        
        #column2 binary list
        hexRep = parityBit[hx-16]+parityBit[hx-15]
        binRep = decimalToBinary(int(hexRep,16))
        binList3 = binList(binRep)

        #column3 binary list
        hexRep = parityBit[hx-8]+parityBit[hx-7]
        binRep = decimalToBinary(int(hexRep,16))
        binList4 = binList(binRep)

        l1 = rgfMul(binList0, 2)
        l2 = rgfMul(binList2, 3)
        
        #preforms xor operation for the first row
        binResultList = "" # stores result of xoring first row
        for c in range(8):
            binResultList += str(l1[c]^l2[c]^binList3[c]^binList4[c])

        binListToHexVar=""#holds the hex rep of that result list
        #converts binary result list to hexadecimal value then adds it to result string
        for e in binResultList:
            binListToHexVar += e
        mixCol+=binToHex(binListToHexVar)


    # elif c%32 < 16:
    # elif c%32 <24:


print("\n\nMixcolumns:")
print("\n\nMixcolumns:", file=outputFile)
#prints the mix columns in formatted way
for i in range(0, len(mixCol), 2):
    if (i/8).is_integer() and i!=0:
        print()
        print(file=outputFile)
    if (i/32).is_integer() and i!=0:
        print()
        print(file=outputFile)
    print(mixCol[i]+mixCol[i+1]+" ", end="")
    print(mixCol[i]+mixCol[i+1]+" ", end="",file=outputFile) 
print("\n")
print("\n",file=outputFile)
