#!/usr/bin/python3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import os.path
import pickle
import socket
import _thread
import time
import math
import sys

class App(QTabWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'CSI Data Collection Tool'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 500
        self.Devices = list()

        self.Port = 5005

        self.initUI()

    def initUI(self):
        #set title
        self.setWindowTitle(self.title)
        #set window size
        self.setGeometry(self.left, self.top, self.width, self.height)
        #set font
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.CollectDataTab = QWidget()
        self.addTab(self.CollectDataTab, "Collect Data")

        self.AddDevicesTab = QWidget()
        self.addTab(self.AddDevicesTab, "Add Devices")

        self.SettingsTab = QWidget()
        self.addTab(self.SettingsTab, "Settings")
 
        self.CollectDataTabUI()
        self.AddDevicesTabUI()
        self.SettingsTabUI()

        #display window
        self.show()

    def AddDevicesTabUI(self):
        self.AddDevicesTab.layout = QWidget(self.AddDevicesTab)

        self.Label14 = QLabel("Name", self.AddDevicesTab.layout)
        self.Label14.setGeometry(QRect(20, 20, 150, 20))
        self.LineEdit7 = QLineEdit(self.AddDevicesTab.layout)
        self.LineEdit7.setGeometry(QRect(120, 20, 150, 20))

        self.Label9 = QLabel("IP Address", self.AddDevicesTab.layout)
        self.Label9.setGeometry(QRect(20, 50, 150, 20))
        self.LineEdit4 = QLineEdit(self.AddDevicesTab.layout)
        self.LineEdit4.setGeometry(QRect(120, 50, 150, 20))
        self.LineEdit4.setInputMask('000.000.000.000')
        
        self.AddDevicesTab.layout.DeviceType = QWidget(self.AddDevicesTab.layout)
        self.AddDevicesTab.layout.DeviceType.setGeometry(20, 80, 600, 20)
        self.Label17 = QLabel("Device Type", self.AddDevicesTab.layout.DeviceType)
        self.Label17.setGeometry(QRect(0, 0, 200, 20))
        self.RadioButton8 = QRadioButton("Transmitter", self.AddDevicesTab.layout.DeviceType)
        self.RadioButton8.setGeometry(QRect(100, 0, 100, 20))
        self.RadioButton9 = QRadioButton("Receiver ", self.AddDevicesTab.layout.DeviceType)
        self.RadioButton9.setGeometry(QRect(200, 0, 100, 20))
        self.RadioButton9.setChecked(True)

        self.PushButton2 = QPushButton("Add", self.AddDevicesTab.layout)
        self.PushButton2.setGeometry(QRect(350, 80, 80, 20))
        self.PushButton2.clicked.connect(self.Add)

        self.PushButton4 = QPushButton("Remove", self.AddDevicesTab.layout)
        self.PushButton4.setGeometry(QRect(530, 440, 80, 20))
        self.PushButton4.clicked.connect(self.Remove)

        self.Label15 = QLabel("Devices", self.AddDevicesTab.layout)
        self.Label15.setStyleSheet("font-weight: bold")
        self.Label15.setGeometry(QRect(20, 190, 150, 20))
        self.Label16 = QLabel("{:<42} {:<41} {:<40}".format("Name", "IP Address", "Type"), self.AddDevicesTab.layout)
        self.Label16.setGeometry(QRect(20, 210, 600, 20))

        self.AddDevicesTab.layout.Name = QListWidget(self.AddDevicesTab.layout)
        self.AddDevicesTab.layout.Name.setGeometry(20, 230, 199, 200)
        self.AddDevicesTab.layout.Name.itemClicked.connect(self.ListSelectName)
        self.AddDevicesTab.layout.IP = QListWidget(self.AddDevicesTab.layout)
        self.AddDevicesTab.layout.IP.setGeometry(220, 230, 199, 200)
        self.AddDevicesTab.layout.IP.itemClicked.connect(self.ListSelectIP)
        self.AddDevicesTab.layout.Type = QListWidget(self.AddDevicesTab.layout)
        self.AddDevicesTab.layout.Type.setGeometry(420, 230, 199, 200)
        self.AddDevicesTab.layout.Type.itemClicked.connect(self.ListSelectType)

    def SettingsTabUI(self):
        self.SettingsTab.layout = QWidget(self.SettingsTab)

        self.SettingsTab.layout.RFBand = QWidget(self.SettingsTab.layout)
        self.SettingsTab.layout.RFBand.setGeometry(20, 20, 600, 20)
        self.Label4 = QLabel("RF Band", self.SettingsTab.layout.RFBand)
        self.Label4.setGeometry(QRect(0, 0, 200, 20))
        self.RadioButton1 = QRadioButton("2.4 GHz", self.SettingsTab.layout.RFBand)
        self.RadioButton1.setGeometry(QRect(210, 0, 100, 20))
        self.RadioButton1.toggled.connect(self.SetChannels)
        self.RadioButton2 = QRadioButton("5 GHz", self.SettingsTab.layout.RFBand)
        self.RadioButton2.setGeometry(QRect(310, 0, 100, 20))
        self.RadioButton2.toggled.connect(self.SetChannels)

        self.SettingsTab.layout.NumberOfSeconds = QWidget(self.SettingsTab.layout)
        self.SettingsTab.layout.NumberOfSeconds.setGeometry(20, 50, 600, 20)
        self.Label2 = QLabel("Number of seconds", self.SettingsTab.layout.NumberOfSeconds)
        self.Label2.setGeometry(QRect(0, 0, 150, 20))
        self.LineEdit2 = QLineEdit("10", self.SettingsTab.layout.NumberOfSeconds)
        self.LineEdit2.setGeometry(QRect(210, 0, 50, 20))
        self.LineEdit2.setValidator(QIntValidator(1, 86400))
        self.LineEdit2.setMaxLength(5)

        self.SettingsTab.layout.PacketsPerSecond = QWidget(self.SettingsTab.layout)
        self.SettingsTab.layout.PacketsPerSecond.setGeometry(20, 80, 600, 20)
        self.Label3 = QLabel("Packets per second", self.SettingsTab.layout.PacketsPerSecond)
        self.Label3.setGeometry(QRect(0, 0, 150, 20))
        self.LineEdit3 = QLineEdit("2000", self.SettingsTab.layout.PacketsPerSecond)
        self.LineEdit3.setGeometry(QRect(210, 0, 40, 20))
        self.LineEdit3.setValidator(QIntValidator(1, 2000))
        self.LineEdit3.setMaxLength(4)

        self.SettingsTab.layout.Channel = QWidget(self.SettingsTab.layout)
        self.SettingsTab.layout.Channel.setGeometry(20, 110, 600, 20)
        self.Label12 = QLabel("Channel", self.SettingsTab.layout.Channel)
        self.Label12.setGeometry(QRect(0, 0, 150, 20))
        self.ComboBox2 = QComboBox(self.SettingsTab.layout.Channel)
        self.ComboBox2.setGeometry(QRect(210, 0, 50, 20))
        self.RadioButton2.setChecked(True)

        self.SettingsTab.layout.Power = QWidget(self.SettingsTab.layout)
        self.SettingsTab.layout.Power.setGeometry(20, 140, 600, 20)
        self.Label13 = QLabel("Power", self.SettingsTab.layout.Power)
        self.Label13.setGeometry(QRect(0, 0, 150, 20))
        self.SpinBox1 = QSpinBox(self.SettingsTab.layout.Power)
        self.SpinBox1.setGeometry(QRect(210, 0, 50, 20))
        self.SpinBox1.setRange(0, 30)
        self.SpinBox1.setValue(15)

        self.SettingsTab.layout.MAC = QWidget(self.SettingsTab.layout)
        self.SettingsTab.layout.MAC.setGeometry(20, 170, 600, 20)
        self.Label18 = QLabel("MAC Address", self.SettingsTab.layout.MAC)
        self.Label18.setGeometry(QRect(0, 0, 150, 20))
        self.LineEdit5 = QLineEdit("00:1A:3F:F1:4C:C6" ,self.SettingsTab.layout.MAC)
        self.LineEdit5.setGeometry(QRect(210, 0, 130, 20))
        self.LineEdit5.setInputMask('HH:HH:HH:HH:HH:HH')

        self.SettingsTab.layout.Save = QWidget(self.SettingsTab.layout)
        self.SettingsTab.layout.Save.setGeometry(20, 200, 600, 20)
        self.PushButton3 = QPushButton("Save", self.SettingsTab.layout.Save)
        self.PushButton3.setGeometry(QRect(400, 0, 100, 20))
        self.PushButton3.clicked.connect(self.Save)

    def CollectDataTabUI(self):
        self.CollectDataTab.layout = QWidget(self.CollectDataTab)

        self.Label1 = QLabel("Filename", self.CollectDataTab.layout)
        self.Label1.setGeometry(QRect(20, 20, 150, 20))
        self.LineEdit1 = QLineEdit(self.CollectDataTab.layout)
        self.LineEdit1.setGeometry(QRect(100, 20, 150, 20))

        self.PushButton1 = QPushButton("Start", self.CollectDataTab.layout)
        self.PushButton1.setGeometry(QRect(350, 20, 100, 20))
        self.PushButton1.clicked.connect(self.Start)

    def ListSelectName(self):
        row = self.AddDevicesTab.layout.Name.currentRow()
        self.AddDevicesTab.layout.IP.setCurrentRow(row)
        self.AddDevicesTab.layout.Type.setCurrentRow(row)

    def ListSelectIP(self):
        row = self.AddDevicesTab.layout.IP.currentRow()
        self.AddDevicesTab.layout.Name.setCurrentRow(row)
        self.AddDevicesTab.layout.Type.setCurrentRow(row)

    def ListSelectType(self):
        row = self.AddDevicesTab.layout.Type.currentRow()
        self.AddDevicesTab.layout.IP.setCurrentRow(row)
        self.AddDevicesTab.layout.Name.setCurrentRow(row)

    def Add(self):
        if (self.LineEdit7.text() and self.LineEdit4.text() and (self.RadioButton8.isChecked() or self.RadioButton9.isChecked())):
            if not any((d["IP"] == self.LineEdit4.text() or d["Name"] == self.LineEdit7.text()) for d in self.Devices):
                if self.RadioButton9.isChecked():
                    DevType = "Receiver"
                else:
                    DevType = "Transmitter"

                self.Devices.append({"IP":self.LineEdit4.text(), "Name":self.LineEdit7.text(), "Type": DevType})
                self.AddDevicesTab.layout.Name.addItem(self.LineEdit7.text())
                self.AddDevicesTab.layout.IP.addItem(self.LineEdit4.text())
                self.AddDevicesTab.layout.Type.addItem(DevType)

                self.LineEdit7.clear()
                self.LineEdit4.clear()
                    
    def Remove(self):
        row = self.AddDevicesTab.layout.Name.currentRow()
        self.AddDevicesTab.layout.Name.takeItem(row)
        self.AddDevicesTab.layout.IP.takeItem(row)
        self.AddDevicesTab.layout.Type.takeItem(row)
        del self.Devices[row]

    def SetChannels(self):
        self.ComboBox2.clear()

        if (self.RadioButton2.isChecked()):
            self.ComboBox2.addItems(["36", "44", "149", "157"])   
        else:
            self.ComboBox2.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"])  

    def Start(self):	
        self.Save()

        time_start = math.floor(time.time())+2
        end_time = int(self.LineEdit2.text())+2
        for ind in range(len(self.Devices)):
            if self.Devices[ind]['Type'] == "Receiver":
                self.Devices[ind]['socket'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                self.Devices[ind]['socket'].connect((self.Devices[ind]['IP'],self.Port))
                self.Devices[ind]['socket'].send(str.encode("recv {} {} {}".format(str(self.LineEdit1.text()), str(end_time), str(time_start))))

        for ind in range(len(self.Devices)):
            if self.Devices[ind]['Type'] == "Transmitter":
                self.Devices[ind]['socket'] = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                self.Devices[ind]['socket'].connect((self.Devices[ind]['IP'],self.Port))
                self.Devices[ind]['socket'].send(str.encode("send {} {} {} {} {} {} {}".format(self.Band5, self.Channel, self.Power, self.MAC, str(int(int(self.LineEdit2.text()) * (1000000/self.Delay))), self.Delay, str(time_start))))
                self.Devices[ind]['socket'].close()

    def Save(self):
        if (self.RadioButton2.isChecked()):
        	self.Band5 = 1
        else:
        	self.Band5 = 0

        self.Channel = self.ComboBox2.currentText()
        self.Power = self.SpinBox1.value()
        self.MAC = self.LineEdit5.text()
        self.Delay = int(1000000/int(self.LineEdit3.text()))

    def showdialog(self, Text, Details=""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(Text)
        msg.setDetailedText(Details)
        msg.setWindowTitle("Error!!")
        retval = msg.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())