# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_businesscard.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFormLayout,
    QFrame, QGraphicsView, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpinBox,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_DialogBuisinessCard(object):
    def setupUi(self, DialogBuisinessCard):
        if not DialogBuisinessCard.objectName():
            DialogBuisinessCard.setObjectName(u"DialogBuisinessCard")
        DialogBuisinessCard.resize(674, 829)
        self.HOPS_name_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_name_spinBox.setObjectName(u"HOPS_name_spinBox")
        self.HOPS_name_spinBox.setGeometry(QRect(290, 154, 35, 24))
        self.HOPS_name_spinBox.setMinimum(0)
        self.HOPS_name_spinBox.setMaximum(4)
        self.skills_offers_textEdit = QTextEdit(DialogBuisinessCard)
        self.skills_offers_textEdit.setObjectName(u"skills_offers_textEdit")
        self.skills_offers_textEdit.setGeometry(QRect(30, 512, 581, 111))
        self.image_graphicsView = QGraphicsView(DialogBuisinessCard)
        self.image_graphicsView.setObjectName(u"image_graphicsView")
        self.image_graphicsView.setGeometry(QRect(30, 100, 100, 131))
        self.label_3 = QLabel(DialogBuisinessCard)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 442, 131, 16))
        self.label_5 = QLabel(DialogBuisinessCard)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(342, 211, 30, 16))
        self.country_lineEdit = QLineEdit(DialogBuisinessCard)
        self.country_lineEdit.setObjectName(u"country_lineEdit")
        self.country_lineEdit.setGeometry(QRect(416, 211, 191, 23))
        self.label_6 = QLabel(DialogBuisinessCard)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(342, 153, 23, 16))
        self.zip_code_lineEdit = QLineEdit(DialogBuisinessCard)
        self.zip_code_lineEdit.setObjectName(u"zip_code_lineEdit")
        self.zip_code_lineEdit.setGeometry(QRect(416, 153, 191, 23))
        self.zip_code_lineEdit.setInputMethodHints(Qt.ImhDigitsOnly)
        self.zip_code_lineEdit.setClearButtonEnabled(False)
        self.label_7 = QLabel(DialogBuisinessCard)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(342, 182, 20, 16))
        self.city_lineEdit = QLineEdit(DialogBuisinessCard)
        self.city_lineEdit.setObjectName(u"city_lineEdit")
        self.city_lineEdit.setGeometry(QRect(416, 182, 191, 23))
        self.label_8 = QLabel(DialogBuisinessCard)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(342, 124, 40, 16))
        self.street_lineEdit = QLineEdit(DialogBuisinessCard)
        self.street_lineEdit.setObjectName(u"street_lineEdit")
        self.street_lineEdit.setGeometry(QRect(416, 124, 191, 23))
        self.HOPS_family_name_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_family_name_spinBox.setObjectName(u"HOPS_family_name_spinBox")
        self.HOPS_family_name_spinBox.setGeometry(QRect(290, 204, 35, 24))
        self.HOPS_family_name_spinBox.setMinimum(0)
        self.HOPS_family_name_spinBox.setMaximum(4)
        self.HOPS_street_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_street_spinBox.setObjectName(u"HOPS_street_spinBox")
        self.HOPS_street_spinBox.setGeometry(QRect(620, 124, 35, 24))
        self.HOPS_street_spinBox.setMinimum(0)
        self.HOPS_street_spinBox.setMaximum(4)
        self.HOPS_city_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_city_spinBox.setObjectName(u"HOPS_city_spinBox")
        self.HOPS_city_spinBox.setGeometry(QRect(620, 184, 35, 24))
        self.HOPS_city_spinBox.setMinimum(0)
        self.HOPS_city_spinBox.setMaximum(4)
        self.HOPS_country_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_country_spinBox.setObjectName(u"HOPS_country_spinBox")
        self.HOPS_country_spinBox.setGeometry(QRect(620, 214, 35, 24))
        self.HOPS_country_spinBox.setMinimum(0)
        self.HOPS_country_spinBox.setMaximum(4)
        self.HOPS_zip_code_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_zip_code_spinBox.setObjectName(u"HOPS_zip_code_spinBox")
        self.HOPS_zip_code_spinBox.setGeometry(QRect(620, 154, 35, 24))
        self.HOPS_zip_code_spinBox.setMinimum(0)
        self.HOPS_zip_code_spinBox.setMaximum(4)
        self.label_14 = QLabel(DialogBuisinessCard)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(30, 492, 211, 16))
        self.requests_textEdit = QTextEdit(DialogBuisinessCard)
        self.requests_textEdit.setObjectName(u"requests_textEdit")
        self.requests_textEdit.setGeometry(QRect(30, 650, 581, 61))
        self.label_15 = QLabel(DialogBuisinessCard)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(30, 630, 211, 20))
        self.label_titel = QLabel(DialogBuisinessCard)
        self.label_titel.setObjectName(u"label_titel")
        self.label_titel.setGeometry(QRect(30, 10, 131, 51))
        font = QFont()
        font.setPointSize(12)
        self.label_titel.setFont(font)
        self.label_titel.setAlignment(Qt.AlignCenter)
        self.interests_hobbies_lineEdit = QLineEdit(DialogBuisinessCard)
        self.interests_hobbies_lineEdit.setObjectName(u"interests_hobbies_lineEdit")
        self.interests_hobbies_lineEdit.setGeometry(QRect(30, 462, 581, 23))
        self.line = QFrame(DialogBuisinessCard)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(30, 80, 621, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.HOPS_image_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_image_spinBox.setObjectName(u"HOPS_image_spinBox")
        self.HOPS_image_spinBox.setGeometry(QRect(140, 100, 35, 24))
        self.HOPS_image_spinBox.setMinimum(0)
        self.HOPS_image_spinBox.setMaximum(4)
        self.HOPS_phone_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_phone_spinBox.setObjectName(u"HOPS_phone_spinBox")
        self.HOPS_phone_spinBox.setGeometry(QRect(310, 350, 35, 24))
        self.HOPS_phone_spinBox.setMinimum(0)
        self.HOPS_phone_spinBox.setMaximum(4)
        self.HOPS_company_profession_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_company_profession_spinBox.setObjectName(u"HOPS_company_profession_spinBox")
        self.HOPS_company_profession_spinBox.setGeometry(QRect(310, 300, 35, 24))
        self.HOPS_company_profession_spinBox.setMinimum(0)
        self.HOPS_company_profession_spinBox.setMaximum(4)
        self.HOPS_email_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_email_spinBox.setObjectName(u"HOPS_email_spinBox")
        self.HOPS_email_spinBox.setGeometry(QRect(620, 350, 35, 24))
        self.HOPS_email_spinBox.setMinimum(0)
        self.HOPS_email_spinBox.setMaximum(4)
        self.HOPS_interests_hobbies_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_interests_hobbies_spinBox.setObjectName(u"HOPS_interests_hobbies_spinBox")
        self.HOPS_interests_hobbies_spinBox.setGeometry(QRect(620, 462, 35, 24))
        self.HOPS_interests_hobbies_spinBox.setMinimum(0)
        self.HOPS_interests_hobbies_spinBox.setMaximum(4)
        self.HOPS_skills_offers_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_skills_offers_spinBox.setObjectName(u"HOPS_skills_offers_spinBox")
        self.HOPS_skills_offers_spinBox.setGeometry(QRect(620, 512, 35, 24))
        self.HOPS_skills_offers_spinBox.setMinimum(0)
        self.HOPS_skills_offers_spinBox.setMaximum(4)
        self.HOPS_website_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_website_spinBox.setObjectName(u"HOPS_website_spinBox")
        self.HOPS_website_spinBox.setGeometry(QRect(620, 300, 35, 24))
        self.HOPS_website_spinBox.setMinimum(0)
        self.HOPS_website_spinBox.setMaximum(4)
        self.HOPS_requests_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_requests_spinBox.setObjectName(u"HOPS_requests_spinBox")
        self.HOPS_requests_spinBox.setGeometry(QRect(620, 650, 35, 24))
        self.HOPS_requests_spinBox.setMinimum(0)
        self.HOPS_requests_spinBox.setMaximum(4)
        self.label_9 = QLabel(DialogBuisinessCard)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(340, 244, 81, 16))
        self.coordinates_lineEdit = QLineEdit(DialogBuisinessCard)
        self.coordinates_lineEdit.setObjectName(u"coordinates_lineEdit")
        self.coordinates_lineEdit.setGeometry(QRect(420, 244, 101, 21))
        self.HOPS_coordinates_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_coordinates_spinBox.setObjectName(u"HOPS_coordinates_spinBox")
        self.HOPS_coordinates_spinBox.setGeometry(QRect(620, 244, 35, 24))
        self.HOPS_coordinates_spinBox.setMinimum(0)
        self.HOPS_coordinates_spinBox.setMaximum(4)
        self.HOPS_radius_of_activity_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_radius_of_activity_spinBox.setObjectName(u"HOPS_radius_of_activity_spinBox")
        self.HOPS_radius_of_activity_spinBox.setGeometry(QRect(290, 244, 35, 24))
        self.HOPS_radius_of_activity_spinBox.setMinimum(0)
        self.HOPS_radius_of_activity_spinBox.setMaximum(4)
        self.label_16 = QLabel(DialogBuisinessCard)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(38, 247, 81, 16))
        self.radius_of_activity_lineEdit = QLineEdit(DialogBuisinessCard)
        self.radius_of_activity_lineEdit.setObjectName(u"radius_of_activity_lineEdit")
        self.radius_of_activity_lineEdit.setGeometry(QRect(140, 244, 141, 23))
        self.save_pushButton = QPushButton(DialogBuisinessCard)
        self.save_pushButton.setObjectName(u"save_pushButton")
        self.save_pushButton.setGeometry(QRect(200, 780, 111, 23))
        self.valid_until_label = QLabel(DialogBuisinessCard)
        self.valid_until_label.setObjectName(u"valid_until_label")
        self.valid_until_label.setGeometry(QRect(220, 60, 301, 16))
        self.layoutWidget = QWidget(DialogBuisinessCard)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(140, 134, 141, 96))
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

        self.layoutWidget1 = QWidget(DialogBuisinessCard)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(390, 280, 220, 96))
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

        self.layoutWidget2 = QWidget(DialogBuisinessCard)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(33, 282, 271, 96))
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

        self.label_18 = QLabel(DialogBuisinessCard)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(30, 720, 131, 16))
        self.HOPS_tags_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_tags_spinBox.setObjectName(u"HOPS_tags_spinBox")
        self.HOPS_tags_spinBox.setGeometry(QRect(620, 740, 35, 24))
        self.HOPS_tags_spinBox.setMinimum(0)
        self.HOPS_tags_spinBox.setMaximum(4)
        self.tags_lineEdit = QLineEdit(DialogBuisinessCard)
        self.tags_lineEdit.setObjectName(u"tags_lineEdit")
        self.tags_lineEdit.setGeometry(QRect(30, 740, 581, 23))
        self.close_pushButton = QPushButton(DialogBuisinessCard)
        self.close_pushButton.setObjectName(u"close_pushButton")
        self.close_pushButton.setGeometry(QRect(330, 780, 111, 23))
        self.label_range = QLabel(DialogBuisinessCard)
        self.label_range.setObjectName(u"label_range")
        self.label_range.setGeometry(QRect(540, 10, 101, 16))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_range.setFont(font1)
        self.increase_hops_pushButton = QPushButton(DialogBuisinessCard)
        self.increase_hops_pushButton.setObjectName(u"increase_hops_pushButton")
        self.increase_hops_pushButton.setGeometry(QRect(560, 30, 21, 23))
        font2 = QFont()
        font2.setPointSize(11)
        font2.setBold(True)
        self.increase_hops_pushButton.setFont(font2)
        self.decrease_hops_pushButton = QPushButton(DialogBuisinessCard)
        self.decrease_hops_pushButton.setObjectName(u"decrease_hops_pushButton")
        self.decrease_hops_pushButton.setGeometry(QRect(590, 30, 21, 23))
        font3 = QFont()
        font3.setPointSize(15)
        self.decrease_hops_pushButton.setFont(font3)
        self.determine_coordinates_pushButton = QPushButton(DialogBuisinessCard)
        self.determine_coordinates_pushButton.setObjectName(u"determine_coordinates_pushButton")
        self.determine_coordinates_pushButton.setGeometry(QRect(530, 244, 80, 23))
        self.status_label = QLabel(DialogBuisinessCard)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setGeometry(QRect(30, 810, 581, 20))
        self.checkBox_extend_hops = QCheckBox(DialogBuisinessCard)
        self.checkBox_extend_hops.setObjectName(u"checkBox_extend_hops")
        self.checkBox_extend_hops.setGeometry(QRect(540, 60, 91, 21))
        self.adopt_validity_pushButton = QPushButton(DialogBuisinessCard)
        self.adopt_validity_pushButton.setObjectName(u"adopt_validity_pushButton")
        self.adopt_validity_pushButton.setGeometry(QRect(30, 60, 181, 23))
        self.layoutWidget3 = QWidget(DialogBuisinessCard)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(220, 20, 151, 26))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.month_valid_label = QLabel(self.layoutWidget3)
        self.month_valid_label.setObjectName(u"month_valid_label")

        self.horizontalLayout.addWidget(self.month_valid_label)

        self.month_valid_spinBox = QSpinBox(self.layoutWidget3)
        self.month_valid_spinBox.setObjectName(u"month_valid_spinBox")
        self.month_valid_spinBox.setMinimum(1)
        self.month_valid_spinBox.setMaximum(36)
        self.month_valid_spinBox.setValue(36)

        self.horizontalLayout.addWidget(self.month_valid_spinBox)

        self.HOPS_other_contact_spinBox = QSpinBox(DialogBuisinessCard)
        self.HOPS_other_contact_spinBox.setObjectName(u"HOPS_other_contact_spinBox")
        self.HOPS_other_contact_spinBox.setGeometry(QRect(620, 413, 35, 24))
        self.HOPS_other_contact_spinBox.setMinimum(0)
        self.HOPS_other_contact_spinBox.setMaximum(4)
        self.other_contact_lineEdit = QLineEdit(DialogBuisinessCard)
        self.other_contact_lineEdit.setObjectName(u"other_contact_lineEdit")
        self.other_contact_lineEdit.setGeometry(QRect(30, 413, 581, 23))
        self.label_17 = QLabel(DialogBuisinessCard)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(30, 393, 251, 16))
        self.checkBox_add_to_mailling_list = QCheckBox(DialogBuisinessCard)
        self.checkBox_add_to_mailling_list.setObjectName(u"checkBox_add_to_mailling_list")
        self.checkBox_add_to_mailling_list.setGeometry(QRect(390, 380, 221, 21))
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
        QWidget.setTabOrder(self.email_lineEdit, self.checkBox_add_to_mailling_list)
        QWidget.setTabOrder(self.checkBox_add_to_mailling_list, self.other_contact_lineEdit)
        QWidget.setTabOrder(self.other_contact_lineEdit, self.interests_hobbies_lineEdit)
        QWidget.setTabOrder(self.interests_hobbies_lineEdit, self.skills_offers_textEdit)
        QWidget.setTabOrder(self.skills_offers_textEdit, self.requests_textEdit)
        QWidget.setTabOrder(self.requests_textEdit, self.tags_lineEdit)
        QWidget.setTabOrder(self.tags_lineEdit, self.HOPS_image_spinBox)
        QWidget.setTabOrder(self.HOPS_image_spinBox, self.HOPS_name_spinBox)
        QWidget.setTabOrder(self.HOPS_name_spinBox, self.HOPS_family_name_spinBox)
        QWidget.setTabOrder(self.HOPS_family_name_spinBox, self.HOPS_street_spinBox)
        QWidget.setTabOrder(self.HOPS_street_spinBox, self.HOPS_zip_code_spinBox)
        QWidget.setTabOrder(self.HOPS_zip_code_spinBox, self.HOPS_city_spinBox)
        QWidget.setTabOrder(self.HOPS_city_spinBox, self.HOPS_country_spinBox)
        QWidget.setTabOrder(self.HOPS_country_spinBox, self.HOPS_coordinates_spinBox)
        QWidget.setTabOrder(self.HOPS_coordinates_spinBox, self.HOPS_radius_of_activity_spinBox)
        QWidget.setTabOrder(self.HOPS_radius_of_activity_spinBox, self.HOPS_company_profession_spinBox)
        QWidget.setTabOrder(self.HOPS_company_profession_spinBox, self.HOPS_phone_spinBox)
        QWidget.setTabOrder(self.HOPS_phone_spinBox, self.HOPS_website_spinBox)
        QWidget.setTabOrder(self.HOPS_website_spinBox, self.HOPS_email_spinBox)
        QWidget.setTabOrder(self.HOPS_email_spinBox, self.HOPS_interests_hobbies_spinBox)
        QWidget.setTabOrder(self.HOPS_interests_hobbies_spinBox, self.HOPS_skills_offers_spinBox)
        QWidget.setTabOrder(self.HOPS_skills_offers_spinBox, self.HOPS_requests_spinBox)
        QWidget.setTabOrder(self.HOPS_requests_spinBox, self.HOPS_tags_spinBox)
        QWidget.setTabOrder(self.HOPS_tags_spinBox, self.save_pushButton)
        QWidget.setTabOrder(self.save_pushButton, self.close_pushButton)
        QWidget.setTabOrder(self.close_pushButton, self.image_graphicsView)
        QWidget.setTabOrder(self.image_graphicsView, self.month_valid_spinBox)
        QWidget.setTabOrder(self.month_valid_spinBox, self.increase_hops_pushButton)
        QWidget.setTabOrder(self.increase_hops_pushButton, self.decrease_hops_pushButton)
        QWidget.setTabOrder(self.decrease_hops_pushButton, self.determine_coordinates_pushButton)
        QWidget.setTabOrder(self.determine_coordinates_pushButton, self.checkBox_extend_hops)
        QWidget.setTabOrder(self.checkBox_extend_hops, self.adopt_validity_pushButton)
        QWidget.setTabOrder(self.adopt_validity_pushButton, self.HOPS_other_contact_spinBox)

        self.retranslateUi(DialogBuisinessCard)

        QMetaObject.connectSlotsByName(DialogBuisinessCard)
    # setupUi

    def retranslateUi(self, DialogBuisinessCard):
        DialogBuisinessCard.setWindowTitle(QCoreApplication.translate("DialogBuisinessCard", u"Visitenkarte", None))
        self.label_3.setText(QCoreApplication.translate("DialogBuisinessCard", u"Interessen / Hobbys", None))
        self.label_5.setText(QCoreApplication.translate("DialogBuisinessCard", u"Land", None))
        self.country_lineEdit.setText("")
        self.label_6.setText(QCoreApplication.translate("DialogBuisinessCard", u"PLZ", None))
        self.zip_code_lineEdit.setText("")
        self.label_7.setText(QCoreApplication.translate("DialogBuisinessCard", u"Ort", None))
        self.city_lineEdit.setText("")
        self.label_8.setText(QCoreApplication.translate("DialogBuisinessCard", u"Stra\u00dfe", None))
        self.street_lineEdit.setText("")
        self.label_14.setText(QCoreApplication.translate("DialogBuisinessCard", u"Generelle F\u00e4higkeiten / Angebote", None))
        self.label_15.setText(QCoreApplication.translate("DialogBuisinessCard", u"Generelle Gesuche", None))
        self.label_titel.setText(QCoreApplication.translate("DialogBuisinessCard", u"Visitenkarte", None))
        self.label_9.setText(QCoreApplication.translate("DialogBuisinessCard", u"Koordinaten", None))
        self.coordinates_lineEdit.setText("")
        self.label_16.setText(QCoreApplication.translate("DialogBuisinessCard", u"Aktionsradius", None))
        self.radius_of_activity_lineEdit.setText("")
        self.save_pushButton.setText(QCoreApplication.translate("DialogBuisinessCard", u"Speichern", None))
        self.valid_until_label.setText(QCoreApplication.translate("DialogBuisinessCard", u"G\u00fcltig bis ", None))
        self.label.setText(QCoreApplication.translate("DialogBuisinessCard", u"Rufname", None))
        self.label_4.setText(QCoreApplication.translate("DialogBuisinessCard", u"Familienname", None))
        self.label_10.setText(QCoreApplication.translate("DialogBuisinessCard", u"Internetseite", None))
        self.website_lineEdit.setText("")
        self.label_13.setText(QCoreApplication.translate("DialogBuisinessCard", u"E-Mail", None))
        self.email_lineEdit.setText("")
        self.label_12.setText(QCoreApplication.translate("DialogBuisinessCard", u"Unternehmen / Beruf", None))
        self.label_11.setText(QCoreApplication.translate("DialogBuisinessCard", u"Telefon / Handy", None))
        self.company_profession_lineEdit.setText("")
        self.phone_lineEdit.setText("")
        self.label_18.setText(QCoreApplication.translate("DialogBuisinessCard", u"Stichw\u00f6rter / Tags", None))
        self.close_pushButton.setText(QCoreApplication.translate("DialogBuisinessCard", u"Schlie\u00dfen", None))
