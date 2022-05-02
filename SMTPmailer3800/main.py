import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import uic
from smtplib import SMTP, SMTP_SSL
from email.message import EmailMessage

form_class = uic.loadUiType("uiSMTP.ui")[0] #UI for mailer
form_class_2 = uic.loadUiType("programUI.ui")[0] #Version updates

class InfoDialog(QDialog,form_class_2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.send_button)
        self.action_2.triggered.connect(self.prog_info)
        self.action_3.triggered.connect(qApp.quit)
        self.pushButton.clicked.connect(self.attach_file)
    
    def attach_file(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label_9.setText(fname[0])

    def prog_info(self):
        dlg = InfoDialog()
        dlg.exec_()
    
    def send_button(self):
        self.pushButton_2.setEnabled(False)
        data = self.organize_data()
        try:
            self.send_mail(data)
            self.statusbar.showMessage(f"Success, {self.lineEdit_7.text()}")
        except Exception as e:
            print(e)
            self.statusbar.showMessage(str(e))
        finally:
            self.pushButton_2.setEnabled(True)

        return
    
    def organize_data(self):
        data = {
            'host': self.lineEdit.text(),
            'port': int(self.lineEdit_2.text()),
            'ssl': self.checkBox.isChecked(),
            'id': self.lineEdit_3.text(),
            'pw': self.lineEdit_4.text(),
            'return_path': self.lineEdit_5.text() if self.checkBox_2.isChecked() else self.lineEdit_6.text(),
            'from': self.lineEdit_6.text(),
            'to': self.lineEdit_7.text(),
            'subject': self.lineEdit_8.text(),
            'content': self.textEdit.toPlainText(),
            'attach': self.label_9.text()
        }

        return data
    
    def send_mail(self, mydict):

        msg = EmailMessage()
        msg['Subject'] = mydict['subject']
        msg['From'] = mydict['from']
        msg['To'] = mydict['to']
        msg.set_content(mydict['content'])
        
        if self.label_9.text() != 'Attachment Here':
            with open(mydict['attach'], 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(f.name)

            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        if mydict['ssl']:
            print('ssl on')
            server = SMTP_SSL(mydict['host'], mydict['port'])  # Port -> int
        else:
            print('ssl off')
            server = SMTP(mydict['host'], mydict['port'])
        
        server.login(mydict['id'], mydict['pw'])  # Strings
        server.sendmail(mydict['return_path'], mydict['to'], msg.as_string())
        server.quit()
    
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()