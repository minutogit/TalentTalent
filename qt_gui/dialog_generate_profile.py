# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_generate_profile.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QTextBrowser,
    QTextEdit, QWidget)

class Ui_DialogGenerateProfile(object):
    def setupUi(self, DialogGenerateProfile):
        if not DialogGenerateProfile.objectName():
            DialogGenerateProfile.setObjectName(u"DialogGenerateProfile")
        DialogGenerateProfile.resize(351, 367)
        self.btn_new_seed_words = QPushButton(DialogGenerateProfile)
        self.btn_new_seed_words.setObjectName(u"btn_new_seed_words")
        self.btn_new_seed_words.setGeometry(QRect(100, 140, 171, 23))
        self.textBrowser_new_seed = QTextBrowser(DialogGenerateProfile)
        self.textBrowser_new_seed.setObjectName(u"textBrowser_new_seed")
        self.textBrowser_new_seed.setGeometry(QRect(10, 80, 331, 51))
        self.label = QLabel(DialogGenerateProfile)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 60, 321, 16))
        self.label_2 = QLabel(DialogGenerateProfile)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 170, 331, 16))
        self.textEdit_new_seed_confirmed = QTextEdit(DialogGenerateProfile)
        self.textEdit_new_seed_confirmed.setObjectName(u"textEdit_new_seed_confirmed")
        self.textEdit_new_seed_confirmed.setGeometry(QRect(10, 190, 331, 51))
        self.btn_create_profile = QPushButton(DialogGenerateProfile)
        self.btn_create_profile.setObjectName(u"btn_create_profile")
        self.btn_create_profile.setGeometry(QRect(90, 340, 161, 23))
        self.lineEdit_profile_name = QLineEdit(DialogGenerateProfile)
        self.lineEdit_profile_name.setObjectName(u"lineEdit_profile_name")
        self.lineEdit_profile_name.setGeometry(QRect(10, 30, 331, 23))
        self.label_3 = QLabel(DialogGenerateProfile)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 10, 331, 16))
        self.label_info = QLabel(DialogGenerateProfile)
        self.label_info.setObjectName(u"label_info")
        self.label_info.setGeometry(QRect(10, 250, 331, 81))
        self.label_info.setAutoFillBackground(False)
        self.label_info.setFrameShape(QFrame.Box)
        self.label_info.setFrameShadow(QFrame.Sunken)
        self.label_info.setLineWidth(2)
        self.label_info.setWordWrap(True)

        self.retranslateUi(DialogGenerateProfile)

        QMetaObject.connectSlotsByName(DialogGenerateProfile)
    # setupUi

    def retranslateUi(self, DialogGenerateProfile):
        DialogGenerateProfile.setWindowTitle(QCoreApplication.translate("DialogGenerateProfile", u"Profil generieren", None))
        self.btn_new_seed_words.setText(QCoreApplication.translate("DialogGenerateProfile", u"Neue W\u00f6rter generieren", None))
        self.label.setText(QCoreApplication.translate("DialogGenerateProfile", u"Schl\u00fcsselw\u00f6rter", None))
        self.label_2.setText(QCoreApplication.translate("DialogGenerateProfile", u"Schl\u00fcsselw\u00f6rter zur Best\u00e4tigung nochmal eingeben", None))
        self.btn_create_profile.setText(QCoreApplication.translate("DialogGenerateProfile", u"Profil erstellen", None))
        self.label_3.setText(QCoreApplication.translate("DialogGenerateProfile", u"Profilname (beliebig w\u00e4hlbar)", None))
        self.label_info.setText(QCoreApplication.translate("DialogGenerateProfile", u"Diese W\u00f6rter erzeugen eine digitale Identit\u00e4t. Aufschreiben und geheim halten, damit ihre Eintr\u00e4ge f\u00e4lschungssicher sind. Die Worte dienen auch zur Profil- und Passwortwiederherstellung.", None))
    # retranslateUi

