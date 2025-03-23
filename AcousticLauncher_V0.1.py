import sys
import os
# import subprocess
import win32gui, win32con, win32api
import configparser as cr
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout, QStackedLayout, QSplitter, \
    QWidget, QPushButton, QLabel, QDesktopWidget, QSizePolicy, QLineEdit, QTextEdit, QTextBrowser, QMessageBox
import 

class MyWindown(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.resize(800, 300)
        self.setWindowTitle("AcousticLauncher")

        # Layout setting:
        main_layout = QVBoxLayout()
        input_layout = QHBoxLayout()
        message_layout1 = QHBoxLayout()
        message_layout2 = QHBoxLayout()
        message_layout3 = QHBoxLayout()

        # recipe input area:
        label = QLabel("料号:")
        label.setStyleSheet('''font-size: 24px;color:black''')

        self.input_box = QLineEdit()
        self.input_box.setStyleSheet('''font-size: 20px;color:black''')
        self.input_box.setFixedSize(300, 30)
        confirm_button = QPushButton("确认")
        confirm_button.setStyleSheet('''font-size: 20px;color:black''')

        # recipe ini file parsing;
        self.software_path, self.SEN5XYCCFan_recipes, self.SEN5XDeltaFan_recipes, self.SEN4XFan_recipes = self.parse_ini()

        # recipe info display:
        SEN5XYCCFan_label = QLabel("SEN5X,YCC:")
        SEN5XYCCFan_label.setStyleSheet('''font-size: 14px;color:black''')
        SEN5XYCCFan_message_label = QLabel()
        SEN5XYCCFan_message_label.setText(str(self.SEN5XYCCFan_recipes))
        SEN5XYCCFan_message_label.setStyleSheet('''font-size: 14px;color:black''')

        SEN5XDeltaFan_label = QLabel("SEN5X,Delta:")
        SEN5XDeltaFan_label.setStyleSheet('''font-size: 14px;color:black''')
        SEN5XDeltaFan_message_label = QLabel()
        SEN5XDeltaFan_message_label.setText(str(self.SEN5XDeltaFan_recipes))
        SEN5XDeltaFan_message_label.setStyleSheet('''font-size: 14px;color:black''')

        SEN4XFan_label = QLabel("SEN4X:")
        SEN4XFan_label.setStyleSheet('''font-size: 14px;color:black''')
        SEN4XFan_message_label = QLabel()
        SEN4XFan_message_label.setText(str(self.SEN4XFan_recipes))
        SEN4XFan_message_label.setStyleSheet('''font-size: 14px;color:black''')

        # Input layout:
        input_layout.setContentsMargins(60,10,5,5)
        input_layout.addWidget(label)
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(confirm_button)
        input_layout.addStretch()

        # YCC fan info layout:
        # message_layout1.addStretch(1)
        message_layout1.setContentsMargins(60,5,5,5)
        message_layout1.addWidget(SEN5XYCCFan_label)
        message_layout1.addWidget(SEN5XYCCFan_message_label)
        message_layout1.addStretch()

        # Delta Fan info layout:
        message_layout2.setContentsMargins(60,5,5,5)
        message_layout2.addWidget(SEN5XDeltaFan_label)
        message_layout2.addWidget(SEN5XDeltaFan_message_label)
        message_layout2.addStretch()

        # SEN4X Fan info layout:
        message_layout3.setContentsMargins(60,5,5,5)
        message_layout3.addWidget(SEN4XFan_label)
        message_layout3.addWidget(SEN4XFan_message_label)
        message_layout3.addStretch()

        # Put sub layout to main layout:
        main_layout.addStretch(1)
        main_layout.addLayout(input_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(message_layout1)
        main_layout.addLayout(message_layout2)
        main_layout.addLayout(message_layout3)
        main_layout.addStretch(6)

        # self.input_box.editingFinished.connect(self.open_sw)   #slot func will be triggered twice
        self.input_box.returnPressed.connect(self.open_sw)
        confirm_button.clicked.connect(self.open_sw)
        self.setLayout(main_layout)

    def open_sw(self):
        inputtext = self.input_box.text()
        if inputtext in self.SEN5XYCCFan_recipes:
            ProductName = self.config.get("SEN5XYCCFan",inputtext)
            open_sw_cmd = self.software_path + " --productIdentifier {} --ignoreSoftwareCall".format(ProductName)
            self.close()
            os.system(open_sw_cmd)
            print("SW OPEN")
            print(self.software_path)

        elif inputtext in self.SEN5XDeltaFan_recipes:
            ProductName = self.config.get("SEN5XYCCFan",inputtext)
            open_sw_cmd = self.software_path + " --productIdentifier {} --ignoreSoftwareCall".format(ProductName)
            self.close()
            os.system(open_sw_cmd)

        elif inputtext in self.SEN4XFan_recipes:
            ProductName = self.config.get("SEN5XYCCFan",inputtext)
            open_sw_cmd = self.software_path + " --productIdentifier {} --ignoreSoftwareCall".format(ProductName)
            self.close()
            os.system(open_sw_cmd)

        else:
            win32api.MessageBox(0, "输入的料号不在配置清单里...", "提醒", win32con.MB_OK)


    def parse_ini(self):
        self.config = cr.ConfigParser()
        inifile = r"AcousticLauncher.ini"
        self.config.read(inifile)
        software_path = self.config.get("Particle.AcousticInspection.Path","Path")
        SEN5XYCCFan_recipes = self.config.options('SEN5XYCCFan')
        SEN5XDeltaFan_recipes = self.config.options('SEN5XDeltaFan')
        SEN4XFan_recipes = self.config.options('SEN4XFan')

        return software_path, SEN5XYCCFan_recipes,SEN5XDeltaFan_recipes, SEN4XFan_recipes

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindown()
    w.show()
    app.exec()