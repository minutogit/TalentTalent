# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_restore_profile.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
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
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_DialogRestoreProfile(object):
    def setupUi(self, DialogRestoreProfile):
        if not DialogRestoreProfile.objectName():
            DialogRestoreProfile.setObjectName(u"DialogRestoreProfile")
        DialogRestoreProfile.resize(363, 217)
        self.label_2 = QLabel(DialogRestoreProfile)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 70, 381, 16))
        self.textEdit_profile_seed_words = QTextEdit(DialogRestoreProfile)
        self.textEdit_profile_seed_words.setObjectName(u"textEdit_profile_seed_words")
        self.textEdit_profile_seed_words.setGeometry(QRect(10, 90, 331, 61))
        self.btn_restore_profile = QPushButton(DialogRestoreProfile)
        self.btn_restore_profile.setObjectName(u"btn_restore_profile")
        self.btn_restore_profile.setGeometry(QRect(70, 190, 201, 23))
        self.lineEdit_profile_name = QLineEdit(DialogRestoreProfile)
        self.lineEdit_profile_name.setObjectName(u"lineEdit_profile_name")
        self.lineEdit_profile_name.setGeometry(QRect(10, 40, 331, 23))
        self.label_3 = QLabel(DialogRestoreProfile)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 20, 331, 16))
        self.label_status = QLabel(DialogRestoreProfile)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setGeometry(QRect(10, 160, 331, 21))
        self.label_status.setLineWidth(1)
        self.label_status.setWordWrap(True)

        self.retranslateUi(DialogRestoreProfile)

        QMetaObject.connectSlotsByName(DialogRestoreProfile)
    # setupUi

    def retranslateUi(self, DialogRestoreProfile):
        DialogRestoreProfile.setWindowTitle(QCoreApplication.translate("DialogRestoreProfile", u"Profil wiederherstellen", None))
        self.label_2.setText(QCoreApplication.translate("DialogRestoreProfile", u"Schl\u00fcsselw\u00f6rter des Profils eingeben:", None))
        self.btn_restore_profile.setText(QCoreApplication.translate("DialogRestoreProfile", u"Profil wiederhererstellen", None))
        self.label_3.setText(QCoreApplication.translate("DialogRestoreProfile", u"Profilname (beliebig w\u00e4hlbar)", None))
        self.label_status.setText(QCoreApplication.translate("DialogRestoreProfile", u"Info", None))
    # retranslateUi

