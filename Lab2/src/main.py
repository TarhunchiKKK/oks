from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


bitsNumberComboBoxItems: list[str] = ['8 bit', '7 bit', '6 bit', '5 bit']


class BitStaffingMethods:

    @staticmethod
    def getData(data: str) -> str:
        return data + (1 - len(data)) * "x"

    @staticmethod
    def getFlag(data: str) -> str:
        length: int = len(data)
        binaryNumber: str = ""
        while length > 0:
            binaryNumber = str(length % 2) + binaryNumber
            length //= 2
        return "0" * (8 - len(binaryNumber)) + binaryNumber


    @staticmethod
    def getSourceAddress(portName: str) -> str:
        number: int = 0
        for i in range(len(portName)):
            if portName[i].isdigit():
                number = int(portName[3::1])
                break

        binaryNumber: str = ""
        while number > 0:
            binaryNumber = str(number % 2) + binaryNumber
            number //= 2
        length: int = len(binaryNumber)
        return "0" * (4 - length) + binaryNumber


    @staticmethod
    def bitStaffing(data: str) -> str:
        counter: int = 0
        staffed: str = ""
        for i in range(len(data)):
            staffed += data[i]
            if data[i] == "0":
                counter += 1
                if counter == 7:
                    staffed += "0"
                    counter = 0
            elif data[i] == "1":
                counter = 0
        return staffed


    @staticmethod
    def debitStaffing(data: str) -> str:
        data = data[8::1]
        counter: int = 0
        destuffed: str = ""
        for i in data:
            if i == "0":
                counter += 1
                if counter != 8:
                    destuffed += i
                else:
                    counter = 0
            elif i == "1" or i == "x":
                destuffed += i
                counter = 0
        return destuffed

    @staticmethod
    def getHighlightedBits(data: str) -> str:
        counter: int = 0
        highlightedData: str = ""
        for i in range(len(data)):
            if data[i] == "0":
                counter += 1
            elif data[i] == "1":
                counter = 0

            if counter == 8:
                highlightedData += "["
                highlightedData += data[i]
                highlightedData += "]"
                counter = 0
            else:
                highlightedData += data[i]
        return highlightedData

    @staticmethod
    def divide_str(data: str, n: int = 1) -> list[str]:
        if len(data) == 0:
            return list("x")
        else:
            return list(data)
    @staticmethod
    def split_on_packages(data: str) -> list[str]:
        splited: list[str] = []
        length: int = len(data)
        step: int = 0
        if length % 18 == 0:
            step = 18
        elif length % 19 == 0:
            step = 19
        start: int = 0
        while start < length:
            splited.append(data[start:start + step:1])
            start += step
        return splited

    @staticmethod
    def list_to_str(lst: list[str]) -> str:
        data: str = ""
        for i in lst:
            data += i
        return data



