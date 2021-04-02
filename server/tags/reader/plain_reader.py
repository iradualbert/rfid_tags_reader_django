import serial

cmd = "t" + '\r\n'

def scan_tags():
    ser = serial.Serial("COM5", 115200)
    while True:
        ser.write(cmd.encode())
        line = ser.readline()
        # line = line.strip().decode("utf-8")
        print(line)


if __name__ == "__main__":
    scan_tags()