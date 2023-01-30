# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_mail_import.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_DialogMailImport(object):
    def setupUi(self, DialogMailImport):
        if not DialogMailImport.objectName():
            DialogMailImport.setObjectName(u"DialogMailImport")
        DialogMailImport.resize(630, 408)
        self.widget = QWidget(DialogMailImport)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(9, 9, 611, 391))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_description = QLabel(self.widget)
        self.label_description.setObjectName(u"label_description")

        self.verticalLayout.addWidget(self.label_description)

        self.textEdit_mail_text = QTextEdit(self.widget)
        self.textEdit_mail_text.setObjectName(u"textEdit_mail_text")
        self.textEdit_mail_text.setLineWrapColumnOrWidth(0)

        self.verticalLayout.addWidget(self.textEdit_mail_text)

        self.pushButton_import = QPushButton(self.widget)
        self.pushButton_import.setObjectName(u"pushButton_import")

        self.verticalLayout.addWidget(self.pushButton_import)


        self.retranslateUi(DialogMailImport)

        QMetaObject.connectSlotsByName(DialogMailImport)
    # setupUi

    def retranslateUi(self, DialogMailImport):
        DialogMailImport.setWindowTitle(QCoreApplication.translate("DialogMailImport", u"E-Mail Import", None))
        self.label_description.setText(QCoreApplication.translate("DialogMailImport", u"E-Mail Text vom Webformular zum sammeln Eintr\u00e4gen hier einf\u00fcgen und importieren.", None))
        self.pushButton_import.setText(QCoreApplication.translate("DialogMailImport", u"Importieren", None))
    # retranslateUi

