# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dialog_friendship.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QTextBrowser, QTextEdit, QWidget)

class Ui_DialogFriendship(object):
    def setupUi(self, DialogFriendship):
        if not DialogFriendship.objectName():
            DialogFriendship.setObjectName(u"DialogFriendship")
        DialogFriendship.resize(653, 771)
        self.textBrowser_ownkey = QTextBrowser(DialogFriendship)
        self.textBrowser_ownkey.setObjectName(u"textBrowser_ownkey")
        self.textBrowser_ownkey.setGeometry(QRect(10, 60, 630, 191))
        font = QFont()
        font.setFamilies([u"FreeMono"])
        font.setPointSize(11)
        font.setKerning(False)
        self.textBrowser_ownkey.setFont(font)
        self.label_own_key = QLabel(DialogFriendship)
        self.label_own_key.setObjectName(u"label_own_key")
        self.label_own_key.setGeometry(QRect(10, 40, 361, 16))
        self.textEdit_friendskey = QTextEdit(DialogFriendship)
        self.textEdit_friendskey.setObjectName(u"textEdit_friendskey")
        self.textEdit_friendskey.setGeometry(QRect(10, 500, 630, 191))
        font1 = QFont()
        font1.setFamilies([u"FreeMono"])
        font1.setPointSize(11)
        self.textEdit_friendskey.setFont(font1)
        self.label_enter_friends_key = QLabel(DialogFriendship)
        self.label_enter_friends_key.setObjectName(u"label_enter_friends_key")
        self.label_enter_friends_key.setGeometry(QRect(10, 480, 381, 16))
        self.line = QFrame(DialogFriendship)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(10, 320, 631, 20))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.lineEdit_friends_name = QLineEdit(DialogFriendship)
        self.lineEdit_friends_name.setObjectName(u"lineEdit_friends_name")
        self.lineEdit_friends_name.setGeometry(QRect(10, 390, 301, 23))
        self.lineEdit_friends_comment = QLineEdit(DialogFriendship)
        self.lineEdit_friends_comment.setObjectName(u"lineEdit_friends_comment")
        self.lineEdit_friends_comment.setGeometry(QRect(10, 440, 631, 23))
        self.label = QLabel(DialogFriendship)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 370, 151, 16))
        self.label_4 = QLabel(DialogFriendship)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 420, 351, 16))
        self.label_friendhip_date_info = QLabel(DialogFriendship)
        self.label_friendhip_date_info.setObjectName(u"label_friendhip_date_info")
        self.label_friendhip_date_info.setGeometry(QRect(10, 10, 551, 16))
        self.spinBox_friendship_years = QSpinBox(DialogFriendship)
        self.spinBox_friendship_years.setObjectName(u"spinBox_friendship_years")
        self.spinBox_friendship_years.setGeometry(QRect(10, 260, 35, 24))
        self.spinBox_friendship_years.setMinimum(1)
        self.spinBox_friendship_years.setMaximum(5)
        self.spinBox_friendship_years.setValue(5)
        self.label_help_text = QLabel(DialogFriendship)
        self.label_help_text.setObjectName(u"label_help_text")
        self.label_help_text.setGeometry(QRect(10, 690, 631, 41))
        self.label_help_text.setWordWrap(True)
        self.pushButton_copy_ownkey_to_clipboard = QPushButton(DialogFriendship)
        self.pushButton_copy_ownkey_to_clipboard.setObjectName(u"pushButton_copy_ownkey_to_clipboard")
        self.pushButton_copy_ownkey_to_clipboard.setGeometry(QRect(190, 290, 261, 23))
        self.label_own_key_expiration = QLabel(DialogFriendship)
        self.label_own_key_expiration.setObjectName(u"label_own_key_expiration")
        self.label_own_key_expiration.setGeometry(QRect(396, 40, 241, 16))
        self.label_friend_key_expiration = QLabel(DialogFriendship)
        self.label_friend_key_expiration.setObjectName(u"label_friend_key_expiration")
        self.label_friend_key_expiration.setGeometry(QRect(390, 480, 241, 16))
        self.label_6 = QLabel(DialogFriendship)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(330, 370, 151, 16))
        self.lineEdit_friends_email = QLineEdit(DialogFriendship)
        self.lineEdit_friends_email.setObjectName(u"lineEdit_friends_email")
        self.lineEdit_friends_email.setGeometry(QRect(330, 390, 301, 23))
        self.pushButton_extend_friendship = QPushButton(DialogFriendship)
        self.pushButton_extend_friendship.setObjectName(u"pushButton_extend_friendship")
        self.pushButton_extend_friendship.setGeometry(QRect(190, 340, 261, 23))
        self.layoutWidget = QWidget(DialogFriendship)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 740, 631, 25))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pushButton_add_renew_friendship = QPushButton(self.layoutWidget)
        self.pushButton_add_renew_friendship.setObjectName(u"pushButton_add_renew_friendship")

        self.horizontalLayout_3.addWidget(self.pushButton_add_renew_friendship)

        self.pushButton_close = QPushButton(self.layoutWidget)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.horizontalLayout_3.addWidget(self.pushButton_close)

        self.pushButton_cancel_friendship = QPushButton(self.layoutWidget)
        self.pushButton_cancel_friendship.setObjectName(u"pushButton_cancel_friendship")

        self.horizontalLayout_3.addWidget(self.pushButton_cancel_friendship)

        self.label_years_of_validity = QLabel(DialogFriendship)
        self.label_years_of_validity.setObjectName(u"label_years_of_validity")
        self.label_years_of_validity.setGeometry(QRect(50, 260, 561, 21))
        self.label_years_of_validity.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_years_of_validity.setWordWrap(True)

        self.retranslateUi(DialogFriendship)

        QMetaObject.connectSlotsByName(DialogFriendship)
    # setupUi

    def retranslateUi(self, DialogFriendship):
        DialogFriendship.setWindowTitle(QCoreApplication.translate("DialogFriendship", u"Freund hinzuf\u00fcgen", None))
        self.label_own_key.setText(QCoreApplication.translate("DialogFriendship", u"Eigener Schl\u00fcssel (an Freund senden)", None))
        self.label_enter_friends_key.setText(QCoreApplication.translate("DialogFriendship", u"Schl\u00fcssel vom Freund (unten im Textfeld einf\u00fcgen)", None))
        self.label.setText(QCoreApplication.translate("DialogFriendship", u"Name des Freundes", None))
        self.label_4.setText(QCoreApplication.translate("DialogFriendship", u"Kommentar (f\u00fcr weitere Infos zum Freund)", None))
        self.label_friendhip_date_info.setText(QCoreApplication.translate("DialogFriendship", u"Freund seit ... L\u00e4uft ab am ...", None))
        self.label_help_text.setText(QCoreApplication.translate("DialogFriendship", u"label_help_text", None))
        self.pushButton_copy_ownkey_to_clipboard.setText(QCoreApplication.translate("DialogFriendship", u"Schl\u00fcssel in Zwischenablage kopieren", None))
        self.label_own_key_expiration.setText(QCoreApplication.translate("DialogFriendship", u"label_own_key_expiration", None))
        self.label_friend_key_expiration.setText(QCoreApplication.translate("DialogFriendship", u"label_friend_key_expiration", None))
        self.label_6.setText(QCoreApplication.translate("DialogFriendship", u"Email des Freundes", None))
        self.pushButton_extend_friendship.setText(QCoreApplication.translate("DialogFriendship", u"Freundschaft verl\u00e4ngern", None))
        self.pushButton_add_renew_friendship.setText(QCoreApplication.translate("DialogFriendship", u"Hinzuf\u00fcgen", None))
        self.pushButton_close.setText(QCoreApplication.translate("DialogFriendship", u"Schlie\u00dfen", None))
        self.pushButton_cancel_friendship.setText(QCoreApplication.translate("DialogFriendship", u"Freundschaft beenden", None))
        self.label_years_of_validity.setText(QCoreApplication.translate("DialogFriendship", u"Jahre G\u00fcltigkeit des Schl\u00fcssel. (maximale Freundschaftsdauer festlegen).", None))
    # retranslateUi

