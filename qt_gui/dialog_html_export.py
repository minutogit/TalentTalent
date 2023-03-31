# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_html_export.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFormLayout, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_DialogHtmlExport(object):
    def setupUi(self, DialogHtmlExport):
        if not DialogHtmlExport.objectName():
            DialogHtmlExport.setObjectName(u"DialogHtmlExport")
        DialogHtmlExport.resize(656, 401)
        self.pushButton_html_export = QPushButton(DialogHtmlExport)
        self.pushButton_html_export.setObjectName(u"pushButton_html_export")
        self.pushButton_html_export.setGeometry(QRect(210, 240, 211, 23))
        self.line = QFrame(DialogHtmlExport)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(20, 260, 621, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.pushButton_set_own_location = QPushButton(DialogHtmlExport)
        self.pushButton_set_own_location.setObjectName(u"pushButton_set_own_location")
        self.pushButton_set_own_location.setGeometry(QRect(369, 210, 231, 20))
        self.layoutWidget = QWidget(DialogHtmlExport)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 20, 311, 161))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.layoutWidget)
        self.label_11.setObjectName(u"label_11")
        font = QFont()
        font.setFamilies([u"Sans Serif"])
        font.setBold(True)
        self.label_11.setFont(font)

        self.verticalLayout.addWidget(self.label_11)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label_2)

        self.comboBox_filter = QComboBox(self.layoutWidget)
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.setObjectName(u"comboBox_filter")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_filter.sizePolicy().hasHeightForWidth())
        self.comboBox_filter.setSizePolicy(sizePolicy)
        self.comboBox_filter.setMinimumSize(QSize(200, 0))

        self.verticalLayout.addWidget(self.comboBox_filter)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignBottom|Qt.AlignLeading|Qt.AlignLeft)

        self.verticalLayout.addWidget(self.label)

        self.comboBox_column_selection = QComboBox(self.layoutWidget)
        self.comboBox_column_selection.addItem("")
        self.comboBox_column_selection.setObjectName(u"comboBox_column_selection")
        sizePolicy.setHeightForWidth(self.comboBox_column_selection.sizePolicy().hasHeightForWidth())
        self.comboBox_column_selection.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.comboBox_column_selection)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(200, 0))
        self.label_3.setWordWrap(True)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_max_distance = QLineEdit(self.layoutWidget)
        self.lineEdit_max_distance.setObjectName(u"lineEdit_max_distance")

        self.horizontalLayout_2.addWidget(self.lineEdit_max_distance)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.layoutWidget1 = QWidget(DialogHtmlExport)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(341, 20, 300, 181))
        self.formLayout = QFormLayout(self.layoutWidget1)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setBold(True)
        self.label_4.setFont(font1)

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_4)

        self.label_10 = QLabel(self.layoutWidget1)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.label_10)

        self.label_8 = QLabel(self.layoutWidget1)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_8)

        self.street_lineEdit = QLineEdit(self.layoutWidget1)
        self.street_lineEdit.setObjectName(u"street_lineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.street_lineEdit)

        self.label_6 = QLabel(self.layoutWidget1)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.zip_code_lineEdit = QLineEdit(self.layoutWidget1)
        self.zip_code_lineEdit.setObjectName(u"zip_code_lineEdit")
        self.zip_code_lineEdit.setInputMethodHints(Qt.ImhDigitsOnly)
        self.zip_code_lineEdit.setClearButtonEnabled(False)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.zip_code_lineEdit)

        self.label_7 = QLabel(self.layoutWidget1)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.city_lineEdit = QLineEdit(self.layoutWidget1)
        self.city_lineEdit.setObjectName(u"city_lineEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.city_lineEdit)

        self.label_5 = QLabel(self.layoutWidget1)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_5)

        self.country_lineEdit = QLineEdit(self.layoutWidget1)
        self.country_lineEdit.setObjectName(u"country_lineEdit")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.country_lineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_9 = QLabel(self.layoutWidget1)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout.addWidget(self.label_9)

        self.coordinates_lineEdit = QLineEdit(self.layoutWidget1)
        self.coordinates_lineEdit.setObjectName(u"coordinates_lineEdit")

        self.horizontalLayout.addWidget(self.coordinates_lineEdit)

        self.determine_coordinates_pushButton = QPushButton(self.layoutWidget1)
        self.determine_coordinates_pushButton.setObjectName(u"determine_coordinates_pushButton")

        self.horizontalLayout.addWidget(self.determine_coordinates_pushButton)


        self.formLayout.setLayout(6, QFormLayout.SpanningRole, self.horizontalLayout)

        self.checkBox_compact_mode = QCheckBox(DialogHtmlExport)
        self.checkBox_compact_mode.setObjectName(u"checkBox_compact_mode")
        self.checkBox_compact_mode.setGeometry(QRect(13, 210, 309, 21))
        self.label_12 = QLabel(DialogHtmlExport)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(13, 190, 231, 16))
        self.label_12.setFont(font1)
        self.max_radius_lineedit = QLineEdit(DialogHtmlExport)
        self.max_radius_lineedit.setObjectName(u"max_radius_lineedit")
        self.max_radius_lineedit.setGeometry(QRect(160, 370, 71, 23))
        self.max_radius_lineedit.setInputMethodHints(Qt.ImhNone)
        self.label_13 = QLabel(DialogHtmlExport)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(20, 280, 111, 16))
        self.label_13.setFont(font1)
        self.label_14 = QLabel(DialogHtmlExport)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(20, 300, 611, 61))
        self.label_14.setWordWrap(True)
        self.label_15 = QLabel(DialogHtmlExport)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(20, 360, 141, 31))
        font2 = QFont()
        font2.setBold(False)
        self.label_15.setFont(font2)
        self.label_15.setWordWrap(True)
        self.pushButton_html_multi_export = QPushButton(DialogHtmlExport)
        self.pushButton_html_multi_export.setObjectName(u"pushButton_html_multi_export")
        self.pushButton_html_multi_export.setGeometry(QRect(260, 370, 191, 23))

        self.retranslateUi(DialogHtmlExport)

        QMetaObject.connectSlotsByName(DialogHtmlExport)
    # setupUi

    def retranslateUi(self, DialogHtmlExport):
        DialogHtmlExport.setWindowTitle(QCoreApplication.translate("DialogHtmlExport", u"HTML Export", None))
        self.pushButton_html_export.setText(QCoreApplication.translate("DialogHtmlExport", u"Einzel-Export starten", None))