#if QT_CONFIG(tooltip)
        self.label_range.setToolTip(QCoreApplication.translate("DialogBuisinessCard", u"<html><head/><body><p>0 = Eintrag wird nur lokal gespeichert.</p><p>1 = Eintrag wird auch an Freunde geteilt (Freund ersten Grads)</p><p>2 = Eintrag wird bis an Freunde der Freunde geteilt (2. Grad)</p><p>3 = Teilen bis Freunde 3. Grads</p><p>4 = Teilen bis Freunde 4. Grads</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_range.setText(QCoreApplication.translate("DialogBuisinessCard", u"Reichweite", None))
#if QT_CONFIG(tooltip)
        self.increase_hops_pushButton.setToolTip(QCoreApplication.translate("DialogBuisinessCard", u"<html><head/><body><p>0 = Eintrag wird nur lokal gespeichert.</p><p>1 = Eintrag wird auch an Freunde geteilt (Freund ersten Grads)</p><p>2 = Eintrag wird bis an Freunde der Freunde geteilt (2. Grad)</p><p>3 = Teilen bis Freunde 3. Grads</p><p>4 = Teilen bis Freunde 4. Grads</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.increase_hops_pushButton.setText(QCoreApplication.translate("DialogBuisinessCard", u"+", None))
#if QT_CONFIG(tooltip)
        self.decrease_hops_pushButton.setToolTip(QCoreApplication.translate("DialogBuisinessCard", u"<html><head/><body><p>0 = Eintrag wird nur lokal gespeichert.</p><p>1 = Eintrag wird auch an Freunde geteilt (Freund ersten Grads)</p><p>2 = Eintrag wird bis an Freunde der Freunde geteilt (2. Grad)</p><p>3 = Teilen bis Freunde 3. Grads</p><p>4 = Teilen bis Freunde 4. Grads</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.decrease_hops_pushButton.setText(QCoreApplication.translate("DialogBuisinessCard", u"-", None))
        self.determine_coordinates_pushButton.setText(QCoreApplication.translate("DialogBuisinessCard", u"Ermitteln", None))
        self.status_label.setText(QCoreApplication.translate("DialogBuisinessCard", u"status_label", None))
        self.checkBox_extend_hops.setText(QCoreApplication.translate("DialogBuisinessCard", u"erweitert", None))
        self.adopt_validity_pushButton.setText(QCoreApplication.translate("DialogBuisinessCard", u"G\u00fcltigkeit \u00e4ndern", None))
        self.month_valid_label.setText(QCoreApplication.translate("DialogBuisinessCard", u"Monate g\u00fcltig:", None))
        self.label_17.setText(QCoreApplication.translate("DialogBuisinessCard", u"Sonstige Kontaktm\u00f6glichkeiten", None))
        self.checkBox_add_to_mailling_list.setText(QCoreApplication.translate("DialogBuisinessCard", u"in Mailverteiler aufnehmen", None))
    # retranslateUi

