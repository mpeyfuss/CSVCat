#!/usr/bin/python

'''
Creation of CSVCat application/GUI that concatenates multiple csv files.
'''

# import packages
import sys
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# define application class
class CSVCat(QMainWindow):
    def __init__(self):
        # init
        super().__init__()
        self.initUI()

        # class variables
        self.filenames = []
        self.path = ""

    def initUI(self):
        # window creation
        self.resize(600, 400)
        self.center()
        self.setWindowTitle("CSVCat")
        self.setWindowIcon(QIcon("CSVCat_Icon.png"))

        # create display for file path
        path = QLabel("File Path")
        self.pathDisp = QLineEdit()
        self.pathDisp.setEnabled(False)

        # create list box for file names
        files = QLabel("Selected Files")
        self.fileDisp = QListWidget()
        self.fileDisp.setEnabled(False)

        # create edit box for output file name
        outFile = QLabel("Output File Name")
        self.outFileDisp = QLineEdit()

        # create number entry for header line begin
        headerStart = QLabel("Header Start Row")
        self.headerStartDisp = QSpinBox()
        self.headerStartDisp.setMinimum(1)
        self.headerStartDisp.setSingleStep(1)
        self.headerStartDisp.valueChanged.connect(self.headerStartChange)

        # create number entry for header line end
        headerEnd = QLabel("Header End Row")
        self.headerEndDisp = QSpinBox()
        self.headerEndDisp.setMinimum(1)
        self.headerEndDisp.setSingleStep(1)
        self.headerEndDisp.valueChanged.connect(self.headerEndChange)

        # open files action
        self.openAct = QAction(QIcon("OpenFiles.png"), "Open Files", self)
        self.openAct.triggered.connect(self.openFiles)

        # run program action
        self.concatAct = QAction(QIcon("ConCat.png"), "Merge CSV Files", self)
        self.concatAct.triggered.connect(self.concatFiles)

        # add toolbar and actions
        self.toolbar =self.addToolBar("CSVCat")
        self.toolbar.addAction(self.openAct)
        self.toolbar.addAction(self.concatAct)

        # add grid and widgets to the grid
        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)

        grid.addWidget(path, 0, 0, 1, 5, Qt.AlignHCenter | Qt.AlignBottom)
        grid.addWidget(self.pathDisp, 1, 0, 1, 5, Qt.AlignTop)

        grid.addWidget(files, 0, 5, 1, 5, Qt.AlignHCenter | Qt.AlignBottom)
        grid.addWidget(self.fileDisp, 1, 5, 7, 5)

        grid.addWidget(headerStart, 2, 0, 1, 5, Qt.AlignHCenter | Qt.AlignBottom)
        grid.addWidget(self.headerStartDisp, 3, 0, 1, 5, Qt.AlignHCenter)

        grid.addWidget(headerEnd, 4, 0, 1, 5, Qt.AlignHCenter | Qt.AlignBottom)
        grid.addWidget(self.headerEndDisp, 5, 0, 1, 5, Qt.AlignHCenter)

        grid.addWidget(outFile, 6, 0, 1, 5, Qt.AlignHCenter | Qt.AlignBottom)
        grid.addWidget(self.outFileDisp, 7, 0, 1, 5)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(grid)

        # show UI
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFiles(self):
        # get file names
        self.filenames, ok = QFileDialog.getOpenFileNames(caption="Select CSV files to concatenate",filter="*.csv")

        # proceed only if wasn't canceled
        if ok:
            # get path end
            p_end = self.filenames[0].rfind("/")

            # display path
            self.pathDisp.setText(self.filenames[0][0:p_end+1])

            # add each filename to the list widget
            for str in self.filenames:
                self.fileDisp.addItem(str[p_end+1:])

    def concatFiles(self):

        try:
            # if there isn't a output file name, ask the user for it
            if len(self.outFileDisp.text()) == 0:
                qid = QWidget()
                text, ok = QInputDialog.getText(qid, 'Output File Name', 'Enter Output File Name:')
                if not ok or len(text) == 0:
                    text = 'Results'

            else:
                text = self.outFileDisp.text()

            # loop through csv file and concatenate
            result = pd.DataFrame()
            for file in self.filenames:
                data = pd.read_csv(file, header=[self.headerStartDisp.value() - 1, self.headerEndDisp.value() - 1])
                result = pd.concat([result, data])

            # write output file
            result.to_csv(self.pathDisp.text() + text + ".csv", index=False)

            # show process completed message
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Process Completed!")
            msg.setWindowTitle("Yay!")
            msg.exec()

        except Exception as e:
            logf = open("error.log", "w")
            logf.write(str(e))
            logf.close()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Looks like something went wrong...")
            msg.setWindowTitle("Uh Oh")
            msg.exec()

    def headerStartChange(self):
        if self.headerEndDisp.value() < self.headerStartDisp.value():
            self.headerEndDisp.setValue(self.headerStartDisp.value())

    def headerEndChange(self):
        if self.headerStartDisp.value() > self.headerEndDisp.value():
            self.headerStartDisp.setValue(self.headerEndDisp.value())


if __name__ == '__main__':
    # create application container
    app = QApplication(sys.argv)

    # instantiate GUI
    gui = CSVCat()

    # run application
    sys.exit(app.exec())