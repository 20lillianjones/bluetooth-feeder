from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from feederUI import Feeder_UI
import sys

appOne = QApplication(sys.argv)
windowOne = Feeder_UI()
windowOne.show()
sys.exit(appOne.exec_())