#if QT_CONFIG(tooltip)
        self.pushButton_set_own_location.setToolTip(QCoreApplication.translate("DialogHtmlExport", u"Eigener Standort aus Profil-Einstellungen", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_set_own_location.setText(QCoreApplication.translate("DialogHtmlExport", u"Eigenen Standort setzen", None))
        self.label_11.setText(QCoreApplication.translate("DialogHtmlExport", u"Filter (Was soll exportiert werden?)", None))
        self.label_2.setText(QCoreApplication.translate("DialogHtmlExport", u"zu exportierende Eintr\u00e4ge", None))
        self.comboBox_filter.setItemText(0, QCoreApplication.translate("DialogHtmlExport", u"Alle G\u00fcltigen", None))
        self.comboBox_filter.setItemText(1, QCoreApplication.translate("DialogHtmlExport", u"Nur Eigene", None))
        self.comboBox_filter.setItemText(2, QCoreApplication.translate("DialogHtmlExport", u"Nicht Eigene", None))

        self.label.setText(QCoreApplication.translate("DialogHtmlExport", u"zu exportierende Eintragsinhalte", None))
        self.comboBox_column_selection.setItemText(0, QCoreApplication.translate("DialogHtmlExport", u"Spalten", None))

#if QT_CONFIG(tooltip)
        self.comboBox_column_selection.setToolTip(QCoreApplication.translate("DialogHtmlExport", u"test", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("DialogHtmlExport", u"max. Entfernung (km) vom Standort (0 = unbegrenzt)", None))
        self.lineEdit_max_distance.setInputMask(QCoreApplication.translate("DialogHtmlExport", u"00000", None))
        self.label_4.setText(QCoreApplication.translate("DialogHtmlExport", u"Standort (f\u00fcr Entfernungsangaben)", None))
        self.label_10.setText(QCoreApplication.translate("DialogHtmlExport", u"Korrekte Koordinaten sind entscheidend", None))
        self.label_8.setText(QCoreApplication.translate("DialogHtmlExport", u"Stra\u00dfe", None))
        self.street_lineEdit.setText("")
        self.label_6.setText(QCoreApplication.translate("DialogHtmlExport", u"PLZ", None))
        self.zip_code_lineEdit.setText("")
        self.label_7.setText(QCoreApplication.translate("DialogHtmlExport", u"Ort", None))
        self.city_lineEdit.setText("")
        self.label_5.setText(QCoreApplication.translate("DialogHtmlExport", u"Land", None))
        self.country_lineEdit.setText("")
        self.label_9.setText(QCoreApplication.translate("DialogHtmlExport", u"Koordinaten*", None))
        self.coordinates_lineEdit.setText("")
        self.determine_coordinates_pushButton.setText(QCoreApplication.translate("DialogHtmlExport", u"Ermitteln", None))
        self.checkBox_compact_mode.setText(QCoreApplication.translate("DialogHtmlExport", u"Kompakt (Zeilenumbr\u00fcche etc. entfernen)", None))
        self.label_12.setText(QCoreApplication.translate("DialogHtmlExport", u"Text Einstellungen", None))
        self.max_radius_lineedit.setInputMask("")
        self.label_13.setText(QCoreApplication.translate("DialogHtmlExport", u"Multi-Export", None))
        self.label_14.setText(QCoreApplication.translate("DialogHtmlExport", u"Hier ist ein Export f\u00fcr mehrere Standorte m\u00f6glich. Orte von Angeboten, die du gesammelt hast, werden in Gruppen mit einem maximalen Radius zusammengefasst. F\u00fcr jeden Ort der eine Gruppe am besten repr\u00e4sentiert, wird ein Export mit jeweiligen Entfernungsangaben gemacht.\n"
"", None))
        self.label_15.setText(QCoreApplication.translate("DialogHtmlExport", u"maximaler Gruppen-Radius (in km)", None))
        self.pushButton_html_multi_export.setText(QCoreApplication.translate("DialogHtmlExport", u"Multi-Export starten", None))
    # retranslateUi

