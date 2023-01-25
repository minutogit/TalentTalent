# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_profile_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_DialogProfileSettings(object):
    def setupUi(self, DialogProfileSettings):
        if not DialogProfileSettings.objectName():
            DialogProfileSettings.setObjectName(u"DialogProfileSettings")
        DialogProfileSettings.resize(620, 431)
        self.label_3 = QLabel(DialogProfileSettings)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 335, 131, 16))
        self.label_5 = QLabel(DialogProfileSettings)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(312, 160, 30, 16))
        self.country_lineEdit = QLineEdit(DialogProfileSettings)
        self.country_lineEdit.setObjectName(u"country_lineEdit")
        self.country_lineEdit.setGeometry(QRect(396, 160, 201, 23))
        self.label_6 = QLabel(DialogProfileSettings)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(312, 102, 23, 16))
        self.zip_code_lineEdit = QLineEdit(DialogProfileSettings)
        self.zip_code_lineEdit.setObjectName(u"zip_code_lineEdit")
        self.zip_code_lineEdit.setGeometry(QRect(396, 102, 201, 23))
        self.zip_code_lineEdit.setInputMethodHints(Qt.ImhDigitsOnly)
        self.zip_code_lineEdit.setClearButtonEnabled(False)
        self.label_7 = QLabel(DialogProfileSettings)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(312, 131, 20, 16))
        self.city_lineEdit = QLineEdit(DialogProfileSettings)
        self.city_lineEdit.setObjectName(u"city_lineEdit")
        self.city_lineEdit.setGeometry(QRect(396, 131, 201, 23))
        self.label_8 = QLabel(DialogProfileSettings)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(312, 73, 40, 16))
        self.street_lineEdit = QLineEdit(DialogProfileSettings)
        self.street_lineEdit.setObjectName(u"street_lineEdit")
        self.street_lineEdit.setGeometry(QRect(396, 73, 201, 23))
        self.interests_hobbies_lineEdit = QLineEdit(DialogProfileSettings)
        self.interests_hobbies_lineEdit.setObjectName(u"interests_hobbies_lineEdit")
        self.interests_hobbies_lineEdit.setGeometry(QRect(20, 355, 581, 23))
        self.label_9 = QLabel(DialogProfileSettings)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(310, 193, 81, 16))
        self.coordinates_lineEdit = QLineEdit(DialogProfileSettings)
        self.coordinates_lineEdit.setObjectName(u"coordinates_lineEdit")
        self.coordinates_lineEdit.setGeometry(QRect(410, 193, 101, 21))
        self.label_16 = QLabel(DialogProfileSettings)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(28, 196, 81, 16))
        self.radius_of_activity_lineEdit = QLineEdit(DialogProfileSettings)
        self.radius_of_activity_lineEdit.setObjectName(u"radius_of_activity_lineEdit")
        self.radius_of_activity_lineEdit.setGeometry(QRect(130, 193, 141, 23))
        self.layoutWidget = QWidget(DialogProfileSettings)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 73, 251, 96))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.name_lineEdit = QLineEdit(self.layoutWidget)
        self.name_lineEdit.setObjectName(u"name_lineEdit")

        self.verticalLayout.addWidget(self.name_lineEdit)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.family_name_lineEdit = QLineEdit(self.layoutWidget)
        self.family_name_lineEdit.setObjectName(u"family_name_lineEdit")

        self.verticalLayout.addWidget(self.family_name_lineEdit)

        self.layoutWidget1 = QWidget(DialogProfileSettings)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(329, 233, 271, 96))
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_10 = QLabel(self.layoutWidget1)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_3.addWidget(self.label_10)

        self.website_lineEdit = QLineEdit(self.layoutWidget1)
        self.website_lineEdit.setObjectName(u"website_lineEdit")

        self.verticalLayout_3.addWidget(self.website_lineEdit)

        self.label_13 = QLabel(self.layoutWidget1)
        self.label_13.setObjectName(u"label_13")

        self.verticalLayout_3.addWidget(self.label_13)

        self.email_lineEdit = QLineEdit(self.layoutWidget1)
        self.email_lineEdit.setObjectName(u"email_lineEdit")

        self.verticalLayout_3.addWidget(self.email_lineEdit)

        self.layoutWidget2 = QWidget(DialogProfileSettings)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(23, 235, 271, 96))
        self.formLayout = QFormLayout(self.layoutWidget2)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.layoutWidget2)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_12)

        self.label_11 = QLabel(self.layoutWidget2)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_11)

        self.company_profession_lineEdit = QLineEdit(self.layoutWidget2)
        self.company_profession_lineEdit.setObjectName(u"company_profession_lineEdit")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.company_profession_lineEdit)

        self.phone_lineEdit = QLineEdit(self.layoutWidget2)
        self.phone_lineEdit.setObjectName(u"phone_lineEdit")

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.phone_lineEdit)

        self.determine_coordinates_pushButton = QPushButton(DialogProfileSettings)
        self.determine_coordinates_pushButton.setObjectName(u"determine_coordinates_pushButton")
        self.determine_coordinates_pushButton.setGeometry(QRect(520, 193, 80, 23))
        self.status_label = QLabel(DialogProfileSettings)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setGeometry(QRect(20, 413, 461, 20))
        self.label_2 = QLabel(DialogProfileSettings)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(510, 413, 101, 21))
        self.layoutWidget3 = QWidget(DialogProfileSettings)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(190, 383, 271, 25))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.save_pushButton = QPushButton(self.layoutWidget3)
        self.save_pushButton.setObjectName(u"save_pushButton")

        self.horizontalLayout.addWidget(self.save_pushButton)

        self.close_pushButton = QPushButton(self.layoutWidget3)
        self.close_pushButton.setObjectName(u"close_pushButton")

        self.horizontalLayout.addWidget(self.close_pushButton)

        self.profile_name_lineEdit = QLineEdit(DialogProfileSettings)
        self.profile_name_lineEdit.setObjectName(u"profile_name_lineEdit")
        self.profile_name_lineEdit.setGeometry(QRect(20, 30, 251, 23))
        self.line = QFrame(DialogProfileSettings)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 50, 581, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.label_14 = QLabel(DialogProfileSettings)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(20, 10, 101, 16))
        QWidget.setTabOrder(self.name_lineEdit, self.family_name_lineEdit)
        QWidget.setTabOrder(self.family_name_lineEdit, self.street_lineEdit)
        QWidget.setTabOrder(self.street_lineEdit, self.zip_code_lineEdit)
        QWidget.setTabOrder(self.zip_code_lineEdit, self.city_lineEdit)
        QWidget.setTabOrder(self.city_lineEdit, self.country_lineEdit)
        QWidget.setTabOrder(self.country_lineEdit, self.coordinates_lineEdit)
        QWidget.setTabOrder(self.coordinates_lineEdit, self.radius_of_activity_lineEdit)
        QWidget.setTabOrder(self.radius_of_activity_lineEdit, self.company_profession_lineEdit)
        QWidget.setTabOrder(self.company_profession_lineEdit, self.phone_lineEdit)
        QWidget.setTabOrder(self.phone_lineEdit, self.website_lineEdit)
        QWidget.setTabOrder(self.website_lineEdit, self.email_lineEdit)
        QWidget.setTabOrder(self.email_lineEdit, self.interests_hobbies_lineEdit)
        QWidget.setTabOrder(self.interests_hobbies_lineEdit, self.save_pushButton)
        QWidget.setTabOrder(self.save_pushButton, self.close_pushButton)

        self.retranslateUi(DialogProfileSettings)

        QMetaObject.connectSlotsByName(DialogProfileSettings)
    # setupUi

    def retranslateUi(self, DialogProfileSettings):
        DialogProfileSettings.setWindowTitle(QCoreApplication.translate("DialogProfileSettings", u"Profileinstellungen", None))
        self.label_3.setText(QCoreApplication.translate("DialogProfileSettings", u"Interessen / Hobbys", None))
        self.label_5.setText(QCoreApplication.translate("DialogProfileSettings", u"Land", None))
        self.country_lineEdit.setText("")
        self.label_6.setText(QCoreApplication.translate("DialogProfileSettings", u"PLZ", None))
        self.zip_code_lineEdit.setText("")
        self.label_7.setText(QCoreApplication.translate("DialogProfileSettings", u"Ort", None))
        self.city_lineEdit.setText("")
        self.label_8.setText(QCoreApplication.translate("DialogProfileSettings", u"Stra\u00dfe", None))
        self.street_lineEdit.setText("")
        self.label_9.setText(QCoreApplication.translate("DialogProfileSettings", u"Koordinaten*", None))
        self.coordinates_lineEdit.setText("")
        self.label_16.setText(QCoreApplication.translate("DialogProfileSettings", u"Aktionsradius", None))
        self.radius_of_activity_lineEdit.setText("")
        self.label.setText(QCoreApplication.translate("DialogProfileSettings", u"Rufname", None))
        self.label_4.setText(QCoreApplication.translate("DialogProfileSettings", u"Familienname", None))
        self.label_10.setText(QCoreApplication.translate("DialogProfileSettings", u"Internetseite", None))
        self.website_lineEdit.setText("")
        self.label_13.setText(QCoreApplication.translate("DialogProfileSettings", u"E-Mail*", None))
        self.email_lineEdit.setText("")
        self.label_12.setText(QCoreApplication.translate("DialogProfileSettings", u"Unternehmen / Beruf", None))
        self.label_11.setText(QCoreApplication.translate("DialogProfileSettings", u"Telefon / Handy", None))
        self.company_profession_lineEdit.setText("")
        self.phone_lineEdit.setText("")
        self.determine_coordinates_pushButton.setText(QCoreApplication.translate("DialogProfileSettings", u"Ermitteln", None))
        self.status_label.setText(QCoreApplication.translate("DialogProfileSettings", u"status_label", None))
        self.label_2.setText(QCoreApplication.translate("DialogProfileSettings", u"*Wichtig", None))
        self.save_pushButton.setText(QCoreApplication.translate("DialogProfileSettings", u"Speichern", None))
        self.close_pushButton.setText(QCoreApplication.translate("DialogProfileSettings", u"Schlie\u00dfen", None))
        self.label_14.setText(QCoreApplication.translate("DialogProfileSettings", u"Profil Name:", None))
    # retranslateUi

