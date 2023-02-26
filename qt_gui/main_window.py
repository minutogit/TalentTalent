# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(762, 480)
        MainWindow.setAutoFillBackground(False)
        self.actionAdd_BusinessCard = QAction(MainWindow)
        self.actionAdd_BusinessCard.setObjectName(u"actionAdd_BusinessCard")
        self.action_generate_database_for_friends = QAction(MainWindow)
        self.action_generate_database_for_friends.setObjectName(u"action_generate_database_for_friends")
        self.actionGenerate_Profile = QAction(MainWindow)
        self.actionGenerate_Profile.setObjectName(u"actionGenerate_Profile")
        self.action_import_database_from_friends = QAction(MainWindow)
        self.action_import_database_from_friends.setObjectName(u"action_import_database_from_friends")
        self.action_generate_database_with_password = QAction(MainWindow)
        self.action_generate_database_with_password.setObjectName(u"action_generate_database_with_password")
        self.action_import_database_with_password = QAction(MainWindow)
        self.action_import_database_with_password.setObjectName(u"action_import_database_with_password")
        self.actionAddFriendship = QAction(MainWindow)
        self.actionAddFriendship.setObjectName(u"actionAddFriendship")
        self.actionFriendshipList = QAction(MainWindow)
        self.actionFriendshipList.setObjectName(u"actionFriendshipList")
        self.actionChangePassword = QAction(MainWindow)
        self.actionChangePassword.setObjectName(u"actionChangePassword")
        self.actionRestoreProfile = QAction(MainWindow)
        self.actionRestoreProfile.setObjectName(u"actionRestoreProfile")
        self.actionForgotPassword = QAction(MainWindow)
        self.actionForgotPassword.setObjectName(u"actionForgotPassword")
        self.actionLogIn = QAction(MainWindow)
        self.actionLogIn.setObjectName(u"actionLogIn")
        self.actionLogOut = QAction(MainWindow)
        self.actionLogOut.setObjectName(u"actionLogOut")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actiontest = QAction(MainWindow)
        self.actiontest.setObjectName(u"actiontest")
        self.actionCleanDatabase = QAction(MainWindow)
        self.actionCleanDatabase.setObjectName(u"actionCleanDatabase")
        self.actionProfilSettings = QAction(MainWindow)
        self.actionProfilSettings.setObjectName(u"actionProfilSettings")
        self.actionShowSeedWords = QAction(MainWindow)
        self.actionShowSeedWords.setObjectName(u"actionShowSeedWords")
        self.actionHTML_Export = QAction(MainWindow)
        self.actionHTML_Export.setObjectName(u"actionHTML_Export")
        self.actionEMail_to_friends = QAction(MainWindow)
        self.actionEMail_to_friends.setObjectName(u"actionEMail_to_friends")
        self.action_mailinglist = QAction(MainWindow)
        self.action_mailinglist.setObjectName(u"action_mailinglist")
        self.action_mail_import = QAction(MainWindow)
        self.action_mail_import.setObjectName(u"action_mail_import")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.comboBox_column_selection = QComboBox(self.centralwidget)
        self.comboBox_column_selection.addItem("")
        self.comboBox_column_selection.setObjectName(u"comboBox_column_selection")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_column_selection.sizePolicy().hasHeightForWidth())
        self.comboBox_column_selection.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.comboBox_column_selection)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label)

        self.lineEdit_filter = QLineEdit(self.centralwidget)
        self.lineEdit_filter.setObjectName(u"lineEdit_filter")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(20)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lineEdit_filter.sizePolicy().hasHeightForWidth())
        self.lineEdit_filter.setSizePolicy(sizePolicy1)
        self.lineEdit_filter.setMinimumSize(QSize(100, 0))

        self.horizontalLayout_4.addWidget(self.lineEdit_filter)

        self.comboBox_filter = QComboBox(self.centralwidget)
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.addItem("")
        self.comboBox_filter.setObjectName(u"comboBox_filter")
        sizePolicy.setHeightForWidth(self.comboBox_filter.sizePolicy().hasHeightForWidth())
        self.comboBox_filter.setSizePolicy(sizePolicy)
        self.comboBox_filter.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_4.addWidget(self.comboBox_filter)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addWidget(self.tableView)

        self.label_statistics = QLabel(self.centralwidget)
        self.label_statistics.setObjectName(u"label_statistics")

        self.verticalLayout.addWidget(self.label_statistics)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_add_own_businesscard = QPushButton(self.centralwidget)
        self.pushButton_add_own_businesscard.setObjectName(u"pushButton_add_own_businesscard")

        self.horizontalLayout_3.addWidget(self.pushButton_add_own_businesscard)

        self.pushButton_add_businesscard = QPushButton(self.centralwidget)
        self.pushButton_add_businesscard.setObjectName(u"pushButton_add_businesscard")

        self.horizontalLayout_3.addWidget(self.pushButton_add_businesscard)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 762, 20))
        self.menuStart = QMenu(self.menubar)
        self.menuStart.setObjectName(u"menuStart")
        self.menuExtended = QMenu(self.menubar)
        self.menuExtended.setObjectName(u"menuExtended")
        self.menuFriends = QMenu(self.menubar)
        self.menuFriends.setObjectName(u"menuFriends")
        self.menuProfil = QMenu(self.menubar)
        self.menuProfil.setObjectName(u"menuProfil")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuStart.menuAction())
        self.menubar.addAction(self.menuFriends.menuAction())
        self.menubar.addAction(self.menuProfil.menuAction())
        self.menubar.addAction(self.menuExtended.menuAction())
        self.menuStart.addAction(self.actionAdd_BusinessCard)
        self.menuStart.addAction(self.actionExit)
        self.menuExtended.addAction(self.action_generate_database_with_password)
        self.menuExtended.addAction(self.action_import_database_with_password)
        self.menuExtended.addAction(self.actionCleanDatabase)
        self.menuExtended.addAction(self.actionHTML_Export)
        self.menuExtended.addAction(self.action_mailinglist)
        self.menuExtended.addAction(self.action_mail_import)
        self.menuFriends.addAction(self.actionFriendshipList)
        self.menuFriends.addAction(self.actionAddFriendship)
        self.menuFriends.addAction(self.action_generate_database_for_friends)
        self.menuFriends.addAction(self.action_import_database_from_friends)
        self.menuFriends.addAction(self.actionEMail_to_friends)
        self.menuProfil.addAction(self.actionProfilSettings)
        self.menuProfil.addAction(self.actionLogIn)
        self.menuProfil.addAction(self.actionLogOut)
        self.menuProfil.addAction(self.actionGenerate_Profile)
        self.menuProfil.addAction(self.actionRestoreProfile)
        self.menuProfil.addAction(self.actionChangePassword)
        self.menuProfil.addAction(self.actionForgotPassword)
        self.menuProfil.addAction(self.actionShowSeedWords)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("")
        self.actionAdd_BusinessCard.setText(QCoreApplication.translate("MainWindow", u"Visitenkarte hinzuf\u00fcgen", None))
        self.action_generate_database_for_friends.setText(QCoreApplication.translate("MainWindow", u"Datenbank an Freunde teilen", None))
        self.actionGenerate_Profile.setText(QCoreApplication.translate("MainWindow", u"Profil erstellen", None))
        self.action_import_database_from_friends.setText(QCoreApplication.translate("MainWindow", u"Datenbank von Freunden importieren", None))
        self.action_generate_database_with_password.setText(QCoreApplication.translate("MainWindow", u"Datenbank mit Passwort teilen", None))
        self.action_import_database_with_password.setText(QCoreApplication.translate("MainWindow", u"Datenbank mit Passwort importieren", None))
        self.actionAddFriendship.setText(QCoreApplication.translate("MainWindow", u"Freund hinzuf\u00fcgen", None))
        self.actionFriendshipList.setText(QCoreApplication.translate("MainWindow", u"Meine Freunde", None))
        self.actionChangePassword.setText(QCoreApplication.translate("MainWindow", u"Passwort \u00e4ndern", None))
        self.actionRestoreProfile.setText(QCoreApplication.translate("MainWindow", u"Profil wiederherstellen", None))
        self.actionForgotPassword.setText(QCoreApplication.translate("MainWindow", u"Passwort vergessen", None))
        self.actionLogIn.setText(QCoreApplication.translate("MainWindow", u"Anmelden", None))
        self.actionLogOut.setText(QCoreApplication.translate("MainWindow", u"Abmelden", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Beenden", None))
        self.actiontest.setText(QCoreApplication.translate("MainWindow", u"test", None))
        self.actionCleanDatabase.setText(QCoreApplication.translate("MainWindow", u"Datenbank reinigen", None))
        self.actionProfilSettings.setText(QCoreApplication.translate("MainWindow", u"Profil Einstellungen", None))
        self.actionShowSeedWords.setText(QCoreApplication.translate("MainWindow", u"Schl\u00fcsselw\u00f6rter anzeigen", None))
        self.actionHTML_Export.setText(QCoreApplication.translate("MainWindow", u"HTML-Export der Eintr\u00e4ge", None))
        self.actionEMail_to_friends.setText(QCoreApplication.translate("MainWindow", u"E-Mail an Freunde", None))
        self.action_mailinglist.setText(QCoreApplication.translate("MainWindow", u"E-Mail an Mailverteiler", None))
        self.action_mail_import.setText(QCoreApplication.translate("MainWindow", u"Visitenkarte E-Mail Import", None))
        self.comboBox_column_selection.setItemText(0, QCoreApplication.translate("MainWindow", u"Spalten", None))

#if QT_CONFIG(tooltip)
        self.comboBox_column_selection.setToolTip(QCoreApplication.translate("MainWindow", u"test", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("MainWindow", u"Filter:", None))
        self.comboBox_filter.setItemText(0, QCoreApplication.translate("MainWindow", u"Alle G\u00fcltigen", None))
        self.comboBox_filter.setItemText(1, QCoreApplication.translate("MainWindow", u"Nur Eigene", None))
        self.comboBox_filter.setItemText(2, QCoreApplication.translate("MainWindow", u"Nicht Eigene", None))
        self.comboBox_filter.setItemText(3, QCoreApplication.translate("MainWindow", u"Eigene (abgelaufen)", None))
        self.comboBox_filter.setItemText(4, QCoreApplication.translate("MainWindow", u"Ausgeblendete", None))

        self.label_statistics.setText(QCoreApplication.translate("MainWindow", u"---", None))
        self.pushButton_add_own_businesscard.setText(QCoreApplication.translate("MainWindow", u"Pers\u00f6nliche Visitenkarte", None))
        self.pushButton_add_businesscard.setText(QCoreApplication.translate("MainWindow", u"Andere Visitenkarte hinzuf\u00fcgen", None))
        self.menuStart.setTitle(QCoreApplication.translate("MainWindow", u"Start", None))
        self.menuExtended.setTitle(QCoreApplication.translate("MainWindow", u"Erweitert", None))
        self.menuFriends.setTitle(QCoreApplication.translate("MainWindow", u"Freunde", None))
        self.menuProfil.setTitle(QCoreApplication.translate("MainWindow", u"Profil", None))
    # retranslateUi

