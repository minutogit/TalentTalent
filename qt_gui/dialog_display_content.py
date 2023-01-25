# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_display_content.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QHBoxLayout,
    QPushButton, QSizePolicy, QTextBrowser, QWidget)

class Ui_DialogDisplayContent(object):
    def setupUi(self, DialogDisplayContent):
        if not DialogDisplayContent.objectName():
            DialogDisplayContent.setObjectName(u"DialogDisplayContent")
        DialogDisplayContent.resize(700, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogDisplayContent.sizePolicy().hasHeightForWidth())
        DialogDisplayContent.setSizePolicy(sizePolicy)
        self.textBrowser = QTextBrowser(DialogDisplayContent)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(15, 11, 671, 551))
        self.layoutWidget = QWidget(DialogDisplayContent)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(180, 570, 371, 25))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_edit = QPushButton(self.layoutWidget)
        self.pushButton_edit.setObjectName(u"pushButton_edit")

        self.horizontalLayout.addWidget(self.pushButton_edit)

        self.pushButton_close = QPushButton(self.layoutWidget)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.horizontalLayout.addWidget(self.pushButton_close)

        self.pushButton_delete_hide = QPushButton(self.layoutWidget)
        self.pushButton_delete_hide.setObjectName(u"pushButton_delete_hide")

        self.horizontalLayout.addWidget(self.pushButton_delete_hide)

        self.checkBox_show_Details = QCheckBox(DialogDisplayContent)
        self.checkBox_show_Details.setObjectName(u"checkBox_show_Details")
        self.checkBox_show_Details.setGeometry(QRect(20, 570, 121, 21))

        self.retranslateUi(DialogDisplayContent)

        QMetaObject.connectSlotsByName(DialogDisplayContent)
    # setupUi

    def retranslateUi(self, DialogDisplayContent):
        DialogDisplayContent.setWindowTitle(QCoreApplication.translate("DialogDisplayContent", u"Dialog", None))
        self.pushButton_edit.setText(QCoreApplication.translate("DialogDisplayContent", u"Bearbeiten", None))
        self.pushButton_close.setText(QCoreApplication.translate("DialogDisplayContent", u"Schlie\u00dfen", None))
        self.pushButton_delete_hide.setText(QCoreApplication.translate("DialogDisplayContent", u"L\u00f6schen", None))
        self.checkBox_show_Details.setText(QCoreApplication.translate("DialogDisplayContent", u"Details anzeigen", None))
    # retranslateUi

