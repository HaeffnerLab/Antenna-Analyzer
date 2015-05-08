# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotSNA.ui'
#
# Created: Mon Apr 20 18:06:48 2015
#      by: PyQt4 UI code generator 4.11.3
#      by: Silje Skeide Fuglerud

from PyQt4 import QtCore, QtGui
import sys, serial, time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget): 

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.filename=""
        self.txtfilename=""
        self.txt=False
        self.setupUi(self)
        self.start=1
        self.stop=2
        self.steps=50
        # Connect with arduino
        self.ser = serial.Serial("COM3", 9600, timeout = 1)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(892, 661)

        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        #Make menubar
        #menubar = QMenuBar()
        #self.verticalLayout.addWidget(menubar)
        #file_menu=menubar.addMenu('File')

        #exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit application')
        #exitAction.triggered.connect(QtGui.qApp.quit)
        #file_menu.addAction(exitAction)

        #First Line
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        #Create a label - in retranslateUI set it to Start Frequency
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_12.addWidget(self.label)
        #Create a spinbox to control start frequency
        self.spinBox_1 = QtGui.QSpinBox(Form)
        self.spinBox_1.setObjectName(_fromUtf8("spinBox_1"))
        self.spinBox_1.setRange(1, 59)
        self.spinBox_1.setSingleStep(1)
        self.horizontalLayout_12.addWidget(self.spinBox_1) 
        #Define function to catch a change in the spinbox's position, and make sure start frequency is not bigger than stop frequency
        self.spinBox_1.valueChanged.connect(self.catch_val_start)
        #Display MHz
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_12.addWidget(self.label_5)
        #Make space inbetween
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem)
        #Define save figure-button
        self.sfbtn = QtGui.QPushButton('Save figure', self)
        self.sfbtn.clicked.connect(self.saveffunc)
        self.horizontalLayout_12.addWidget(self.sfbtn)
        #Define save data-button
        self.sdbtn = QtGui.QPushButton('Save data', self)
        self.sdbtn.clicked.connect(self.savedfunc)
        self.horizontalLayout_12.addWidget(self.sdbtn)

        #Second line
        self.verticalLayout.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        #Create a label - in retranslateUI set it to Number of steps
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_11.addWidget(self.label_2)
        #Create a spinbox with step 50
        self.spinBox_2 = QtGui.QSpinBox(Form)
        self.spinBox_2.setObjectName(_fromUtf8("spinBox_2"))
        self.spinBox_2.setRange(50, 500)
        self.spinBox_2.setSingleStep(50)
        self.horizontalLayout_11.addWidget(self.spinBox_2)            
        #More space
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        #Create change button
        self.setbtn = QtGui.QPushButton('Set arguments', self)
        self.setbtn.clicked.connect(self.setArguments)
        self.horizontalLayout_11.addWidget(self.setbtn)

        #Third line
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        #Create a label - in retranslateUI set it to Stop frequency
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_9.addWidget(self.label_3)
        #Create a spinbox to control stop frequency. 
        self.spinBox_3 = QtGui.QSpinBox(Form)
        self.spinBox_3.setObjectName(_fromUtf8("spinBox_3"))
        self.spinBox_3.setRange(2, 60)
        self.spinBox_3.setSingleStep(1)
        self.horizontalLayout_9.addWidget(self.spinBox_3) 
        #Define function to catch a change in the spinbox's position. In the function catch_val_stop make sure stop frequency has a higher value than start 
        self.spinBox_3.valueChanged.connect(self.catch_val_stop)            
        #Display the sliders value
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_9.addWidget(self.label_6)
        #More space
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        #Create quit button
        self.qbtn = QtGui.QPushButton('Quit', self)
        self.qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.horizontalLayout_9.addWidget(self.qbtn)

        #Initialize figure
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.figure.suptitle('Finding The Resonance Frequency of The Testing Device')
        self.verticalLayout.addWidget(self.canvas)
        self.horizontalLayout.addLayout(self.verticalLayout)

        #Set label names
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Antenna Analyzer", None))
        self.label.setText(_translate("Form", "Start Frequency", None))
        self.label_2.setText(_translate("Form", "Number of steps", None))
        self.label_3.setText(_translate("Form", "Stop Frequency", None))
        self.label_5.setText(_translate("Form", "MHz", None))
        self.label_6.setText(_translate("Form", "MHz", None))

    @pyqtSlot()
    def catch_val_start(self):
        val = self.spinBox_1.value()
        #self.label_5.setText(_translate("Form", str(val)+" MHz", None))
        if self.spinBox_3.value()<val:
            self.spinBox_3.setValue(val)
            #self.label_6.setText(_translate("Form", str(val)+" MHz", None))

    @pyqtSlot()
    def catch_val_stop(self):
        val = self.spinBox_3.value()
        #self.label_6.setText(_translate("Form", str(val)+" MHz", None))
        if self.spinBox_1.value()>val:
            self.spinBox_1.setValue(val)
            #self.label_5.setText(_translate("Form", str(val)+" MHz", None))
   

    def run(self, line, resonance_text,qFactor_text,gamma_text):
        def init():
            line.set_data([], [])
            return line, resonance_text, qFactor_text, gamma_text
        
        # animation function.  This is called sequentially
        def update(n):
            #print "frame number: " + str(n)
            dataFreq = []
            dataGamma = []
            #dataFwd=[]
            #dataRev=[]
            self.ser.write('s')

            if self.txt:
                txtfile= open(self.txtfilename, 'a')                    

            for i in range(self.steps + 1):
                inputStr = self.ser.readline()
                time.sleep(.005) # Delay
                
                # See arduino file - SNA.ino - for more info
                nspaces=inputStr.count(" ")
                if nspaces<1:
                    print("Not enough data")
                    quit
                strValues=[str(x) for x in inputStr.split()]
                if self.txt:
                    #Write: freq gamma FWD REV
                    txtfile.write((strValues[0])+" "+(strValues[1])+" "+(strValues[2])+" "+(strValues[3])+"\n")
            
                #freq, gamma, fwd, rev, dump = inputStr.split(" ")
                dataFreq.append(float(strValues[0]))
                dataGamma.append(float(strValues[1]))
                #dataFwd.append(float(strValues[2]))
                #dataRev.append(float(strValues[3]))

            # Find the resonance frequency
            minGamma = min(dataGamma)
            maxGamma=max(dataGamma)
            resonanceIndex = dataGamma.index(minGamma)
            resonanceFreq = dataFreq[resonanceIndex]
            # Find the quality factor by finding the freq just outside
            # the half-max bandwidth (1/2 max power)
            # When we can't find the freq outside the bandwidth
            # we use
            highF = self.stop
            lowF = self.start
            # Find the highest freq of the bandwidth
            for k in range(resonanceIndex, self.steps):
                if (dataGamma[k] > maxGamma - float(maxGamma-minGamma)/2):
                    highF = dataFreq[k]
                    break
            # Find the lowest freq in the bandwidth
            for k in range(resonanceIndex, 0, -1):
                if (dataGamma[k] > maxGamma - float(maxGamma-minGamma)/2):
                    lowF = dataFreq[k]
                    break
            if (highF == lowF):
                Q = float("inf")
            else:
                Q = resonanceFreq / (highF - lowF)
                
            resonance_text.set_text('Resonance Freq is %.2f MHz' % resonanceFreq)
            qFactor_text.set_text('Quality Factor is %.2f (%.2f MHz, %.2f MHz)' % (Q, lowF, highF))
            gamma_text.set_text('Minimum Reflected Power is %.4f %%' % minGamma)
            # update the line
            line.set_data(np.asarray(dataFreq), np.asarray(dataGamma))
            if self.txt:
                print "Data saved as ", self.txtfilename
                txtfile.close()
                self.txt=False

            return line, resonance_text, qFactor_text, gamma_text
        
        anim=animation.FuncAnimation(self.figure, update, init_func=init,fargs=None, blit=False, repeat=True)                     
        self.canvas.draw()
        return anim

    @pyqtSlot()
    def setArguments(self):
        time.sleep(.1)
        self.start=self.spinBox_1.value()
        self.stop=self.spinBox_3.value()
        self.steps=self.spinBox_2.value()

        for i in range(len(str(self.start))):
            self.ser.write(str(self.start)[i])
        # Tell arduino that those previous numbers are for the starting frequency
        self.ser.write('A')

        for i in range(len(str(self.stop))):
            self.ser.write(str(self.stop)[i])
        # Tell arduino that those previous numbers are for the stopping frequency
        self.ser.write('B')
        
        for i in range(len(str(self.steps))):
            self.ser.write(str(self.steps)[i])
        # Tell arduino that those previous numbers are for the number of steps
        self.ser.write('N')

        data = self.ser.readline()
        if data:
            print data.rstrip('\n') #strip out the new lines for now
            #(better to do .read() in the long run for this reason 
        #ser.write('s')
        print "start:", self.start, " stop:", self.stop, " steps:", self.steps
        #time.sleep(.5)
        self.ax=self.figure.add_subplot(111)

        self.ax.hold(False)
        line, = self.ax.plot([], [], lw=2)

        self.ax.set_xlim(self.start,self.stop)
        self.ax.set_ylim(0,125)
        self.ax.set_xlabel('Frequency (MHz)')
        self.ax.set_ylabel('Reflected Power (%)')
        self.ax.grid()

        # Resonance stands for the resonance frequency
        resonance_text = self.ax.text(0.02, 0.95, ' ', transform = self.ax.transAxes)
        # qFactor stands for Quality factor: Q = f/df where f is the resonance freq
        # and df is the half-power bandwidth
        qFactor_text = self.ax.text(0.02,0.90, ' ', transform = self.ax.transAxes)
        # Gamma in this context means the reflected power
        gamma_text = self.ax.text(0.02, 0.85, ' ', transform = self.ax.transAxes)
        #self.ser.flushInput()
        anim=self.run(line, resonance_text,qFactor_text,gamma_text)

    @pyqtSlot()
    def closeEvent(self, event): 
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure that you want to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 

    @pyqtSlot()
    def saveffunc(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        if not self.filename.endsWith('.png'):
            self.filename+='.png'
            #must be saved as png
        pixmap = QPixmap.grabWidget(self.canvas)
        pixmap.save(self.filename)
        print "Figure saved as ", self.filename

    @pyqtSlot()
    def savedfunc(self):    
        self.txtfilename = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        if not self.txtfilename.endsWith('.txt'):
            self.txtfilename+='.txt'
            #must be saved as txt
        self.txt=True

    
if __name__=='__main__':
    #anim=main()
    app=QtGui.QApplication(sys.argv)
    ex=Ui_Form()
    ex.show()
    sys.exit(app.exec_())
