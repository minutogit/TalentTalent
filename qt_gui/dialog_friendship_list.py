# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_friendship_list.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QDialog,
    QHBoxLayout, QHeaderView, QPushButton, QSizePolicy,
    QTableView, QWidget)

class Ui_DialogFriendshipList(object):
    def setupUi(self, DialogFriendshipList):
        if not DialogFriendshipList.objectName():
            DialogFriendshipList.setObjectName(u"DialogFriendshipList")
        DialogFriendshipList.resize(753, 446)
        self.tableView_friendlist = QTableView(DialogFriendshipList)
        self.tableView_friendlist.setObjectName(u"tableView_friendlist")
        self.tableView_friendlist.setGeometry(QRect(10, 10, 731, 391))
        self.tableView_friendlist.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.comboBox_friend_filter = QComboBox(DialogFriendshipList)
        self.comboBox_friend_filter.addItem("")
        self.comboBox_friend_filter.addItem("")
        self.comboBox_friend_filter.setObjectName(u"comboBox_friend_filter")
        self.comboBox_friend_filter.setGeometry(QRect(540, 410, 201, 23))
        self.widget = QWidget(DialogFriendshipList)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(120, 410, 371, 25))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_friend = QPushButton(self.widget)
        self.pushButton_add_friend.setObjectName(u"pushButton_add_friend")

        self.horizontalLayout.addWidget(self.pushButton_add_friend)

        self.pushButton_close = QPushButton(self.widget)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.horizontalLayout.addWidget(self.pushButton_close)


        self.retranslateUi(DialogFriendshipList)

        QMetaObject.connectSlotsByName(DialogFriendshipList)
    # setupUi

    def retranslateUi(self, DialogFriendshipList):
        DialogFriendshipList.setWindowTitle(QCoreApplication.translate("DialogFriendshipList", u"Dialog", None))
        self.comboBox_friend_filter.setItemText(0, QCoreApplication.translate("DialogFriendshipList", u"g\u00fcltige Freunde", None))
        self.comboBox_friend_filter.setItemText(1, QCoreApplication.translate("DialogFriendshipList", u"abgelaufene Freuned", None))

        self.pushButton_add_friend.setText(QCoreApplication.translate("DialogFriendshipList", u"Freund hinzuf\u00fcgen", None))
        self.pushButton_close.setText(QCoreApplication.translate("DialogFriendshipList", u"Schlie\u00dfen", None))
    # retranslateUi

