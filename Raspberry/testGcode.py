import serial
import os
import time

PORT = "/dev/ttyACM0"
def connectResetHome():
    SERIAL_CONNECTION = serial.Serial(PORT, 115200)
    # Hit enter a few times to wake up
    SERIAL_CONNECTION.write(str.encode("\r\n\r\n"))
    time.sleep(2)  # Wait for initialization
    SERIAL_CONNECTION.flushInput()  # Flush startup text in serial input
    SERIAL_CONNECTION.write(str.encode('G10 P0 L20 X0 Y0 Z0') + str.encode('\n'))
    grbl_out = SERIAL_CONNECTION.readline()
    print("resetting" + grbl_out.strip().decode("utf-8"))
    SERIAL_CONNECTION.close()
    
    
def penUp():
    SERIAL_CONNECTION = serial.Serial(PORT, 115200)
    # Hit enter a few times to wake up
    SERIAL_CONNECTION.write(str.encode("\r\n\r\n"))
    time.sleep(2)  # Wait for initialization
    SERIAL_CONNECTION.flushInput()  # Flush startup text in serial input
    SERIAL_CONNECTION.write(str.encode('G21G91Z5F1000') + str.encode('\n'))
    grbl_out = SERIAL_CONNECTION.readline()
    SERIAL_CONNECTION.close()

def printMat(mat):
    penUp()
    connectResetHome()
    for i in range (0,9):
        if i%2 == 0:
            for j in range (0,9):
                print(str(mat[i][j]))
                if mat[i][j] != 0 and mat[i][j] != '0':
                    printBlock(mat[i][j])
                if(j < 8):
                    os.system('python3.8 gcode_sender.py -p '+PORT+' -f "/home/pi/Desktop/GP/Gcode/x+.ngc" -v 0 -r 1')
                    time.sleep(2)
                elif(j == 8 and i != 8):
                        os.system('python3.8 gcode_sender.py -p '+PORT+' -f "/home/pi/Desktop/GP/Gcode/y-.ngc" -v 0 -r 1')
                        time.sleep(2)
        else:
            for j in range (8,-1,-1):
                print(str(mat[i][j]))
                if mat[i][j] != 0 and mat[i][j] != '0':
                    printBlock(mat[i][j])
                if(j > 0):
                    os.system('python3.8 gcode_sender.py -p '+PORT+' -f "/home/pi/Desktop/GP/Gcode/x-.ngc" -v 0 -r 1')
                    time.sleep(2)
                elif(j == 0):
                    os.system('python3.8 gcode_sender.py -p '+PORT+' -f "/home/pi/Desktop/GP/Gcode/y-.ngc" -v 0 -r 1')
                    time.sleep(2)

def printBlock(num):
    print(num)
    connectResetHome()
    os.system('python3.8 gcode_sender.py -p '+PORT+' -f "/home/pi/Desktop/GP/Gcode/'+str(num)+'.ngc" -v 0 -r 1')
    time.sleep(2)


def cncPrint(solution):
    print(solution)
    matrix = solution
    printMat(matrix)
