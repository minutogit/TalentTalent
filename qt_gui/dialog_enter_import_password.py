# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_enter_import_password.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_DialogEnterImportPassword(object):
    def setupUi(self, DialogEnterImportPassword):
        if not DialogEnterImportPassword.objectName():
            DialogEnterImportPassword.setObjectName(u"DialogEnterImportPassword")
        DialogEnterImportPassword.resize(233, 102)
        DialogEnterImportPassword.setLayoutDirection(Qt.RightToLeft)
        self.lineEdit_entered_password = QLineEdit(DialogEnterImportPassword)
        self.lineEdit_entered_password.setObjectName(u"lineEdit_entered_password")
        self.lineEdit_entered_password.setGeometry(QRect(30, 40, 181, 23))
        self.lineEdit_entered_password.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_entered_password.setEchoMode(QLineEdit.Normal)
        self.label = QLabel(DialogEnterImportPassword)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 10, 181, 20))
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setLineWidth(-1)
        self.label.setAlignment(Qt.AlignCenter)
        self.pushButton_OK = QPushButton(DialogEnterImportPassword)
        self.pushButton_OK.setObjectName(u"pushButton_OK")
        self.pushButton_OK.setGeometry(QRect(80, 70, 81, 23))
        self.pushButton_OK.setLayoutDirection(Qt.LeftToRight)

        self.retranslateUi(DialogEnterImportPassword)

        QMetaObject.connectSlotsByName(DialogEnterImportPassword)
    # setupUi

    def retranslateUi(self, DialogEnterImportPassword):
        DialogEnterImportPassword.setWindowTitle(QCoreApplication.translate("DialogEnterImportPassword", u"Passwort eingeben", None))
        self.label.setText(QCoreApplication.translate("DialogEnterImportPassword", u"Import Passwort eingeben:", None))
        self.pushButton_OK.setText(QCoreApplication.translate("DialogEnterImportPassword", u"OK", None))
    # retranslateUi

