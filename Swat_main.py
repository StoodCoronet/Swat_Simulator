from real_plc import plc1, plc2, plc3, plc4, plc5, plc6
import sys, os

sys.path.insert(0, os.getcwd())
from SCADA import H
from IO import *
from plant.plant import plant
import SWaT

from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout, QLabel, QMainWindow
import time
class WinForm(QMainWindow, SWaT.Ui_MainWindow):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle('example')
        #layout = QGridLayout()

        #self.myLable = QLabel('hello world', self)
        #self.btnStart=QPushButton('start')

        #layout.addWidget(self.myLable, 2, 2)
        #layout.addWidget(self.btnStart,1,1)

        self.StartBtn.clicked.connect(self.slotRun)
        self.StopBtn.clicked.connect(self.slotStop)
        self.StepBtn.clicked.connect(self.oneStep)
        self.ChangeVal.clicked.connect(self.changeValue)
        #self.setLayout(layout)

        self.data_set = []
        self.path = "data/normal.npy"
        self.time_interval = 1
        self.log_path = ''
        self.maxstep = 60 * 60 * 10
        # Initiating Plant
        self.Plant = plant(self.log_path, self.time_interval, self.maxstep)
        # Defining I/O
        self.IO_DI_WIFI = DI_WIFI()
        self.IO_P1 = P1()
        self.IO_P2 = P2()
        self.IO_P3 = P3()
        self.IO_P4 = P4()
        self.IO_P5 = P5()
        self.IO_P6 = P6()
        # print ("Initializing SCADA HMI")
        self.HMI = H()
        # print ("Initializing PLCs\n")
        self.PLC1 = plc1.plc1(self.HMI)
        self.PLC2 = plc2.plc2(self.HMI)
        self.PLC3 = plc3.plc3(self.HMI)
        self.PLC4 = plc4.plc4(self.HMI)
        self.PLC5 = plc5.plc5(self.HMI)
        self.PLC6 = plc6.plc6(self.HMI)
        # print ("Now starting Simulation")
        self.timestamp = 0
        self.isRunning = False


    def slotAdd(self, time_t):
        #for time_t in range(0, self.maxstep):
        Sec_P = not bool(time_t % (1 / self.time_interval))
        Min_P = not bool(time_t % (60 / self.time_interval))
        self.Plant.Actuator(self.IO_P1, self.IO_P2, self.IO_P3, self.IO_P4, self.IO_P5, self.IO_P6)
        Out1, Out2, Out3 = self.Plant.Plant(self.IO_P1, self.IO_P2, self.IO_P3, self.IO_P4, self.IO_P5, self.IO_P6, time_t, self.HMI)
        # #PLC working
        self.PLC1.Pre_Main_Raw_Water(self.IO_P1, self.HMI)
        self.PLC2.Pre_Main_UF_Feed_Dosing(self.IO_P2, self.HMI)
        self.PLC3.Pre_Main_UF_Feed(self.IO_P3, self.HMI, Sec_P, Min_P)
        self.PLC4.Pre_Main_RO_Feed_Dosing(self.IO_P4, self.HMI, )
        self.PLC5.Pre_Main_High_Pressure_RO(self.IO_P5, self.HMI, Sec_P, Min_P)
        self.PLC6.Pre_Main_Product(self.IO_P6, self.HMI)
        #print(tmp)
        self.LabOutput1.setText(str(Out1))
        self.LabOutput2.setText(str(Out2))
        self.LabOutput3.setText(str(Out3))
        #self.myLable.setText(str(tmp))
        QApplication.processEvents()
        #time.sleep(0.1)

    def slotRun(self):
        self.isRunning = True
        while self.timestamp < self.maxstep:
            if self.isRunning:
                self.slotAdd(self.timestamp)
                self.timestamp += 1
            else:
                break

    def slotStop(self):
        self.isRunning = False

    def oneStep(self):
        self.isRunning = False
        if self.timestamp < self.maxstep:
            self.slotAdd(self.timestamp)
            self.timestamp += 1

    def changeValue(self): # I don't know what's these values, just call it result#num
        self.isRunning = False
        result0 = int(self.ChangeVal0.text())
        result1 = int(self.ChangeVal1.text())
        result2 = int(self.ChangeVal2.text())
        result3 = int(self.ChangeVal3.text())
        result4 = int(self.ChangeVal4.text())
        self.Plant.changeValueBF(result0, result1, result2, result3, result4, self.timestamp)
        self.timestamp += 1

if __name__ == '__main__':
    app=QApplication(sys.argv)
    #MainWindow = QMainWindow()
    #ui = SWaT.Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()

    #win=WinForm()
    #win.show()

    MainWindow = WinForm()
    MainWindow.show()
    sys.exit(app.exec_())
