import serial
from generate import generatePuzzle
from getGrid import takeImageExtractGrid
from DigitDetect import *
from Suduko import solverController
from testGcode import cncPrint


ESP_port = "/dev/ttyACM1"


SERIAL_CONNECTION = serial.Serial(ESP_port, 9600)

count = 0
camGrid = ""
puzzleGrid = ""
userGrid = ""
model = initializePredictionModel()

def convertToMatrix(test_str, K):
    # slicing strings
    temp = [test_str[idx: idx + K] for idx in range(0, len(test_str), K)]
 
    # conversion to list of characters
    res = [list(ele) for ele in temp]
 
    # printing result
    return res

def readvalues():
    global count
    global userGrid
    flag = False
    while True:
        for c in SERIAL_CONNECTION.read().decode('utf-8'):
            if c.isnumeric():
                userGrid.append(c)
                count = count + 1
                print("count: ",count)
            if count == 81:
                flag = True
                break
        if flag:
            break
    count = 0

while True:
    if SERIAL_CONNECTION.in_waiting > 0:
        data = SERIAL_CONNECTION.read().decode('utf-8').rstrip()
        print(data)
        # take image
        if data == "0":
            camGrid = takeImageExtractGrid(model)
            SERIAL_CONNECTION.write(b"1")
        # send grid
        elif data == "1":
            SERIAL_CONNECTION.write(camGrid.encode('utf-8'))
        # puzzle
        elif data == "2":
            SERIAL_CONNECTION.write(b"1")
            while SERIAL_CONNECTION.in_waiting <= 0:
                x=1
            level = SERIAL_CONNECTION.read().decode('utf-8')
            puzzle = generatePuzzle(level)
            print(type(puzzle))
            puzzle = convertToMatrix(puzzle, 9)
            cncPrint(puzzle)
            SERIAL_CONNECTION.write(b"1")
        #get user grid
        elif data == "3":
            SERIAL_CONNECTION.write(b"1")
            userGrid = []
            while SERIAL_CONNECTION.in_waiting <= 0:
                x=1
            readvalues()
            userGrid = ''.join(userGrid)
            solution = solverController(userGrid)
            #print(solution)
            cncPrint(solution)
            SERIAL_CONNECTION.write(b"1")
