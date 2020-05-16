from PyQt5 import QtCore, QtGui, QtWidgets
import BusRouteOptimiser as GAM
from pyqtgraph import PlotWidget
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import pyqtgraph as pg

data=[0,0,0,0,0]
reg_ex=QRegExp("[0-9]+")
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(671, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lab_gen = QtWidgets.QLabel(self.centralwidget)
        self.lab_gen.setGeometry(QtCore.QRect(20, 10, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_gen.setFont(font)
        self.lab_gen.setObjectName("lab_gen")
        self.lab_pop = QtWidgets.QLabel(self.centralwidget)
        self.lab_pop.setGeometry(QtCore.QRect(130, 10, 101, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_pop.setFont(font)
        self.lab_pop.setObjectName("lab_pop")
        self.lab_route = QtWidgets.QLabel(self.centralwidget)
        self.lab_route.setGeometry(QtCore.QRect(260, 10, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_route.setFont(font)
        self.lab_route.setObjectName("lab_route")
        self.lab_mut = QtWidgets.QLabel(self.centralwidget)
        self.lab_mut.setGeometry(QtCore.QRect(400, 10, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_mut.setFont(font)
        self.lab_mut.setObjectName("lab_mut")
        self.lab_copy = QtWidgets.QLabel(self.centralwidget)
        self.lab_copy.setGeometry(QtCore.QRect(560, 10, 81, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lab_copy.setFont(font)
        self.lab_copy.setObjectName("lab_copy")
        self.line_gen = QtWidgets.QLineEdit(self.centralwidget)
        self.line_gen.setGeometry(QtCore.QRect(20, 50, 81, 20))
        self.line_gen.setObjectName("line_gen")
        self.line_gen.setToolTip("Number of generations. Must be an integer.")
        input_validator=QRegExpValidator(reg_ex,self.line_gen)
        self.line_gen.setValidator(input_validator)
        self.line_gen.editingFinished.connect(self.gen_equ)
        self.line_pop = QtWidgets.QLineEdit(self.centralwidget)
        self.line_pop.setGeometry(QtCore.QRect(140, 50, 81, 20))
        self.line_pop.setObjectName("line_pop")
        self.line_pop.setToolTip("Maximum population size. Must be an integer.")
        input_validator=QRegExpValidator(reg_ex,self.line_pop)
        self.line_pop.setValidator(input_validator)
        self.line_pop.editingFinished.connect(self.pop_equ)
        self.line_route = QtWidgets.QLineEdit(self.centralwidget)
        self.line_route.setGeometry(QtCore.QRect(270, 50, 81, 20))
        self.line_route.setObjectName("line_route")
        self.line_route.setToolTip("Maximum route size. Must be an integer.")
        input_validator=QRegExpValidator(reg_ex,self.line_route)
        self.line_route.setValidator(input_validator)
        self.line_route.editingFinished.connect(self.route_equ)
        self.line_mut = QtWidgets.QLineEdit(self.centralwidget)
        self.line_mut.setGeometry(QtCore.QRect(420, 50, 81, 20))
        self.line_mut.setObjectName("line_mut")
        self.line_mut.setToolTip("Probability of mutation in percentage. Must be an integer.")
        input_validator=QRegExpValidator(reg_ex,self.line_mut)
        self.line_mut.setValidator(input_validator)
        self.line_mut.editingFinished.connect(self.mut_equ)
        self.line_copy = QtWidgets.QLineEdit(self.centralwidget)
        self.line_copy.setGeometry(QtCore.QRect(560, 50, 81, 20))
        self.line_copy.setObjectName("line_copy")
        self.line_copy.setToolTip("Copies made of each string for reproduction. Must be an integer.")
        input_validator=QRegExpValidator(reg_ex,self.line_copy)
        self.line_copy.setValidator(input_validator)
        self.line_copy.editingFinished.connect(self.copy_equ)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(260, 80, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setToolTip("Start the genetic algorithm with these parameters.")
        self.pushButton.clicked.connect(self.model_start)
        self.graphWidget = PlotWidget(self.centralwidget)
        self.graphWidget.setGeometry(QtCore.QRect(19, 159, 631, 351))
        self.graphWidget.setObjectName("graphWidget")
        self.graphWidget.setTitle("<span style=\"color:white;font-size:20px\">Fitness vs Generations</span>")
        self.graphWidget.setLabel('left', 'Fitness', color='white', size=15)
        self.graphWidget.setLabel('bottom', 'Generations', color='white', size=15)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Genetic Algorithm Simulator"))
        self.lab_gen.setText(_translate("MainWindow", "Generations"))
        self.lab_pop.setText(_translate("MainWindow", "Population Size"))
        self.lab_route.setText(_translate("MainWindow", "Max Route Size"))
        self.lab_mut.setText(_translate("MainWindow", "Mutation Probability"))
        self.lab_copy.setText(_translate("MainWindow", "Copy Count"))
        self.pushButton.setText(_translate("MainWindow", "Start"))

    def gen_equ(self):
        if self.line_gen.text()=='':
            pass
        else:
            data[0]=int(self.line_gen.text())
    def pop_equ(self):
        if self.line_pop.text()=='':
            pass
        else:
            data[1]=int(self.line_pop.text())
    def mut_equ(self):
        if self.line_mut.text()=='':
            pass
        else:
            data[2]=int(self.line_mut.text())
    def route_equ(self):
        if self.line_route.text()=='':
            pass
        else:
            data[3]=int(self.line_route.text())
    def copy_equ(self):
        if self.line_copy.text()=='':
            pass
        else:
            data[4]=int(self.line_copy.text())

    def model_start(self):
        final_population,max_fit,avg_fit=GAM.model_run(data)
        pen2 = pg.mkPen(color=(0, 255, 0))
        self.graphWidget.plot([x for x in range(data[0])],avg_fit,name="Avg Fit",pen=pen2,clear=True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
