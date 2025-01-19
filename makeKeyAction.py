""" Совершаем ключевое действие, если вердикт верный с компонентом Arduino """

from compareResultPointsFace import get_compare_points
from initPointsFace import FacePoints
import time
try:
    import serial.tools.list_ports
    import serial
except ImportError:
    import pip
    pip.main(['install', 'pyserial'])


class ActionArduino:
    """ Настроенное действие или действия с компонентами Arduino """

    def checkDifferentPointValue(self) -> bool:

        facePointsStatic = FacePoints(modeReadFacePoint='static')
        facePointsStaticArray = facePointsStatic.getFacePoints()[0]

        facePointsLive = FacePoints(modeReadFacePoint='live')
        facePointsLiveArray = facePointsLive.getFacePoints()[0]

        # итоговый вердикт по совпадению двух изображений
        DifferentPointValue = get_compare_points(facePointsStaticArray, facePointsLiveArray)

        return DifferentPointValue


if __name__ == '__main__':

    checkPortArduino = FacePoints(modeReadFacePoint="checkPort")
    availablePort = checkPortArduino.checkArduinoPortESP()

    def sendMessageArduino(command: str):
        """ Отправляем сообщение на плату Arduino по порту 9600 """

        port = "/dev/ttyUSB1"
        baudrate = 9600
        ser = serial.Serial(port, baudrate)
        time.sleep(2)

        try:
            while True:
                ser.write(command.encode('utf-8'))  # Отправка команды в Arduino
                break
        except KeyboardInterrupt:
            pass
        finally:
            ser.close()  # Закрытие порта при завершении работы

    if availablePort:
        actionArduino = ActionArduino()
        responseCheckFace = actionArduino.checkDifferentPointValue()

        if responseCheckFace: # Лица успешно совпали
            sendMessageArduino(command="SUCCESS")
        else:
            sendMessageArduino(command="FAILED")

    else:
        assert ValueError

