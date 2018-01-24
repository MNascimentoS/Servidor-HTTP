import serial

class Conexao(object):

    def __init__(self):
        self.opcao = "1"
        self.arduino = serial.Serial("COM3", 9600)

    def temperature(self):
        self.arduino.write(self.opcao.encode())

    def sendMessage(self, frase):
        self.arduino.write(frase.encode())

    def close(self):
        self.arduino.close()

    def getTemperature(self):
        temp = str(self.arduino.read(6))
        print("Temperatura: " + temp)
        return temp[2] + temp[3] + temp[4] + temp[5] + temp[6]
