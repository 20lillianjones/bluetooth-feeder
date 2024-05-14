from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from datetime import datetime
import csv
import os
import serial
from google.cloud import storage

#Use the Google Cloud Storage API so that the same feeding log can be displayed and updated from different devices:
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'serviceKey.json'
#Bucket name = 'feeder-new'

#Initialize Serial object to connect to HC-05 Bluetooth module:
bluetoothObject = serial.Serial('COM10', 9600, timeout=1) #Change COM depending on assigned port

class Feeder_UI(QMainWindow):
    #Initialization function:
    def __init__(self):
        super(Feeder_UI, self).__init__()
        uic.loadUi("feederUI.ui", self)

        #Variables:
        self.BUCKET_NAME = 'feeder-new'
        self.BLOB_NAME = 'feederLog'
        self.storageClient = storage.Client()
        self.myBucket = self.storageClient.get_bucket(self.BUCKET_NAME)
        self.downloadFromBucket()

        self.feederName = ""
        self.feedAmount = None
        self.currentDateTime = ""
        self.feedTriple = []
        self.readFromCSV()
        self.loadToTable()

        #Set the initial button colors:
        self.pushButtonOne.setStyleSheet("background-color : #e2e2e2") 
        self.pushButtonTwo.setStyleSheet("background-color : #e2e2e2") 
        self.pushButtonThree.setStyleSheet("background-color : #e2e2e2")

        #Disable push buttons until a name is entered:
        self.frameButtons.setEnabled(False)
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Amount", "Time"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True) 
        self.tableWidget.horizontalHeader().setSectionResizeMode( 
            QHeaderView.Stretch) 

        #Signals connected to buttons:
        self.comboBoxName.activated.connect(self.getFeederName)
        self.pushButtonOne.clicked.connect(self.pushButtonOnePressed)
        self.pushButtonTwo.clicked.connect(self.pushButtonTwoPressed)
        self.pushButtonThree.clicked.connect(self.pushButtonThreePressed)
        self.pushButtonClear.clicked.connect(self.clearFeederLog)
    
    def clearFeederLog(self):
        self.feedTriple.clear()
        self.appendToCSV()
        self.tableWidget.setRowCount(0)
    
    def uploadToBucket(self):
        filePathOne = r'C:\Users\20lil\OneDrive - University of Pittsburgh\Documents\PITT - Spring 2024\ECE 1895 - Junior Design\Final Project'
        filePath = os.path.join(filePathOne, 'feedLog.csv')
        blobOne = self.myBucket.blob(self.BLOB_NAME)
        blobOne.upload_from_filename(filePath)
    
    def downloadFromBucket(self):
        filePathOne = r'C:\Users\20lil\OneDrive - University of Pittsburgh\Documents\PITT - Spring 2024\ECE 1895 - Junior Design\Final Project'
        filePath = os.path.join(filePathOne, 'feedLog.csv')
        blobOne = self.myBucket.blob(self.BLOB_NAME)
        with open(filePath, 'wb') as f:
            self.storageClient.download_blob_to_file(blobOne, f)

    def keepAtTen(self):
        while len(self.feedTriple) >= 10:
            self.feedTriple.reverse()
            self.feedTriple.pop()
            self.feedTriple.reverse()   
    
    def readFromCSV(self):
        with open("feedLog.csv", "r") as fileObject:
            fileReader = csv.reader(fileObject, delimiter=",")
            for line in enumerate(fileReader):
                self.feedTriple.append(line[1])
        self.feedTriple.reverse()

    #Function to get the name of the current feeder:
    def getFeederName(self):
        self.pushButtonOne.setStyleSheet("background-color : #e2e2e2") 
        self.pushButtonTwo.setStyleSheet("background-color : #e2e2e2") 
        self.pushButtonThree.setStyleSheet("background-color : #e2e2e2")
        self.pushButtonOne.setEnabled(True)
        self.pushButtonTwo.setEnabled(True)
        self.pushButtonThree.setEnabled(True)

        self.feederName = self.comboBoxName.currentText()
        self.frameButtons.setEnabled(True)

    def pushButtonOnePressed(self):
        self.pushButtonOne.setStyleSheet("background-color : #FFA03D") 
        self.pushButtonTwo.setEnabled(False)
        self.pushButtonThree.setEnabled(False)
        self.feedAmount = "Just a Snack"
        now = datetime.now()
        self.currentDateTime = now.strftime("%m/%d/%Y %H:%M:%S")
        self.feedTriple.append([self.feederName, self.feedAmount, self.currentDateTime])

        #Specify Arduino operation with Serial character:
        tempDat = 'A'
        bluetoothObject.write(tempDat.encode())

        self.keepAtTen()
        self.appendToCSV()
        self.loadToTable()

    def pushButtonTwoPressed(self):
        self.pushButtonTwo.setStyleSheet("background-color : #FFA03D") 
        self.pushButtonOne.setEnabled(False)
        self.pushButtonThree.setEnabled(False)
        self.feedAmount = "Lunch Time"
        now = datetime.now()
        self.currentDateTime = now.strftime("%d/%m/%Y %H:%M:%S")
        self.feedTriple.append([self.feederName, self.feedAmount, self.currentDateTime])

        #Specify Arduino operation with Serial character:
        tempDat = 'B'
        bluetoothObject.write(tempDat.encode())

        self.keepAtTen()
        self.appendToCSV()
        self.loadToTable()
    
    def pushButtonThreePressed(self):
        self.pushButtonThree.setStyleSheet("background-color : #FFA03D")
        self.pushButtonOne.setEnabled(False)
        self.pushButtonTwo.setEnabled(False)
        self.feedAmount = "CHOW DOWN!"
        now = datetime.now()
        self.currentDateTime = now.strftime("%d/%m/%Y %H:%M:%S")
        self.feedTriple.append([self.feederName, self.feedAmount, self.currentDateTime])

        #Specify Arduino operation with Serial character:
        tempDat = 'C'
        bluetoothObject.write(tempDat.encode())

        self.keepAtTen()
        self.appendToCSV()
        self.loadToTable()
    
    def appendToCSV(self):
        self.feedTriple.reverse()
        with open('feedLog.csv', 'w', newline='') as fileObject:
            writerObject = csv.writer(fileObject)
            writerObject.writerows(self.feedTriple)
        self.uploadToBucket()
        self.feedTriple.reverse()
    
    def loadToTable(self):
        if len(self.feedTriple) == 0:
            return
        
        self.feedTriple.reverse()
        self.tableWidget.setRowCount(len(self.feedTriple))
        self.tableWidget.setColumnCount(len(self.feedTriple[0]))
        for i, row in enumerate(self.feedTriple):
            for j, column in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(column))
        self.feedTriple.reverse()