class Ui_PortApp(object):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.port: QSerialPort = QSerialPort()
        self.port.readyRead.connect(self.onRecieveBytes)

    def setupUi(self, PortApp):
        PortApp.setObjectName("PortApp")
        PortApp.resize(700, 500)
        PortApp.setMinimumSize(QtCore.QSize(700, 500))
        PortApp.setMaximumSize(QtCore.QSize(700, 500))
        PortApp.setStyleSheet("")

        self.centralwidget = QtWidgets.QWidget(PortApp)
        self.centralwidget.setObjectName("centralwidget")

        self.inputTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.inputTextEdit.setGeometry(QtCore.QRect(20, 40, 300, 131))
        self.inputTextEdit.setObjectName("inputTextEdit")
        self.inputTextEdit.keyPressEvent = self.onInputTextChanged

        self.outputTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.outputTextEdit.setEnabled(True)
        self.outputTextEdit.setGeometry(QtCore.QRect(370, 40, 300, 131))
        self.outputTextEdit.setReadOnly(True)
        self.outputTextEdit.setObjectName("outputTextEdit")

        self.inputLabel = QtWidgets.QLabel(self.centralwidget)
        self.inputLabel.setGeometry(QtCore.QRect(20, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.inputLabel.setFont(font)
        self.inputLabel.setStyleSheet("font-size: 20px;\n"
"font-weight: bold;")
        self.inputLabel.setObjectName("inputLabel")

        self.outputLabel = QtWidgets.QLabel(self.centralwidget)
        self.outputLabel.setGeometry(QtCore.QRect(370, 10, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.outputLabel.setFont(font)
        self.outputLabel.setStyleSheet("font-size: 20px;\n"
"font-weight: bold;")
        self.outputLabel.setObjectName("outputLabel")

        self.controlLabel = QtWidgets.QLabel(self.centralwidget)
        self.controlLabel.setGeometry(QtCore.QRect(20, 210, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.controlLabel.setFont(font)
        self.controlLabel.setStyleSheet("font-size: 20px;\n"
"font-weight: bold;")
        self.controlLabel.setObjectName("controlLabel")

        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setGeometry(QtCore.QRect(370, 210, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        self.statusLabel.setFont(font)
        self.statusLabel.setStyleSheet("font-size: 20px;\n"
"font-weight: bold;")
        self.statusLabel.setObjectName("statusLabel")

        self.portNumberLabel = QtWidgets.QLabel(self.centralwidget)
        self.portNumberLabel.setGeometry(QtCore.QRect(20, 250, 120, 21))
        self.portNumberLabel.setStyleSheet("font-size: 20px;")
        self.portNumberLabel.setObjectName("portNumberLabel")

        self.bitsNumberLabel = QtWidgets.QLabel(self.centralwidget)
        self.bitsNumberLabel.setGeometry(QtCore.QRect(20, 280, 121, 31))
        self.bitsNumberLabel.setStyleSheet("font-size: 20px;")
        self.bitsNumberLabel.setObjectName("bitsNumberLabel")

        self.bitsNumberComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.bitsNumberComboBox.setGeometry(QtCore.QRect(143, 285, 80, 22))
        self.bitsNumberComboBox.setStyleSheet("font-size: 20px;")
        self.bitsNumberComboBox.setObjectName("bitsNumberComboBox")
        self.fillBitsNumberComboBox()

        self.portNumberComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.portNumberComboBox.setGeometry(QtCore.QRect(143, 250, 80, 22))
        self.portNumberComboBox.setStyleSheet("font-size: 20px;")
        self.portNumberComboBox.setObjectName("portNumberComboBox")
        self.fillPortNumberComboBox()

        self.baudRateLabel = QtWidgets.QLabel(self.centralwidget)
        self.baudRateLabel.setGeometry(QtCore.QRect(370, 420, 91, 21))
        self.baudRateLabel.setStyleSheet("font-size: 20px;")
        self.baudRateLabel.setObjectName("baudRateLabel")

        self.sentBytesLabel = QtWidgets.QLabel(self.centralwidget)
        self.sentBytesLabel.setGeometry(QtCore.QRect(370, 390, 101, 21))
        self.sentBytesLabel.setStyleSheet("font-size: 20px;")
        self.sentBytesLabel.setObjectName("sentBytesLabel")

        self.sentBytesValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.sentBytesValueLabel.setGeometry(QtCore.QRect(473, 390, 50, 21))
        self.sentBytesValueLabel.setStyleSheet("font-size: 20px;")
        self.sentBytesValueLabel.setText("")
        self.sentBytesValueLabel.setObjectName("sentBytesValueLabel")

        self.baudRateValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.baudRateValueLabel.setGeometry(QtCore.QRect(467, 420, 50, 21))
        self.baudRateValueLabel.setStyleSheet("font-size: 20px;")
        self.baudRateValueLabel.setText("")
        self.baudRateValueLabel.setObjectName("baudRateValueLabel")

        self.statusTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.statusTextEdit.setEnabled(True)
        self.statusTextEdit.setGeometry(QtCore.QRect(370, 240, 300, 131))
        self.statusTextEdit.setReadOnly(True)
        self.statusTextEdit.setObjectName("statusTextEdit")

        PortApp.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PortApp)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 22))
        self.menubar.setObjectName("menubar")
        PortApp.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PortApp)
        self.statusbar.setObjectName("statusbar")
        PortApp.setStatusBar(self.statusbar)

        self.retranslateUi(PortApp)
        QtCore.QMetaObject.connectSlotsByName(PortApp)

        self.openPort()
        self.portNumberComboBox.currentIndexChanged.connect(self.onChangePort)

    def retranslateUi(self, PortApp):
        _translate = QtCore.QCoreApplication.translate
        PortApp.setWindowTitle(_translate("PortApp", "PortApp"))
        self.inputLabel.setText(_translate("PortApp", "Input"))
        self.outputLabel.setText(_translate("PortApp", "Output"))
        self.controlLabel.setText(_translate("PortApp", "Control"))
        self.statusLabel.setText(_translate("PortApp", "Status"))
        self.portNumberLabel.setText(_translate("PortApp", "Port number:"))
        self.bitsNumberLabel.setText(_translate("PortApp", "Bits per byte:"))
        self.baudRateLabel.setText(_translate("PortApp", "Baud rate:"))
        self.sentBytesLabel.setText(_translate("PortApp", "Sent bytes:"))

    def fillPortNumberComboBox(self):
        availablePorts: list[QSerialPortInfo] = QSerialPortInfo.availablePorts()
        currentPort: str = self.portNumberComboBox.currentText()
        if availablePorts:
            self.portNumberComboBox.blockSignals(True)
            self.portNumberComboBox.clear()

            for availablePort in availablePorts:
                self.portNumberComboBox.addItem(availablePort.portName())

            currentIndex: int = self.portNumberComboBox.findText(currentPort)

            if currentIndex != -1:
                self.portNumberComboBox.setCurrentIndex(currentIndex)

            self.portNumberComboBox.blockSignals(False)
        else:
            QMessageBox.warning(None, "Error", "No available COM-Ports")
            sys.exit(app.exec_())

    def fillBitsNumberComboBox(self):
        self.bitsNumberComboBox.clear()
        for item in bitsNumberComboBoxItems:
            self.bitsNumberComboBox.addItem(item)

    def openPort(self):
        if not self.port.isOpen():
            self.configurePort()
            if not self.tryOpenPort(self.port.portName()):
                availablePorts: list[QSerialPortInfo] = QSerialPortInfo.availablePorts()
                for availablePort in availablePorts:
                    if self.tryOpenPort(availablePort.portName()):
                        self.portNumberComboBox.setCurrentText(availablePort.portName())
                        self.port.setPortName(availablePort.portName())
                        break
                else:
                    QMessageBox.warning(None, "Error", "No available COM-Ports found")
                    sys.exit(app.exec_())
            self.port.open(QtCore.QIODevice.ReadWrite)

    def tryOpenPort(self, portName: str) -> bool:
        port: QSerialPort = QSerialPort()
        port.setPortName(portName)
        if port.open(QtCore.QIODevice.ReadWrite):
            port.close()
            return True
        else:
            return False

    def configurePort(self):
        portName: str = self.portNumberComboBox.currentText()
        self.port.setPortName(portName)

        baudRate: int = 9600
        self.port.setBaudRate(baudRate)

        dataBits: int = int(self.bitsNumberComboBox.currentText()[0])
        self.port.setDataBits(dataBits)

        self.port.setParity(QSerialPort.Parity.NoParity)
        self.port.setStopBits(QSerialPort.StopBits.OneStop)
        self.port.setFlowControl(QSerialPort.FlowControl.NoFlowControl)

    def onInputTextChanged(self, event):
        QtWidgets.QTextEdit.keyPressEvent(self.inputTextEdit, event)
        if event.key() == QtCore.Qt.Key_Return:
            self.onSendBytes()
        else:
            data: str = self.inputTextEdit.toPlainText()
            cursorPosition: int = self.inputTextEdit.textCursor().position()
            for ch in data:
                if ch != '0' and ch != '1':
                    data = data.replace(ch, "")
                    cursorPosition -= 1
                    self.inputTextEdit.clear()
                    self.inputTextEdit.setPlainText(data)
                    cursor: QTextCursor = self.inputTextEdit.textCursor()
                    cursor.setPosition(cursorPosition)
                    self.inputTextEdit.setTextCursor(cursor)
                    break



    def onSendBytes(self):
        input_data: str = self.inputTextEdit.toPlainText().replace("\n", "")
        data_list: list[str] = BitStaffingMethods.divide_str(input_data)
        data_to_send: str = ""
        for item in data_list:
            flag: str = "00000001"
            destinationAddress: str = "0000"
            sourceAddress: str = BitStaffingMethods.getSourceAddress(self.port.portName())
            data: str = BitStaffingMethods.getData(item)
            fcs: str = "0"

            staffedData: str = BitStaffingMethods.bitStaffing(destinationAddress + sourceAddress + data + fcs)
            data_to_send += flag + staffedData

        sendedBytesCount: int = len(data_to_send)

        self.port.write(data_to_send.encode())
        self.inputTextEdit.clear()

        self.sentBytesValueLabel.setText(str(sendedBytesCount))
        self.baudRateValueLabel.setText(str(self.port.baudRate()))


    def onRecieveBytes(self):
        recieved_data = self.port.readAll().data().decode()
        if len(recieved_data) == 0:
            QMessageBox.warning(None, "Error", "Data cannot be read")
            sys.exit(app.exec_())
        else:
            data_list: list[str] = BitStaffingMethods.split_on_packages(recieved_data)
            data_to_output: str = ""
            highlightedData: str = ""
            for data in data_list:
                highlightedData += data[0:8:1]
                highlightedData += BitStaffingMethods.getHighlightedBits(data[8::1])
                highlightedData += '\n'

                destaffedData = BitStaffingMethods.debitStaffing(data)
                destaffedData = destaffedData[8:-1:1]
                data_to_output += destaffedData
            self.outputTextEdit.setText(data_to_output)
            self.statusTextEdit.setText(highlightedData)
            self.baudRateValueLabel.setText(str(self.port.baudRate()))



    def onChangePort(self, index):
        if self.port.isOpen():
            self.port.close()
        self.fillBitsNumberComboBox()
        self.fillPortNumberComboBox()
        self.openPort()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PortApp = QtWidgets.QMainWindow()
    ui = Ui_PortApp(PortApp)
    ui.setupUi(PortApp)
    PortApp.show()
    sys.exit(app.exec_())
