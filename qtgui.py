import binascii, warnings
import re
from datetime import datetime, timedelta
import logging, os
from PySide6.QtCore import QTimer, QSortFilterProxyModel, QTranslator
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import QApplication, QMainWindow, \
    QMessageBox, QFileDialog
from PySide6 import QtSql, QtGui   #Qt.CaseInsensitive  # , Qt

from PySide6.QtCore import Qt

from qt_gui.main_window import Ui_MainWindow
from qt_gui.dialog_generate_profile import Ui_DialogGenerateProfile
from qt_gui.dialog_new_password import Ui_DialogNewPassword
from qt_gui.dialog_enter_password import Ui_DialogEnterPassword
from qt_gui.dialog_businesscard import Ui_DialogBuisinessCard
from qt_gui.dialog_enter_import_password import Ui_DialogEnterImportPassword
from qt_gui.dialog_friendship import Ui_DialogFriendship
from qt_gui.dialog_friendship_list import Ui_DialogFriendshipList
from qt_gui.dialog_restore_profile import Ui_DialogRestoreProfile
from qt_gui.dialog_profile_create_selection import Ui_Dialog_Profile_Create_Selection
from qt_gui.dialog_display_content import Ui_DialogDisplayContent
from qt_gui.dialog_profile_settings import Ui_DialogProfileSettings
from qt_gui.dialog_mail_import import Ui_DialogMailImport
from qt_gui.dialog_html_export import Ui_DialogHtmlExport

from functions import dprint
from meta_info import __version__, __title__
import functions, cryptfunctions
from utils import data_card_to_html, friend_data_to_html, html_export_head, data_card_html_export, key_to_text
import utils


# Config und Daten einlesen  (zusätzlich für temporäre globale variablen)
conf = functions.config()
conf.read()

# logging management
LOG_FILENAME = os.path.join(os.getcwd(), conf.PROGRAMM_FOLDER, "log.txt")
log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # console log-level
console_handler.setFormatter(log_format)
log.addHandler(console_handler)
file_handler = logging.FileHandler(LOG_FILENAME)
file_handler.setLevel(logging.WARN)  # file-log-level
file_handler.setFormatter(log_format)
log.addHandler(file_handler)
#log.setLevel(logging.ERROR)  # complete level, this level limits file and console log

logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

crypt = cryptfunctions.CryptoClass()
localdb = functions.local_card_db("talent.db", conf.PROGRAMM_FOLDER)



def show_message_box(title, text):
    dlg = QMessageBox()
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.exec()

def get_coordinates(self, searched_location):
    """determines the coordinates for a searched location"""
    [result_ok, found_address, coordinates] = functions.get_coordinates(searched_location)
    if result_ok:
        msgbox = QMessageBox.question(self, "Koordinaten übernehmen?",
                                      f"""Gesuchte Adresse:  {searched_location}\n\nGefundene Adresse:  {found_address}\n\nKoordinaten für gefundene Adresse:  {coordinates}\n\nKoordinaten übernehmen?""")
        if msgbox == QMessageBox.Yes:
            return str(coordinates)
        else:
            return ""
    else:
        show_message_box("Fehler",
                         f"Koordinaten für: {searched_location}\n konnten nicht ermittelt werden.\n\nInternet verfügbar? Openstreetmaps offline?")
        return ""

class Dialog_HTML_Export(QMainWindow, Ui_DialogHtmlExport):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_column_selction_entries()
        self.set_own_location()
        self.pushButton_html_export.clicked.connect(self.html_export)
        self.pushButton_set_own_location.clicked.connect(self.set_own_location)
        self.determine_coordinates_pushButton.clicked.connect(self.get_coordinates)
        self.lineEdit_max_distance.setInputMask("00000;")
        self.lineEdit_max_distance.setText("0")
        self.lineEdit_max_distance.setMaxLength(5)

        self.comboBox_column_selection.currentIndexChanged.connect(self.column_selected)
        self.checkBox_compact_mode.setChecked(True)

    def init_and_show(self):
        self.show()

    def init_column_selction_entries(self) -> None:
        """
        Adds all colmuns to to the column-selcetion-combobox
        :return:
        """
        self.all_columns = ["local_id", "name", "family_name", "street", "zip_code", "city", "country", "company_profession", "coordinates",  "phone", "email", "website", "radius_of_activity",
                       "other_contact", "interests_hobbies", "requests", "skills_offers", "tags", "friend_ids"]

        # keys which should be writen to text in the export
        keys_in_text = []

        all_columns_text = [key_to_text(el, 'business_card').upper() for el in self.all_columns]

        for col in all_columns_text:
            self.comboBox_column_selection.addItem(col)

        if conf.HTML_EXPORT_COLUMN_SELECTION == []:
            conf.HTML_EXPORT_COLUMN_SELECTION = [1 for el in self.all_columns] # 1 means actvive column, 0 unactive
            conf.write()

        for index in range(len(conf.HTML_EXPORT_COLUMN_SELECTION)):
            if conf.HTML_EXPORT_COLUMN_SELECTION[index] == 0:
                itemtext = self.comboBox_column_selection.itemText(index + 1)
                itemtext = "___" + itemtext.lower() + "___"  # mark as inactive (to hide this column)
                self.comboBox_column_selection.setItemText(index + 1, itemtext)


    def column_selected(self) -> None:
        """
        activates / deactivates the columns for showing in table view. deactivated are uses lower chars and
        start with "___" and ends with "___"
        :return:
        """
        selected_index = self.comboBox_column_selection.currentIndex()
        if selected_index == 0: # ignore first column, is only description of the combobox
            return


        itemtext = self.comboBox_column_selection.itemText(selected_index)
        if itemtext.startswith("_"):
            itemtext = itemtext.upper()[3:-3] # mark as acitve
            conf.HTML_EXPORT_COLUMN_SELECTION[selected_index - 1] = 1
        else:
            itemtext = "___" + itemtext.lower() + "___" # mark as inactive (to hide this column)
            conf.HTML_EXPORT_COLUMN_SELECTION[selected_index - 1] = 0
        self.comboBox_column_selection.setItemText(selected_index, itemtext)
        self.comboBox_column_selection.setCurrentIndex(0)
        self.comboBox_column_selection.showPopup() # reopen after click, to more quickly activate / deactivate other col

    def get_coordinates(self):
        coordinates = get_coordinates(self, f"{self.street_lineEdit.text()} {self.zip_code_lineEdit.text()} {self.city_lineEdit.text()} {self.country_lineEdit.text()}")
        if coordinates != "":
            self.coordinates_lineEdit.setText(str(coordinates))

    def set_own_location(self):
        """sets own location from profile settings as place from where the distances of the export is calculated"""
        self.street_lineEdit.setText(conf.PROFILE_SET_STREET)
        self.zip_code_lineEdit.setText(conf.PROFILE_SET_ZIP_CODE)
        self.city_lineEdit.setText(conf.PROFILE_SET_CITY)
        self.country_lineEdit.setText(conf.PROFILE_SET_COUNTRY)
        self.coordinates_lineEdit.setText(conf.PROFILE_SET_COORDINATES)


    def html_export(self):
        """export all cards to html for printing to paper"""
        export_filename = str(QFileDialog.getSaveFileName(self, 'HTML speichern',
                                                          os.path.join(os.getcwd(), conf.EXPORT_FOLDER,
                                                                       f"Angebote.html"),
                                                          filter="*.html")[0])
        if export_filename == "": # if no file selected return
            return
        if not export_filename.endswith('.html'):
            export_filename = export_filename.split(".")[0] + ".html"

        # read out if compact mode (remove line breaks in content)
        compact_mode = self.checkBox_compact_mode.isChecked()
        current_time = str(datetime.now().replace(microsecond=0))
        current_date = str(datetime.now().strftime('%d.%m.%Y'))

        # filter out unselected
        filter_out = []
        for selected_index in range(len(self.all_columns)):
            itemtext = self.comboBox_column_selection.itemText(selected_index + 1)
            if itemtext.startswith("_"):
                filter_out.append(self.all_columns[selected_index])

        #dprint(filter_out)
        # extra-filter types to export (own or not own)
        selected_index = self.comboBox_filter.currentIndex()
        extra_where_filter = ""
        if selected_index == 1: # only own cards
            extra_where_filter = f" and creator = '{crypt.Profile.profile_id}'"
        elif selected_index == 2: # not own cards
            extra_where_filter = f" and creator != '{crypt.Profile.profile_id}'"

        # get all needed cards
        card_ids = localdb.sql_list(f"""SELECT card_id FROM dc_head WHERE 
                deleted = False AND type = 'business_card'  AND valid_until > '{current_time}'{extra_where_filter};""")
        all_cards = [localdb.convert_db_to_dict(card_id, add_hops_info=False) for card_id in card_ids]

        #prepare data for sorting with distance (distance between 2 coordinates)
        for data_card in all_cards:
            data_card['data']['coordinates'] += f";{self.coordinates_lineEdit.text()}"



        # remove hidden datacards
        hidden_cards = localdb.sql_list("SELECT card_id FROM local_card_info WHERE hidden = True;")
        all_cards = [data_card for data_card in all_cards if not (data_card['dc_head']['card_id'] in hidden_cards)]

        # sort list - short distance first
        if functions.isValidCoordinate(conf.PROFILE_SET_COORDINATES):
            all_cards = sorted(all_cards, key=lambda k: functions.geo_distance(k['data']['coordinates'], False))

        # filter max distance
        if int(self.lineEdit_max_distance.text()) != 0:
            all_cards = [card for card in all_cards if functions.geo_distance(card['data']['coordinates'], False)
                         < (int(self.lineEdit_max_distance.text()) + 1)]

        number_of_entrys = len(all_cards)
        infohead = {'number_of_entrys': number_of_entrys, 'zip_code': self.zip_code_lineEdit.text(),
                    'city': self.city_lineEdit.text(), 'coordinates': self.coordinates_lineEdit.text(),
                    'current_date': current_date}

        # generate html file
        html = html_export_head # insert html head
        html += utils.generate_html_export_infohead(infohead)
        for data_card in all_cards:
            # add friends_ids to datacard (to display friendsinfo)
            card_id = data_card['dc_head']['card_id']
            friend_ids = localdb.sql("SELECT friend_ids FROM local_card_info WHERE card_id = ?", (card_id,))[0][0]
            data_card['data']['friend_ids'] = friend_ids

            local_id = localdb.sql("SELECT local_id FROM local_card_info WHERE card_id = ?", (card_id,))[0][0]
            #data_card['data']['local_id'] = local_id
            data_part = {'local_id': local_id}
            #dprint(data_part)
            data_part.update(data_card['data'])
            #dprint(data_part)
            data_card['data'] = data_part
            #dprint(data_card)

            opened_type = data_card['dc_head']['type']
            html += data_card_html_export(data_card, type=opened_type, filter=True, filter_empty=True,
                                          grouping="business_card", own_filter_list=filter_out,
                                          compact_mode=compact_mode)
        html += "</body>\n</html>\n" # insert end of html
        html_file = open(export_filename, "w")
        html_file.write(html)
        html_file.close()

class Dialog_Mail_Import(QMainWindow,Ui_DialogMailImport):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_import.clicked.connect(self.import_mail_text)

    def init_and_show(self):
        self.textEdit_mail_text.setText("")
        self.show()

    def import_mail_text(self):
        data_dict = functions.parse_mail_text(self.textEdit_mail_text.toPlainText())
        if not isinstance(data_dict, dict):
            show_message_box("Import fehlgeschlagen", f"Import nicht erfolgreich. Mailtext vollständig eingefügt?\n{data_dict}")
            return
        dprint(data_dict)
        try:
            dialog_business_card.open_mail_import(data_dict)
        except:
            show_message_box("Fehler", "Import fehlgeschlagen")
        self.close()


class Dialog_Profile_Settings(QMainWindow, Ui_DialogProfileSettings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.determine_coordinates_pushButton.clicked.connect(self.get_coordinates)
        self.save_pushButton.clicked.connect(self.save_settings)
        self.close_pushButton.clicked.connect(self.close)
        self.status_label.setText("")

    def get_coordinates(self):
        coordinates = get_coordinates(self, f"{self.street_lineEdit.text()} {self.zip_code_lineEdit.text()} {self.city_lineEdit.text()} {self.country_lineEdit.text()}")
        if coordinates != "":
            self.coordinates_lineEdit.setText(str(coordinates))
            
    def show_and_init(self):
        #conf.read()
        self.profile_name_lineEdit.setText(conf.PROFILE_SET_PROFILE_NAME)
        self.name_lineEdit.setText(conf.PROFILE_SET_NAME)
        self.family_name_lineEdit.setText(str(conf.PROFILE_SET_FAMILIY_NAME))
        self.radius_of_activity_lineEdit.setText(str(conf.PROFILE_SET_RADIUS_OF_ACTIVITY))
        self.street_lineEdit.setText(str(conf.PROFILE_SET_STREET))
        self.zip_code_lineEdit.setText(str(conf.PROFILE_SET_ZIP_CODE))
        self.city_lineEdit.setText(str(conf.PROFILE_SET_CITY))
        self.country_lineEdit.setText(str(conf.PROFILE_SET_COUNTRY))
        self.coordinates_lineEdit.setText(str(conf.PROFILE_SET_COORDINATES))
        self.company_profession_lineEdit.setText(str(conf.PROFILE_SET_COMPANY_PROFESSION))
        self.phone_lineEdit.setText(str(conf.PROFILE_SET_PHONE))
        self.website_lineEdit.setText(str(conf.PROFILE_SET_WEBSITE))
        self.email_lineEdit.setText(str(conf.PROFILE_SET_EMAIL))
        self.interests_hobbies_lineEdit.setText(str(conf.PROFILE_SET_INTERESTS_HOBBIES))
        self.show()
        
    def save_settings(self):
        #dprint(f"'{str(conf.PROFILE_SET_COORDINATES)}' - '{self.coordinates_lineEdit.text()}'")
        new_local_coordinate = (conf.PROFILE_SET_COORDINATES != self.coordinates_lineEdit.text())

        conf.PROFILE_SET_PROFILE_NAME = self.profile_name_lineEdit.text()
        conf.PROFILE_SET_NAME = self.name_lineEdit.text()
        conf.PROFILE_SET_FAMILIY_NAME = self.family_name_lineEdit.text()
        conf.PROFILE_SET_RADIUS_OF_ACTIVITY = self.radius_of_activity_lineEdit.text()
        conf.PROFILE_SET_STREET = self.street_lineEdit.text()
        conf.PROFILE_SET_ZIP_CODE = self.zip_code_lineEdit.text()
        conf.PROFILE_SET_CITY = self.city_lineEdit.text()
        conf.PROFILE_SET_COUNTRY = self.country_lineEdit.text()
        conf.PROFILE_SET_COORDINATES = self.coordinates_lineEdit.text()
        conf.PROFILE_SET_COMPANY_PROFESSION = self.company_profession_lineEdit.text()
        conf.PROFILE_SET_PHONE = self.phone_lineEdit.text()
        conf.PROFILE_SET_WEBSITE = self.website_lineEdit.text()
        conf.PROFILE_SET_EMAIL = self.email_lineEdit.text()
        conf.PROFILE_SET_INTERESTS_HOBBIES = self.interests_hobbies_lineEdit.text()
        conf.write() #save settings to file
        if new_local_coordinate: # if coordinates changed then recalculate distances of all cards
            self.update_distances()
            localdb.recalculate_local_ids()
            frm_main_window.update_table_view()
        frm_main_window.set_gui_depending_profile_status()


    def update_distances(self):
        # update all distances in database
        card_ids = localdb.sql_list(f"""SELECT card_id FROM dc_head WHERE deleted = False and type != 'publickeys'""")
        localdb.update_distances(card_ids, conf.PROFILE_SET_COORDINATES)


class Dialog_Display_Content(QMainWindow, Ui_DialogDisplayContent):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser.setOpenLinks(False) # prevent loading window in textbroswser
        self.textBrowser.anchorClicked.connect(QtGui.QDesktopServices.openUrl) #open link with system browser / mailer
        # anchorClicked
        self.textBrowser.setOpenExternalLinks(True);
        self.setFixedSize(700, 600) # xied size because at the moment no easy solution found to respond on changing size (qt designer bug)
        self.current_element_id = "" # id of the shown content, can be card_id, friend_id ...
        self.own_element = True # bool to mark if the current content / element is created locally or not (used to decide if cards can deleted or only hidden)
        self.opened_type = "" # stores which type of information is currently displayed (friend, busines_scard, ...)

        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_edit.clicked.connect(self.edit_card_id)
        self.pushButton_delete_hide.clicked.connect(self.delete_card)
        self.checkBox_show_Details.stateChanged.connect(self.show_hide_details)


    def reset_gui(self):
        self.textBrowser.setHtml("")
        self.pushButton_edit.show()
        self.pushButton_delete_hide.show()
        #self.checkBox_show_Details.setChecked(False)

    def show_hide_details(self):
        if self.opened_type == "business_card":
            self.show_card_id(self.current_element_id, window_is_open=True)


    def init_and_show(self):
        self.close() #close if old window is opened
        self.reset_gui()
        self.show()

    def edit_card_id(self):
        if self.opened_type == "friend":
            dialog_add_friendship.show_friend(self.current_element_id, opened_from_content_display=True)
        elif self.opened_type == "business_card":
            dialog_business_card.open_business_card(self.current_element_id, opened_from_content_display=True)

    def delete_card(self):
        if self.opened_type == "friend":
            reply = QMessageBox.question(self, 'Freundschaft wirklich beenden?', 'Soll die Freundschaft wirklich beendet werden??',
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                localdb.sql(f"DELETE FROM friends WHERE pubkey_id = '{self.current_element_id}';")
                dialog_friendship_list.update_friend_list_table_view()
                self.close()

        elif self.opened_type == "business_card":
            if self.own_element:
                reply = QMessageBox.question(self, 'Wirklich löschen?', 'Soll der Eintrag wirklich gelöscht werden?',
                                             QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.Yes: # mark own card as deleted and clear content
                    dialog_business_card.delete_business_card(self.current_element_id)
                    frm_main_window.update_table_view()
                    self.close()

            if not self.own_element: # hide card of other creator (if inappropriate)
                is_hidden_card = (localdb.sql_list("SELECT hidden FROM local_card_info WHERE card_id = ?"
                                                   , (self.current_element_id,))[0] == 1)
                if is_hidden_card:
                    reply = QMessageBox.question(self, 'Wieder einblenden?',
                                                 'Soll der Eintrag wieder angezeigt werden und das Teilen an Freunde wieder ermöglicht werden?',
                                                 QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        localdb.unhide_data_card(self.current_element_id)
                else:
                    reply = QMessageBox.question(self, 'Eintrag ausblenden?',
                                                 'Wirklich ausblenden?\nDer Eintrag wird dann nicht mehr angezeigt '
                                                 'und auch nicht mehr an Freunde geteilt! (Kann Rückgängig gemacht '
                                                 'werden.)',
                                                 QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        localdb.hide_data_card(self.current_element_id)
                frm_main_window.update_table_view()
                self.close()


    def email_to_friends_helper(self) -> None:
        """
        Shows a windows to easily send an e-mail to all friends with the local installed email-app. For example to send
        the latest entries of the database to friends.
        :return:
        """
        self.reset_gui()
        self.pushButton_edit.hide()
        self.pushButton_delete_hide.hide()
        self.checkBox_show_Details.hide()
        self.setWindowTitle("E-Mail an alle Freunde")

        friends_mail_adresses = "%2C".join(localdb.sql_list("SELECT email FROM friends WHERE active_friendship = True"))
        my_mail_address = str(conf.PROFILE_SET_EMAIL)
        mail_subject = "Aktuelle TalentTalent Datenbank"

        # brief description
        htmlcode = """<p>Klicke auf den Link, um dein E-Mail Programm zu &ouml;ffnen und eine Mail an alle deine Freunde 
        zu schreiben, z.B. um die aktuelle Datenbank mit den Eintr&auml;gen zu teilen.</p>"""

        # mail link
        htmlcode += (f"""<p style="text-align: center;"><a href="mailto:{my_mail_address}?bcc={friends_mail_adresses}""" +
                    f"""&subject={mail_subject}"><strong>E-Mail an Freunde</strong></a></p>""")

        self.textBrowser.setHtml(htmlcode)
        self.show()

    def email_to_mailing_list(self) -> None:
        """
        Shows a windows to easily send an e-mail to all cards where user wants to have an e-mail with the local installed email-app. For example to send
        the latest entries of the database to friends.
        :return:
        """
        self.reset_gui()
        self.pushButton_edit.hide()
        self.pushButton_delete_hide.hide()
        self.checkBox_show_Details.hide()
        self.setWindowTitle("E-Mail an Abonnenten vom E-Mail-Verteiler")


        all_mail_adresses = "%2C".join(localdb.sql_list("SELECT DISTINCT mailing_list FROM local_card_info WHERE mailing_list != ''"))
        my_mail_address = str(conf.PROFILE_SET_EMAIL)
        mail_subject = "Rundmail"

        # brief description
        htmlcode = """<p>Klicke auf den Link, um eine Mail an alle 
        Interessenten vom E-Mail-Verteiler zu senden, z.B. um die exportieren Eintr&auml;ge zu versenden. </p> """

        # mail link
        htmlcode += (f"""<p style="text-align: center;"><a href="mailto:{my_mail_address}?bcc={all_mail_adresses}""" +
                    f"""&subject={mail_subject}"><strong>E-Mail an Interessenten vom Mail-Verteiler senden</strong></a></p>""")

        self.textBrowser.setHtml(htmlcode)
        self.show()


    def show_friend(self, pubkey_id, window_is_open=False):
        if not window_is_open:
            self.init_and_show()

        self.checkBox_show_Details.hide() # no detail selection for friends
        self.current_element_id = pubkey_id
        self.opened_type = "friend"
        self.pushButton_delete_hide.setText("Freundschaft beenden")

        friends_info = localdb.sql_dict(f"""SELECT name, email, comment, active_friendship, friend_since_date, expire_date, pubkey_id, publickey  
        FROM friends WHERE pubkey_id = '{pubkey_id}';""")[0]

        window_title = f"Freund: {friends_info['name']}  (ID {str(friends_info['pubkey_id'])[:8]})"
        if friends_info['active_friendship'] == 0:
            window_title += "  - INAKTIVE Freundschaft"
        self.setWindowTitle(window_title)

        html = friend_data_to_html(friends_info, type='friend', filter=True, full_html=True, filter_empty=True)



        self.textBrowser.setHtml(html)
        #self.textBrowser.setText(str(friends_info))


    def show_card_id(self, card_id, window_is_open = False):
        if not window_is_open:
            self.init_and_show()

        self.checkBox_show_Details.show()
        show_details = self.checkBox_show_Details.isChecked()
        self.current_element_id = card_id
        self.setWindowTitle(f"Karten ID: {card_id[:8]}")
        local_creator_id = crypt.Profile.rsa_key_pair_id
        data_card = localdb.convert_db_to_dict(card_id, add_hops_info=False)

        # add friends_ids to datacard (to display friendsinfo)
        friend_ids = localdb.sql("SELECT friend_ids FROM local_card_info WHERE card_id = ?", (card_id, ))[0][0]
        data_card['data']['friend_ids'] = friend_ids

        is_hidden_card = (localdb.sql_list("SELECT hidden FROM local_card_info WHERE card_id = ?", (card_id, ))[0] == 1)
        self.opened_type = data_card['dc_head']['type']

        # adapt coordinates and append own coordinates  (that distance can calculated and be shown)
        if functions.isValidCoordinate(data_card['data']['coordinates']) and functions.isValidCoordinate(conf.PROFILE_SET_COORDINATES):
            data_card['data']['coordinates'] += f";{conf.PROFILE_SET_COORDINATES}"

        html = data_card_to_html(data_card, show_details=show_details, type=self.opened_type, filter=True,
                                 full_html=True, filter_empty=True, grouping="business_card")
        self.textBrowser.setHtml(html)
        # prevent editing of cards that where from friends / not locally created (hide buttons)
        self.own_element = True # to enable deletetion
        if data_card['dc_head']['creator'] != local_creator_id:
            self.own_element = False # to disable deletion, only hiding is possible (prevent showin and sharing to friends)
            self.pushButton_edit.hide()
            if not is_hidden_card:
                self.pushButton_delete_hide.setText("Ausblenden (unangemessen)")
            if is_hidden_card:
                self.pushButton_delete_hide.setText("Wieder einblenden")

        if self.own_element:
            self.pushButton_delete_hide.setText("Löschen")


    def resize_happend(self):
        print("resize")

class Dialog_Profile_Create_Selection(QMainWindow, Ui_Dialog_Profile_Create_Selection):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Kein Profil gefunden")

        self.pushButton_create_new_profile.clicked.connect(self.generate_new_profile)
        self.pushButton_restore_exisitin_profile.clicked.connect(self.restore_profile)

    def generate_new_profile(self):
        self.close()
        dialog_generate_profile.show()

    def restore_profile(self):
        self.close()
        dialog_restore_profile.restore_old_profile()


class Dialog_Restore_Profile(QMainWindow, Ui_DialogRestoreProfile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textEdit_profile_seed_words.textChanged.connect(self.live_word_check)
        self.btn_restore_profile.clicked.connect(self.restore_profile)
        self.correct_seed = ""  # stores the correct seed
        self.complete_restore = True  # if not set, only password restore of exisiting profile with seed words is needed

    def restore_profile(self):
        print("start restore")
        self.close()
        crypt.Profile.rsa_seed_words = self.correct_seed
        crypt.Profile.profile_name = str(self.lineEdit_profile_name.text())
        dialog_generate_profile.close()
        if self.complete_restore:  # no existing file, just recreate the old profile with old seed
            conf.PROFILE_SET_PROFILE_NAME = str(self.lineEdit_profile_name.text())
            conf.write()
            dialog_new_password.init_and_show()
            #frm_main_window.set_gui_depending_profile_status()
            #frm_main_window.update_table_view() # if old database file exists after restore -> show content in gui table
        else:  # password is forgotten -> restore only password of existing profile
            if crypt.seed_is_identic_with_profile_seed():
                dialog_new_password.change_password = True
                conf.PROFILE_SET_PROFILE_NAME = str(self.lineEdit_profile_name.text())
                conf.write()
                dialog_new_password.init_and_show()
                pass
            else:
                show_message_box("Passwort setzten fehlgeschlagen",
                                 "Kein Profil gefunden oder die Schlüsselwörter passen nicht zum Profil!")

    def restore_forgotten_password(self):
        self.complete_restore = False
        self.reset_gui()
        self.setWindowTitle("Profil Passwort wiederherstellen")
        self.btn_restore_profile.setText("Passwort wiederherstellen")
        show_message_box("Schlüsselwörter benötigt", "Um neues Passwort zu vergeben, werden die "
                                                     "korrekten Schlüsselwörter des Profils benötigt. Ohne diese "
                                                     "ist keine Wiederherstellung möglich!")
        self.show()

    def restore_old_profile(self, complete_restore=True):
        self.complete_restore = True
        self.reset_gui()
        self.show()

    def live_word_check(self):
        """catches some errors and displays status information when entering the old seed"""
        if self.correct_seed != "":
            return  # prevent infinite recursion when correct seed is typed
        input = str(self.textEdit_profile_seed_words.toPlainText())
        input = input.rstrip().lstrip().lower()  # remove whitespaces on beginning and end of words
        input = re.sub('\s+', ' ', input).strip()  # remove more than one whitespace

        number_of_words = len(input.split(" "))
        if input == "":
            number_of_words = 0
        wrong_words = ""
        # print(number_of_words)
        self.label_status.setText(f"Noch {12 - number_of_words} Worte.")
        for word in input.split(" "):
            if not functions.is_english_seed_word(word):
                wrong_words += f" {word}"
        if input != "" and wrong_words != "":
            self.label_status.setText(f"Ungültige Wörter: {wrong_words}")
        elif number_of_words < 12:
            self.label_status.setText(f"Noch {12 - number_of_words} Worte.")
        elif number_of_words == 12:
            if crypt.check_word_seed(input):
                self.label_status.setText(f"Alle Schlüsselwörter sind korrekt.")
                self.textEdit_profile_seed_words.setReadOnly(True)
                self.correct_seed = str(input)
                self.textEdit_profile_seed_words.setText(self.correct_seed)
                self.btn_restore_profile.setEnabled(True)
            else:
                self.label_status.setText(f"Diese Schlüsselwörter sind nicht korrekt!")
        else:
            self.label_status.setText(f"Zu viele Wörter.")

    def reset_gui(self):
        """reset the gui / clears old entries"""
        self.setWindowTitle("Profil wiederherstellen")
        self.btn_restore_profile.setText("Profil wiederherstellen")
        self.correct_seed = ""
        self.textEdit_profile_seed_words.setReadOnly(False)
        self.textEdit_profile_seed_words.setText("")
        self.btn_restore_profile.setEnabled(False)


class Dialog_Friendship_list(QMainWindow, Ui_DialogFriendshipList):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Liste der Freunde")
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_close.clicked.connect(self.update_friend_list_table_view)
        self.comboBox_friend_filter.currentIndexChanged.connect(self.update_friend_list_table_view)
        self.pushButton_add_friend.clicked.connect(dialog_add_friendship.init_and_show)

    def init_and_show(self):
        self.comboBox_friend_filter.setCurrentIndex(0) # on window open show active friends (not last selection)
        self.update_friend_list_table_view()
        self.show()

    def update_friend_list_table_view(self):
        """shows / update the current bussincards in the table view"""
        # to disable edit in table, disable edittriggers in qt designer in the table
        friend_list = QtSql.QSqlRelationalTableModel()

        filter_selection = self.comboBox_friend_filter.currentIndex()
        if filter_selection == 0:  # active friends
            where_filter = f"active_friendship = True"
        else:  # non active friends
            where_filter = f"active_friendship = False"

        Qquery = QtSql.QSqlQuery(f"""SELECT pubkey_id AS ID, name AS Name,
                                            email AS EMail, friend_since_date AS [Freund seit], expire_date AS [Ende Freundschaft]
                                            FROM friends WHERE {where_filter};""")  # show
        friend_list.setQuery(Qquery)
        friend_list.select()

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(friend_list)
        self.tableView_friendlist.setModel(self.proxy_model)
        self.tableView_friendlist.setSortingEnabled(True)

        # when click on table show selected card
        self.tableView_friendlist.doubleClicked.connect(self.friendlist_table_click)
        self.friend_ids = ""

    def friendlist_table_click(self, index):
        selected_friend_id = self.proxy_model.data(self.proxy_model.index(index.row(), 0))
        dialog_display_content.show_friend(selected_friend_id)


class Dialog_Add_Friendship(QMainWindow, Ui_DialogFriendship):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_from_content_display = False # when opened from content display it will reload content display on cloase
        self.existing_friend_id = ""
        self.opened_from_content_display = False # remembers if window was opened from existing friend from display_content
        self.pushButton_cancel_friendship.setEnabled(False)
        self.pushButton_add_renew_friendship.setEnabled(False)
        self.label_own_key_expiration.setText("")
        self.label_friend_key_expiration.setText("")

        self.pushButton_add_renew_friendship.clicked.connect(self.add_change_friend)
        self.pushButton_cancel_friendship.clicked.connect(self.add_delete_friendship)
        self.spinBox_friendship_years.textChanged.connect(self.calculate_sharing_key)
        self.pushButton_copy_ownkey_to_clipboard.clicked.connect(self.copy_own_key)
        self.pushButton_extend_friendship.clicked.connect(self.set_gui_for_extend_friendship)
        self.textEdit_friendskey.textChanged.connect(self.check_friends_key)
        self.pushButton_close.clicked.connect(self.close)


    def closeEvent(self, event):

        dialog_friendship_list.update_friend_list_table_view()
        print(f"close {self.opened_from_content_display}")
        if self.opened_from_content_display:
            print("update freund dialog!")
            dialog_display_content.show_friend(self.existing_friend_id, window_is_open=True)
            self.opened_from_content_display = False
        self.reset_gui()
        # print("closed")

    def reset_gui(self):
        """resets gui and variables to standard and removes old content from edits ..."""
        self.setWindowTitle("Freund hinzufügen")
        self.label_friend_key_expiration.setText("")
        self.pushButton_add_renew_friendship.setText("Hinzufügen")
        self.label_friendhip_date_info.setText("")
        self.lineEdit_friends_name.setText("")
        self.lineEdit_friends_email.setText("")
        self.lineEdit_friends_comment.setText("")
        self.textEdit_friendskey.setText("")
        self.textEdit_friendskey.setReadOnly(False)
        self.textEdit_friendskey.setDisabled(False)
        self.pushButton_cancel_friendship.setEnabled(False)
        self.pushButton_extend_friendship.hide()
        self.existing_friend_id = ""
        self.label_own_key.setDisabled(False)
        self.textBrowser_ownkey.setDisabled(False)
        self.spinBox_friendship_years.setDisabled((False))
        self.label_years_of_validity.setDisabled(False)
        self.pushButton_copy_ownkey_to_clipboard.setDisabled(False)
        self.spinBox_friendship_years.setValue(5)
        self.label_help_text.setText("Wähle eine Freundschaftsdauer und sende deinen Schlüssel an den Freund. "
                                     "Trage dann den Schlüssel vom Freund in das untere Feld um die Freundschaft "
                                     "zu bestätigen.")

    def set_gui_for_existing_friend(self, friend_id):
        """prepares the gui when an exisitng friend will be showed"""
        self.textEdit_friendskey.setDisabled(True)
        self.label_enter_friends_key.setDisabled(True)
        self.setWindowTitle(f"Freund bearbeiten  -  ID: {friend_id}")
        self.label_help_text.setText(
            "Hier kannst du Namen, E-Mail und Kommentar des Freundes anpassen und bei Bedarf die Freundschaft verlängern.")
        self.pushButton_extend_friendship.show()
        self.label_friend_key_expiration.setText("")
        self.label_own_key_expiration.setText("")
        self.textEdit_friendskey.setText("")
        self.textBrowser_ownkey.setText("")
        self.pushButton_add_renew_friendship.setText("Speichern")
        self.pushButton_add_renew_friendship.setEnabled(True)
        self.pushButton_cancel_friendship.setEnabled(True)
        self.label_own_key.setDisabled(True)
        self.textBrowser_ownkey.setDisabled(True)
        self.spinBox_friendship_years.setDisabled((True))
        self.label_years_of_validity.setDisabled(True)
        self.pushButton_copy_ownkey_to_clipboard.setDisabled(True)

    def set_gui_for_extend_friendship(self):
        """changes GUI elements that the friendship of an existing friends can be extendend with a new key from friend"""
        self.pushButton_extend_friendship.hide()
        self.textEdit_friendskey.setDisabled(False)
        self.label_enter_friends_key.setDisabled(False)
        self.textEdit_friendskey.setReadOnly(False)
        self.label_help_text.setText(
            f"Neuer Schlüssel vom Freund kann jetzt eingefügt werden um die Freundschaft zu verlängern.")
        self.pushButton_add_renew_friendship.setText("Verlängern")
        self.pushButton_add_renew_friendship.setEnabled(False)
        self.label_own_key.setDisabled(False)
        self.textBrowser_ownkey.setDisabled(False)
        self.spinBox_friendship_years.setDisabled((False))
        self.label_years_of_validity.setDisabled(False)
        self.pushButton_copy_ownkey_to_clipboard.setDisabled(False)
        self.calculate_sharing_key()

    def select_complete_ownkey_text(self):
        self.textBrowser_ownkey.selectAll()

    def copy_own_key(self):
        """copys friendhsip key to clipboard"""
        QApplication.clipboard().setText(self.textBrowser_ownkey.toPlainText())
        self.textBrowser_ownkey.selectAll()

    def init_and_show(self):
        self.reset_gui()
        self.calculate_sharing_key()
        self.show()

    def show_friend(self, existing_friend_id, opened_from_content_display):
        """show the friend in the add friend window and load the friends data"""
        self.reset_gui()

        self.opened_from_content_display = opened_from_content_display
        self.set_gui_for_existing_friend(existing_friend_id)
        self.existing_friend_id = existing_friend_id
        self.show()

        [friends_name, friends_comment, friends_email, old_expire_date, friend_since_date, active_friendship] = localdb.sql(f"""SELECT name, comment, email, expire_date, friend_since_date, active_friendship FROM 
                friends WHERE pubkey_id = '{existing_friend_id}';""")[0]
        self.lineEdit_friends_name.setText(str(friends_name))
        self.lineEdit_friends_comment.setText(str(friends_comment))
        self.lineEdit_friends_email.setText(str(friends_email))
        self.label_friendhip_date_info.setText(
            f"{friends_name} ist Freund seit {friend_since_date} und die Freundschaft läuft bis {old_expire_date}.")
        print("active_friendship:", active_friendship)
        if active_friendship == 0:
            self.label_friendhip_date_info.setText(
                f"Mit {friends_name} ist die Freundschaft nicht mehr aktiv und muss verlängert werden.")

    def add_change_friend(self):
        """adding new friends or extend frienship"""
        friends_name = self.lineEdit_friends_name.text()
        friends_comment = self.lineEdit_friends_comment.text()
        friends_email = str(self.lineEdit_friends_email.text()).replace(" ", "")  # remove spaces from mail
        # if self.existing_friend_id has an id (then friend info is loaded from db an then a small update is possible)
        do_small_update = (self.existing_friend_id != "" and not self.pushButton_extend_friendship.isHidden())

        # Name is needed
        if friends_name.replace(" ", "") == "":
            show_message_box("Namen eingeben", f"""Bitte einen Namen für den Freund eingeben""")
            return False

        # catch wrong emailformat
        if not functions.isValidEmail(friends_email) and friends_email != "":
            show_message_box("Mail Adresse prüfen", f"""Die eingegeben Mailadresse ist ungültig!""")
            return False

        if do_small_update:
            """updates only name, comment and mail of friend"""
            sql_command = (f"""UPDATE friends SET email = ?, comment = ?, name = ? WHERE pubkey_id = ?;""")
            localdb.sql(sql_command, (friends_email, friends_comment, friends_name, self.existing_friend_id))
            self.label_help_text.setText("Änderungen zum Freund gespeichert!")
            self.show_friend(self.existing_friend_id, opened_from_content_display=self.opened_from_content_display)
            return

        if not self.check_friends_key(True):  # if not all conditions are correct, exit
            return False

        my_chosen_expire_date = str(functions.add_years(datetime.date(datetime.now()),
                                                        int(self.spinBox_friendship_years.text())))
        friendskey = self.textEdit_friendskey.toPlainText()
        friendshipinfo = functions.friendship_string_to_dict(friendskey)
        friends_profile_id = str(friendshipinfo['pubkey_id'])
        friends_pubkey = str(friendshipinfo['pubkey'])
        friends_expire_date = str(friendshipinfo['expire_date'])
        friend_since_date = str(datetime.date(datetime.now()))
        friendship_expiration = min(friends_expire_date, my_chosen_expire_date)

        if not localdb.friend_exist(friends_profile_id):
            # add new friend
            sql_command = ("""INSERT INTO friends (email, comment, expire_date, friend_since_date, name,
                                    active_friendship, publickey, pubkey_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""")
            localdb.sql(sql_command,
                        (friends_email, friends_comment, friendship_expiration, friend_since_date, friends_name,
                         True, friends_pubkey, friends_profile_id))
            self.show_friend(friends_profile_id, opened_from_content_display=self.opened_from_content_display)

        else:
            # friend exists -> update
            sql_command = (f"""UPDATE friends SET email = ?, comment = ?, expire_date = ?, name = ?,
                                    active_friendship = ? WHERE pubkey_id = ?;""")
            localdb.sql(sql_command,
                        (friends_email, friends_comment, friendship_expiration, friends_name, True, friends_profile_id))
            self.show_friend(friends_profile_id, opened_from_content_display=self.opened_from_content_display)

        localdb.update_database_friends_info(crypt.Profile.rsa_key_pair_id, crypt.Profile.rsa_key_pair, do_update=True)

    def add_delete_friendship(self):
        """this func is for adding new friend, extend friendFship etc """
        # print("delete friend")
        msgbox = QMessageBox.question(self, "Freundschaft beenden?",
                                      f"""Soll die Freundschaft wirklich beendet werden?""")
        if msgbox == QMessageBox.Yes:
            localdb.sql(f"DELETE FROM friends WHERE pubkey_id = '{self.existing_friend_id}';")
            self.close()
            localdb.update_database_friends_info(crypt.Profile.rsa_key_pair_id, crypt.Profile.rsa_key_pair,
                                                 do_update=True)

    def check_friends_key(self, last_check_before_database_change=False):
        """checks if the pasted key of the friend is correct and enables the button to add the friend"""
        self.pushButton_cancel_friendship.setEnabled(False)
        self.pushButton_add_renew_friendship.setEnabled(False)
        friendskey = self.textEdit_friendskey.toPlainText()

        if not self.pushButton_extend_friendship.isHidden():  # only when key is hidden it needs to be verified
            return

        if len(friendskey) < 300:
            self.label_help_text.setText("Wähle eine Freundschaftsdauer und sende deinen Schlüssel an den Freund. "
                                         "Trage dann den Schlüssel vom Freund in das untere Feld um die Freundschaft "
                                         "zu bestätigen.")
            return False

        try:
            friendshipinfo = functions.friendship_string_to_dict(friendskey)
            friends_profile_id = str(friendshipinfo['pubkey_id'])
            friends_expire_date = str(friendshipinfo['expire_date'])
        except:
            self.label_help_text.setText("Schlüssel ungültig.")
            return False

        self.label_friend_key_expiration.setText(f"Schlüssel gültig bis {friends_expire_date}")
        my_profile_id = str(crypt.Profile.profile_id)
        my_chosen_expire_date = str(functions.add_years(datetime.date(datetime.now()),
                                                        int(self.spinBox_friendship_years.text())))
        friendship_expiration = min(friends_expire_date, my_chosen_expire_date)
        # print(friendshipinfo)
        # print("friendship_expiration", friendship_expiration)

        if my_profile_id == friends_profile_id:  # catch case if own key is copied to to friendskey
            self.label_help_text.setText("Dies ist der eigene Schlüssel. Bitte den Schlüssel vom Freund einfügen.")
            return False

        # when friend ist selected from friendlist - then check if the key ist from the correct friend
        # print(f"check correct friend: {self.existing_friend_id} != \"\" and {self.existing_friend_id} != {friends_profile_id}")
        if self.existing_friend_id != "" and self.existing_friend_id != friends_profile_id:
            self.label_help_text.setText(
                "Dies ein anderer Freund. Bitte einen Schlüssel vom richtigen Freund einfügen!")
            return False

        self.textEdit_friendskey.setReadOnly(True)  # disable change of textedit after valid key is entered
        self.label_friend_key_expiration.setText(f"Schlüssel gültig bis {friends_expire_date}")

        # if friend doesn't exist enable to add the new friend
        if not localdb.friend_exist(friends_profile_id):
            self.label_help_text.setText("Schlüssel ist korrekt! Der neue Freund kann hinzugefügt werden.")
            self.pushButton_add_renew_friendship.setEnabled(True)
            return True

        self.pushButton_add_renew_friendship.setText("Verlängern")
        [friends_name, friends_comment, friends_email, old_expire_date, friend_since_date] = localdb.sql(f"""SELECT name, comment, email, expire_date, friend_since_date FROM 
        friends WHERE pubkey_id = '{friends_profile_id}';""")[0]

        # when emtpty friend fields the fill with db-content
        if not last_check_before_database_change:
            if str(self.lineEdit_friends_name.text()).replace(" ", "") == "":
                self.lineEdit_friends_name.setText(str(friends_name))
            if str(self.lineEdit_friends_comment.text()).replace(" ", "") == "":
                self.lineEdit_friends_comment.setText(str(friends_comment))
            if str(self.lineEdit_friends_email.text()).replace(" ", "") == "":
                self.lineEdit_friends_email.setText(str(friends_email))

        self.label_friendhip_date_info.setText(
            f"Freund seit {friend_since_date} und Freundschaft läuft bis {old_expire_date}.")

        # if new expire of the friend date is not longer, the friendship can't be extended
        if old_expire_date >= friends_expire_date:
            self.label_help_text.setText(
                "Existierender Freund. Freundchaft kann aber nicht verlängert werden. Der Schlüssel vom Freund ist nicht lang genug gültig.  Eventuell neuen Schlüssel schicken lassen.")
            return False

        if old_expire_date >= my_chosen_expire_date:
            self.label_help_text.setText("Existierender Freund. Um zu verlängern oben eine längere Gültigkeit wählen.")
            return False

        self.label_help_text.setText(
            "Existierender Freund. Freundschaft kann mit diesem neuen Schlüssel verlängert werden!")
        self.pushButton_add_renew_friendship.setEnabled(True)
        self.pushButton_add_renew_friendship.setText("Verlängern")
        return True

    def calculate_sharing_key(self):
        """calculates the a sharing-string which is send to friend to get all info which is needed for friendship """

        expire_date = str(functions.add_years(datetime.date(datetime.now()), int(self.spinBox_friendship_years.text())))
        self.label_own_key_expiration.setText(f"Schlüssel gültig bis {expire_date}")
        pupkey = crypt.Profile.pubkey_string
        pubkey_id = crypt.Profile.profile_id
        friendship_info_for_friend = {'pubkey': pupkey, 'pubkey_id': pubkey_id, 'expire_date': expire_date}
        self.textBrowser_ownkey.setText(functions.dict_to_friendship_string(friendship_info_for_friend, 61))


class Dialog_Business_Card(QMainWindow, Ui_DialogBuisinessCard):
    def __init__(self):
        super().__init__()
        self.reload_table_view = False  # Saves whether list of cards in mainwindow needs to be updated
        self.setupUi(self)
        self.opened_from_content_display = False
        self.save_pushButton.clicked.connect(self.save_business_card)
        self.close_pushButton.clicked.connect(self.close_window)
        self.increase_hops_pushButton.clicked.connect(self.increase_hops)
        self.decrease_hops_pushButton.clicked.connect(self.decrease_hops)
        self.determine_coordinates_pushButton.clicked.connect(self.get_coordinates)
        self.adopt_validity_pushButton.clicked.connect(self.adjust_valitidy)
        self.current_card_id = ""
        self.status_label.setText("")  # to display status messages
        # self.checkBox_extend_hops.changeEvent.triggered.connect(self.set_hop_settings)
        self.checkBox_extend_hops.stateChanged.connect(self.set_hop_settings)  # when checkbox change
        self.foreign_card = True
        self.set_hop_settings()  # init status of all hop spinboxes

    def show_and_init(self,foreign_card = True):
        self.set_defaults_businesscard_window()
        self.foreign_card = foreign_card
        self.show()


    def closeEvent(self, event):
        # reload content display
        if self.opened_from_content_display:
            self.opened_from_content_display = False
            #dialog_display_content.close()
            dialog_display_content.show_card_id(self.current_card_id, window_is_open=True)
            #dialog_display_content.

        if self.reload_table_view:  # reload table / list with cards only when nedeed (change / deletion of card)
            self.reload_table_view = False
            frm_main_window.update_table_view()

        self.current_card_id = functions.rand_hex(16) + crypt.Profile.profile_id[:16]
        self.set_defaults_businesscard_window()
        self.save_pushButton.show()
        #self.delete_pushButton.show()

    def adjust_valitidy(self):
        """changes gui for change end of valitidy date of a business card"""
        if self.valid_until_label.isHidden():
            self.valid_until_label.show()
            self.month_valid_spinBox.hide()
            self.month_valid_label.hide()
            self.adopt_validity_pushButton.setText("Gültigkeit ändern")
        else:
            self.valid_until_label.hide()
            self.month_valid_spinBox.show()
            self.month_valid_label.show()
            self.adopt_validity_pushButton.setText("Gültigkeit nicht ändern")

    def set_hop_settings(self):
        """enables or disables individual hop settings on every input when extend-checkbox is checked or unchecked"""
        # print(f"check box checked? {self.checkBox_extend_hops.isChecked()}")
        if self.checkBox_extend_hops.isChecked():
            self.HOPS_image_spinBox.setEnabled(True)
            self.HOPS_name_spinBox.setEnabled(True)
            self.HOPS_family_name_spinBox.setEnabled(True)
            self.HOPS_radius_of_activity_spinBox.setEnabled(True)
            self.HOPS_street_spinBox.setEnabled(True)
            self.HOPS_zip_code_spinBox.setEnabled(True)
            self.HOPS_city_spinBox.setEnabled(True)
            self.HOPS_country_spinBox.setEnabled(True)
            self.HOPS_coordinates_spinBox.setEnabled(True)
            self.HOPS_other_contact_spinBox.setEnabled(True)
            self.HOPS_company_profession_spinBox.setEnabled(True)
            self.HOPS_phone_spinBox.setEnabled(True)
            self.HOPS_website_spinBox.setEnabled(True)
            self.HOPS_email_spinBox.setEnabled(True)
            self.HOPS_interests_hobbies_spinBox.setEnabled(True)
            self.HOPS_skills_offers_spinBox.setEnabled(True)
            self.HOPS_requests_spinBox.setEnabled(True)
            self.HOPS_tags_spinBox.setEnabled(True)
        else:
            self.HOPS_image_spinBox.setEnabled(False)
            self.HOPS_name_spinBox.setEnabled(False)
            self.HOPS_family_name_spinBox.setEnabled(False)
            self.HOPS_radius_of_activity_spinBox.setEnabled(False)
            self.HOPS_street_spinBox.setEnabled(False)
            self.HOPS_zip_code_spinBox.setEnabled(False)
            self.HOPS_city_spinBox.setEnabled(False)
            self.HOPS_country_spinBox.setEnabled(False)
            self.HOPS_coordinates_spinBox.setEnabled(False)
            self.HOPS_other_contact_spinBox.setEnabled(False)
            self.HOPS_company_profession_spinBox.setEnabled(False)
            self.HOPS_phone_spinBox.setEnabled(False)
            self.HOPS_website_spinBox.setEnabled(False)
            self.HOPS_email_spinBox.setEnabled(False)
            self.HOPS_interests_hobbies_spinBox.setEnabled(False)
            self.HOPS_skills_offers_spinBox.setEnabled(False)
            self.HOPS_requests_spinBox.setEnabled(False)
            self.HOPS_tags_spinBox.setEnabled(False)

    def close_window(self):
        self.close()


    def delete_business_card(self, card_id = "", close_window = True) -> None:
        """
        Deletes the content of the datacard. The card will still be shared to friends, that also the card will be
        deleted at friends.
        :param card_id: id of the card which should be deleted
        :param close_window: if true the current window will be closed
        :return: None
        """
        if card_id != "":
            self.current_card_id = card_id

        self.reload_table_view = True
        if localdb.datacard_exist(self.current_card_id):
            #dprint("delted card:", self.current_card_id)
            date_time_now = datetime.now().replace(microsecond=0)
            # card still valid to spread the deleted card in the friends network
            # (so the card content is deleted at friends when they import the card with deleted content)
            valid_until = functions.add_months(date_time_now, 6)
            edited = date_time_now
            card_id = self.current_card_id


            last_friend_export = str(localdb.sql_list(f"SELECT value FROM local_status WHERE status_name = 'last_friend_export';")[0])
            card_creation = str(localdb.sql_list(f"SELECT created FROM dc_head WHERE card_id = '{card_id}';")[0])

            # full remove of card when it wasn't exported to friends (else: only delete content and share deleted content)
            if last_friend_export < card_creation: # card created but no export happend after creation (-> full delete)
                localdb.remove_datacards([card_id])
                localdb.recalculate_local_ids(fast_mode=True)
                return

            # the deleted marked cards have to be shared with the same hops number
            maxhops = int(localdb.sql(f"""SELECT maxhop FROM dc_head WHERE card_id = '{card_id}';""")[0][0])


            # content delete {maxhops}
            sql_command = f"""UPDATE business_card SET image = '', name = '', family_name = '', radius_of_activity = '', 
                        street = '', zip_code = '', city = '', country = '', coordinates = '', other_contact = '', company_profession = '', phone = '', 
                        website = '', email = '', interests_hobbies = '', skills_offers = '', requests = '', tags = '', HOPS_image = {maxhops}, 
                        HOPS_name = {maxhops}, HOPS_family_name = {maxhops}, HOPS_radius_of_activity = {maxhops}, HOPS_street = {maxhops}, HOPS_zip_code = {maxhops}, 
                        HOPS_city = {maxhops}, HOPS_country = {maxhops}, HOPS_coordinates = {maxhops}, HOPS_other_contact = {maxhops}, HOPS_company_profession = {maxhops}, HOPS_phone = {maxhops}, 
                        HOPS_website = {maxhops}, HOPS_email = {maxhops}, HOPS_interests_hobbies = {maxhops}, HOPS_skills_offers = {maxhops}, HOPS_requests = {maxhops}, 
                        HOPS_tags = {maxhops} WHERE card_id = '{card_id}'; """
            localdb.sql(sql_command)

            # head delete
            sql_command = (f"""UPDATE dc_head SET edited = ?, valid_until = ?, maxhop = ?, deleted = 1, version = version + 1
                                         WHERE card_id = '{card_id}';""")
            localdb.sql(sql_command, (edited, valid_until, maxhops))

            # dynamic head update
            number_of_salts = maxhops
            salts = ""
            for i in range(number_of_salts):
                # salts.append(binascii.hexlify(os.urandom(8)).decode())
                if salts == "":
                    salts += (binascii.hexlify(os.urandom(8)).decode())
                else:
                    salts += ("," + binascii.hexlify(os.urandom(8)).decode())

            sql_command = (f"""UPDATE dc_dynamic_head SET salts = ? WHERE card_id = ? ;""")

            localdb.sql(sql_command, (salts, card_id))

            # calc signature
            special_hash = localdb.special_hash_from_sql(card_id).encode("utf-8")
            signature = crypt.sign(special_hash, crypt.Profile.rsa_key_pair).decode("utf-8")

            sql_command = (f"""UPDATE dc_dynamic_head SET signature = ? WHERE card_id = ? ;""")
            localdb.sql(sql_command, (signature, card_id))

            # remove from local_card_info
            localdb.sql(f"DELETE FROM local_card_info WHERE card_id = '{card_id}'")

            # recalculate local ids depending on distance
            localdb.recalculate_local_ids(fast_mode=True)

            if close_window:
                self.close()

    def open_business_card(self, card_id, opened_from_content_display = False):
        # print(self.checkBox_extend_hops.isChecked())
        self.opened_from_content_display = opened_from_content_display # need to reload content display on close
        self.current_card_id = card_id
        self.setWindowTitle(f"Visitenkarte  ID: {self.current_card_id[:8]}")
        local_creator_id = crypt.Profile.rsa_key_pair_id

        self.adopt_validity_pushButton.show()
        self.month_valid_spinBox.hide()
        self.month_valid_label.hide()
        self.valid_until_label.show()
        self.adopt_validity_pushButton.setText("Gültigkeit ändern")

        [image, name, family_name, radius_of_activity, street, zip_code, city, country, coordinates, other_contact, company_profession,
         phone, website, email, interests_hobbies, skills_offers, requests, tags, HOPS_image, DELETED_image, HOPS_name,
         DELETED_name, HOPS_family_name, DELETED_family_name, HOPS_radius_of_activity, DELETED_radius_of_activity,
         HOPS_street, DELETED_street, HOPS_zip_code, DELETED_zip_code, HOPS_city, DELETED_city, HOPS_country,
         DELETED_country, HOPS_coordinates, DELETED_coordinates, DELETED_other_contact, HOPS_other_contact, HOPS_company_profession, DELETED_company_profession,
         HOPS_phone, DELETED_phone, HOPS_website, DELETED_website, HOPS_email, DELETED_email, HOPS_interests_hobbies,
         DELETED_interests_hobbies, HOPS_skills_offers, DELETED_skills_offers, HOPS_requests, DELETED_requests,
         HOPS_tags, DELETED_tags] = localdb.sql(f"""SELECT image, name, family_name, radius_of_activity, street, 
        zip_code, city, country, coordinates, other_contact, company_profession, phone, website, email, interests_hobbies, 
        skills_offers, requests, tags, HOPS_image, DELETED_image, HOPS_name, DELETED_name, HOPS_family_name, 
        DELETED_family_name, HOPS_radius_of_activity, DELETED_radius_of_activity, HOPS_street, DELETED_street, 
        HOPS_zip_code, DELETED_zip_code, HOPS_city, DELETED_city, HOPS_country, DELETED_country, HOPS_coordinates, 
        DELETED_coordinates, DELETED_other_contact, HOPS_other_contact, HOPS_company_profession, DELETED_company_profession, HOPS_phone, DELETED_phone, 
        HOPS_website, DELETED_website, HOPS_email, DELETED_email, HOPS_interests_hobbies, DELETED_interests_hobbies, 
        HOPS_skills_offers, DELETED_skills_offers, HOPS_requests, DELETED_requests, HOPS_tags, DELETED_tags FROM 
        business_card WHERE card_id = '{card_id}';""")[0]


        [card_creator_id, valid_until] = localdb.sql(f"""SELECT creator, valid_until FROM 
                dc_head WHERE card_id = '{card_id}';""")[0]

        # prevent editing of cards that where from friends / not locally created (hide buttons)
        if card_creator_id != local_creator_id:
            self.save_pushButton.hide()
            self.adopt_validity_pushButton.hide()

        valid_until = datetime.strptime(valid_until, "%Y-%m-%d %H:%M:%S")

        self.valid_until_label.setText(f"""Gültig bis {valid_until.strftime("%d.%m.%Y")}""")

        if DELETED_image == '0':
            # todo bild self.image_graphicsView()
            pass
        if DELETED_name == '0':
            self.name_lineEdit.setText(name)
        if DELETED_family_name == '0':
            self.family_name_lineEdit.setText(str(family_name))
        if DELETED_radius_of_activity == '0':
            self.radius_of_activity_lineEdit.setText(str(radius_of_activity))
        if DELETED_street == '0':
            self.street_lineEdit.setText(str(street))
        if DELETED_zip_code == '0':
            self.zip_code_lineEdit.setText(str(zip_code))
        if DELETED_city == '0':
            self.city_lineEdit.setText(str(city))
        if DELETED_country == '0':
            self.country_lineEdit.setText(str(country))
        if DELETED_coordinates == '0':
            self.coordinates_lineEdit.setText(str(coordinates))
        if DELETED_other_contact == '0':
            self.other_contact_lineEdit.setText(str(other_contact))
        if DELETED_company_profession == '0':
            self.company_profession_lineEdit.setText(str(company_profession))
        if DELETED_phone == '0':
            self.phone_lineEdit.setText(str(phone))
        if DELETED_website == '0':
            self.website_lineEdit.setText(str(website))
        if DELETED_email == '0':
            self.email_lineEdit.setText(str(email))
        if DELETED_interests_hobbies == '0':
            self.interests_hobbies_lineEdit.setText(str(interests_hobbies))
        if DELETED_skills_offers == '0':
            self.skills_offers_textEdit.setText(str(skills_offers))
        if DELETED_requests == '0':
            self.requests_textEdit.setText(str(requests))
        if DELETED_tags == '0':
            self.tags_lineEdit.setText(str(tags))
        self.HOPS_image_spinBox.setValue(int(HOPS_image))
        self.HOPS_name_spinBox.setValue(int(HOPS_name))
        self.HOPS_family_name_spinBox.setValue(int(HOPS_family_name))
        self.HOPS_radius_of_activity_spinBox.setValue(int(HOPS_radius_of_activity))
        self.HOPS_street_spinBox.setValue(int(HOPS_street))
        self.HOPS_zip_code_spinBox.setValue(int(HOPS_zip_code))
        self.HOPS_city_spinBox.setValue(int(HOPS_city))
        self.HOPS_country_spinBox.setValue(int(HOPS_country))
        self.HOPS_coordinates_spinBox.setValue(int(HOPS_coordinates))
        self.HOPS_other_contact_spinBox.setValue(int(HOPS_other_contact))
        self.HOPS_company_profession_spinBox.setValue(int(HOPS_company_profession))
        self.HOPS_phone_spinBox.setValue(int(HOPS_phone))
        self.HOPS_website_spinBox.setValue(int(HOPS_website))
        self.HOPS_email_spinBox.setValue(int(HOPS_email))
        self.HOPS_interests_hobbies_spinBox.setValue(int(HOPS_interests_hobbies))
        self.HOPS_skills_offers_spinBox.setValue(int(HOPS_skills_offers))
        self.HOPS_requests_spinBox.setValue(int(HOPS_requests))
        self.HOPS_tags_spinBox.setValue(int(HOPS_tags))

        self.label_range.setText(f"Reichweite: {max(self.hop_list())}")  # update view of max hops

        mailinglist_mail = localdb.sql_list("SELECT mailing_list FROM local_card_info WHERE card_id = ?;", (card_id,))[0]
        if functions.isValidEmail(mailinglist_mail):
            self.checkBox_add_to_mailling_list.setChecked(True)
        else:
            self.checkBox_add_to_mailling_list.setChecked(False)
        self.show()
        
    def open_mail_import(self, card_data, opened_from_content_display = False):
        self.set_defaults_businesscard_window()
        self.opened_from_content_display = opened_from_content_display # need to reload content display on close
        self.setWindowTitle(f"Visitenkarte  ID: {self.current_card_id[:8]}")
        #dprint(card_data)

        self.name_lineEdit.setText(card_data['name'])
        self.family_name_lineEdit.setText(card_data['family_name'])
        self.radius_of_activity_lineEdit.setText(card_data['radius_of_activity'])
        self.street_lineEdit.setText(card_data['street'])
        self.zip_code_lineEdit.setText(card_data['zip_code'])
        self.city_lineEdit.setText(card_data['city'])
        self.country_lineEdit.setText(card_data['country'])
        #self.coordinates_lineEdit.setText(card_data['coordinates'])
        self.other_contact_lineEdit.setText(card_data['other_contact'])
        self.company_profession_lineEdit.setText(card_data['company_profession'])
        self.phone_lineEdit.setText(card_data['phone'])
        self.website_lineEdit.setText(card_data['website'])
        self.email_lineEdit.setText(card_data['email'])
        self.interests_hobbies_lineEdit.setText(card_data['interests_hobbies'])
        self.skills_offers_textEdit.setText(card_data['skills_offers'])
        self.requests_textEdit.setText(card_data['requests'])
        self.tags_lineEdit.setText(card_data['tags'])
        

        self.label_range.setText(f"Reichweite: {max(self.hop_list())}")  # update view of max hops
        self.checkBox_add_to_mailling_list.setChecked(True)
        self.show()

    def save_business_card(self):
        self.reload_table_view = True  # to reload the list of cards when the window is closed
        graphic_codierung_todo = ""  # todo grafik einfügen
        # hops to list - needed to get maximum
        maxhop = int(max(self.hop_list()))
        minhop = int(min(self.hop_list()))

        #catch typos
        # remove whitespaces and only small letters in url
        self.website_lineEdit.setText(str(self.website_lineEdit.text()).strip().lower())

        # check for special case when existing card has now lower hops than the old version of the card
        # then old card needs to be deleted (that card is deleted everywhere) and new card id is needed with less hops)
        if localdb.datacard_exist(self.current_card_id):
            old_max_hop = int(localdb.sql_list("SELECT maxhop FROM dc_head WHERE card_id = ?;",(self.current_card_id, ))[0])
            if maxhop < old_max_hop:
                old_card_id = self.current_card_id
                new_card_id = functions.rand_hex(16) + crypt.Profile.profile_id[:16]
                localdb.duplicate_data_card(old_card_id, new_card_id)
                self.delete_business_card(old_card_id, close_window=False) # delete old card
                self.current_card_id = new_card_id

        if localdb.datacard_exist(self.current_card_id):
            date_time_now = datetime.now().replace(microsecond=0)
            valid_until = functions.add_months(date_time_now, int(self.month_valid_spinBox.text()))
            edited = date_time_now
            card_id = self.current_card_id
            #dprint("existing card:", card_id)
            # update distance val in db
            distance = functions.geo_distance(f"{self.coordinates_lineEdit.text()};{conf.PROFILE_SET_COORDINATES}")
            if distance == "":
                localdb.sql(f"""UPDATE local_card_info SET distance = ? WHERE card_id = ?; """, (functions.adapt_dist(distance, 6), card_id))
            else:
                localdb.sql(f"""UPDATE local_card_info SET distance = ? WHERE card_id = ?; """, (functions.adapt_dist(distance, 6), card_id))

            # head update -
            if self.month_valid_spinBox.isHidden(): # don't change valid_until
                sql_command = (f"""UPDATE dc_head SET deleted = False, edited = ?, maxhop = ?, version = version + 1
                             WHERE card_id = '{card_id}';""")
                localdb.sql(sql_command, (edited, maxhop))
            else: # change valid until
                sql_command = (f"""UPDATE dc_head SET deleted = False, edited = ?, valid_until = ?, maxhop = ?, version = version + 1
                             WHERE card_id = '{card_id}';""")
                localdb.sql(sql_command, (edited, valid_until, maxhop))

            # content update
            sql_command = f"""UPDATE business_card SET image = ?, name = ?, family_name = ?, radius_of_activity = ?, 
            street = ?, zip_code = ?, city = ?, country = ?, coordinates = ?, other_contact = ?, company_profession = ?, phone = ?, 
            website = ?, email = ?, interests_hobbies = ?, skills_offers = ?, requests = ?, tags = ?, HOPS_image = ?, 
            HOPS_name = ?, HOPS_family_name = ?, HOPS_radius_of_activity = ?, HOPS_street = ?, HOPS_zip_code = ?, 
            HOPS_city = ?, HOPS_country = ?, HOPS_coordinates = ?, HOPS_other_contact = ?, HOPS_company_profession = ?, HOPS_phone = ?, 
            HOPS_website = ?, HOPS_email = ?, HOPS_interests_hobbies = ?, HOPS_skills_offers = ?, HOPS_requests = ?, 
            HOPS_tags = ? WHERE card_id = '{card_id}'; """
            localdb.sql(sql_command,
                        (graphic_codierung_todo, self.name_lineEdit.text().strip(),
                         self.family_name_lineEdit.text().strip(),
                         self.radius_of_activity_lineEdit.text().strip(), self.street_lineEdit.text().strip(),
                         self.zip_code_lineEdit.text().strip(),
                         self.city_lineEdit.text().strip(), self.country_lineEdit.text().strip(),
                         self.coordinates_lineEdit.text().strip(), self.other_contact_lineEdit.text().strip(),
                         self.company_profession_lineEdit.text().strip(), self.phone_lineEdit.text().strip(),
                         self.website_lineEdit.text().strip(),
                         self.email_lineEdit.text().strip(), self.interests_hobbies_lineEdit.text().strip(),
                         self.skills_offers_textEdit.toPlainText().strip(),
                         self.requests_textEdit.toPlainText().strip(),
                         self.tags_lineEdit.text(), self.HOPS_image_spinBox.text(),
                         self.HOPS_name_spinBox.text(),
                         self.HOPS_family_name_spinBox.text(),
                         self.HOPS_radius_of_activity_spinBox.text(),
                         self.HOPS_street_spinBox.text(), self.HOPS_zip_code_spinBox.text(),
                         self.HOPS_city_spinBox.text(),
                         self.HOPS_country_spinBox.text(), self.HOPS_coordinates_spinBox.text(),
                         self.HOPS_other_contact_spinBox.text(),
                         self.HOPS_company_profession_spinBox.text(), self.HOPS_phone_spinBox.text(),
                         self.HOPS_website_spinBox.text(), self.HOPS_email_spinBox.text(),
                         self.HOPS_interests_hobbies_spinBox.text(),
                         self.HOPS_skills_offers_spinBox.text(),
                         self.HOPS_requests_spinBox.text(), self.HOPS_tags_spinBox.text()))

            # dynamic head update
            number_of_salts = maxhop - minhop + 1
            #generate comma separated salts
            salts = ",".join([binascii.hexlify(os.urandom(8)).decode() for i in range(number_of_salts)])

            sql_command = (f"""UPDATE dc_dynamic_head SET salts = ? WHERE card_id = ? ;""")
            localdb.sql(sql_command, (salts, card_id))

            # calc signature
            special_hash = localdb.special_hash_from_sql(card_id).encode("utf-8")
            signature = crypt.sign(special_hash, crypt.Profile.rsa_key_pair).decode("utf-8")

            sql_command = (f"""UPDATE dc_dynamic_head SET signature = ? WHERE card_id = ? ;""")
            localdb.sql(sql_command, (signature, card_id))

        else:
            # save new business card
            date_time_now = datetime.now().replace(microsecond=0)

            deleted = False
            valid_until = functions.add_months(date_time_now, int(self.month_valid_spinBox.text()))
            edited = date_time_now
            created = date_time_now
            type = "business_card"
            creator = crypt.Profile.rsa_key_pair_id
            card_id = self.current_card_id
            version = 0 # version number of card begins with 0

            #dprint("new datacard", card_id)


            # insert dc_head
            sql_command = (f"""INSERT INTO dc_head ( version, maxhop, deleted, valid_until, edited, created, type, creator, card_id, foreign_card )
                               VALUES ( ? , '{maxhop}', ?, '{valid_until}', '{edited}', '{created}', '{type}', '{creator}', '{card_id}', ? ); """)
            localdb.sql(sql_command, (version, deleted, self.foreign_card))

            # insert distance of card to db
            distance = functions.geo_distance(f"{self.coordinates_lineEdit.text()};{conf.PROFILE_SET_COORDINATES}")
            if distance == "":
                localdb.sql(f"""INSERT INTO local_card_info ( card_id, distance ) VALUES ( ? , ?);""", (card_id, functions.adapt_dist(distance, 6)))
            else:
                localdb.sql(f"INSERT INTO local_card_info ( card_id, distance ) VALUES ( ? , ?);", (card_id, functions.adapt_dist(distance, 6)))

            # insert business card
            sql_command = (f"""INSERT INTO business_card (
                    HOPS_tags, HOPS_requests, HOPS_skills_offers,
                    HOPS_interests_hobbies, HOPS_email, HOPS_website,
                    HOPS_phone, HOPS_company_profession, HOPS_coordinates, HOPS_other_contact,
                    HOPS_country, HOPS_city, HOPS_zip_code,
                    HOPS_street, HOPS_radius_of_activity, HOPS_family_name,
                    HOPS_name, HOPS_image, tags,
                    requests, skills_offers, interests_hobbies,
                    email, website, phone,
                    company_profession, coordinates, other_contact, country,
                    city, zip_code, street,
                    radius_of_activity, family_name, name,
                    image, card_id
                    ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """)
            # todo 'self.image_graphicsView'
            localdb.sql(sql_command, (
                (self.HOPS_tags_spinBox.text(), self.HOPS_requests_spinBox.text(),
                 self.HOPS_skills_offers_spinBox.text(),
                 self.HOPS_interests_hobbies_spinBox.text(), self.HOPS_email_spinBox.text(),
                 self.HOPS_website_spinBox.text(),
                 self.HOPS_phone_spinBox.text(), self.HOPS_company_profession_spinBox.text(),
                 self.HOPS_coordinates_spinBox.text(), self.HOPS_other_contact_spinBox.text(),
                 self.HOPS_country_spinBox.text(), self.HOPS_city_spinBox.text(), self.HOPS_zip_code_spinBox.text(),
                 self.HOPS_street_spinBox.text(), self.HOPS_radius_of_activity_spinBox.text(),
                 self.HOPS_family_name_spinBox.text(),
                 self.HOPS_name_spinBox.text(), self.HOPS_image_spinBox.text(), self.tags_lineEdit.text().strip(),
                 self.requests_textEdit.toPlainText().strip(), self.skills_offers_textEdit.toPlainText().strip(),
                 self.interests_hobbies_lineEdit.text().strip(),
                 self.email_lineEdit.text().strip(), self.website_lineEdit.text().strip(), self.phone_lineEdit.text().strip(),
                 self.company_profession_lineEdit.text().strip(), self.coordinates_lineEdit.text().strip(),
                 self.other_contact_lineEdit.text().strip(), self.country_lineEdit.text().strip(),
                 self.city_lineEdit.text().strip(), self.zip_code_lineEdit.text().strip(), self.street_lineEdit.text().strip(),
                 self.radius_of_activity_lineEdit.text().strip(), self.family_name_lineEdit.text().strip(), self.name_lineEdit.text().strip(),
                 graphic_codierung_todo, card_id)))

            number_of_salts = maxhop - minhop + 1
            # generate comma separated salts
            salts = ",".join([binascii.hexlify(os.urandom(8)).decode() for i in range(number_of_salts)])

            sql_command = (f"""INSERT INTO dc_dynamic_head (
                                            salts, signature, hops, card_id
                                        ) VALUES (
                                            '{salts}',  NULL, 0, '{card_id}'
                                        );""")
            localdb.sql(sql_command)

            # calc signature
            special_hash = localdb.special_hash_from_sql(card_id).encode("utf-8")
            signature = crypt.sign(special_hash, crypt.Profile.rsa_key_pair).decode("utf-8")

            sql_command = f"""UPDATE dc_dynamic_head SET signature = '{signature}' WHERE card_id = '{card_id}';"""
            localdb.sql(sql_command)

            # calc local id, if foreign_card then fast_mode
            localdb.recalculate_local_ids(fast_mode=self.foreign_card)

        # insert / remove mail to mailing list table
        email_address = self.email_lineEdit.text().strip()
        if self.checkBox_add_to_mailling_list.isChecked() and functions.isValidEmail(email_address):
            #dprint("add to mailinglist", email_address)
            localdb.sql(f"UPDATE local_card_info SET mailing_list = ? WHERE card_id = ?;"
                        ,(email_address, card_id))
        if not self.checkBox_add_to_mailling_list.isChecked():
            #dprint("remove from mailinglist", email_address)
            localdb.sql(f"UPDATE local_card_info SET mailing_list = '' WHERE card_id = ?;", (card_id,))
            if functions.isValidEmail(email_address): # maybe also other cards contains the same e-mail, also remove
                localdb.sql(f"UPDATE local_card_info SET mailing_list = '' WHERE mailing_list = ?;", (email_address,))



        # show new date for valid_until
        [valid_until] = localdb.sql(f"""SELECT valid_until FROM 
                        dc_head WHERE card_id = '{card_id}';""")[0]
        valid_until = datetime.strptime(valid_until, "%Y-%m-%d %H:%M:%S")
        self.valid_until_label.setText(f"""Gültig bis {valid_until.strftime("%d.%m.%Y")}""")

        self.setWindowTitle(f"Visitenkarte  ID: {self.current_card_id[:8]}")

        #show validity change button
        self.adopt_validity_pushButton.setText("Gültigkeit ändern")
        self.adopt_validity_pushButton.show()
        self.month_valid_spinBox.hide()
        self.month_valid_label.hide()
        self.valid_until_label.show()


        self.status_label.setText("Visitenkarte erfolgreich gespeichert")
        QTimer.singleShot(4000, lambda: self.status_label.setText(""))

    def set_defaults_businesscard_window(self):
        """clears all fields of the businesscard window and set it to default values"""
        self.current_card_id = functions.rand_hex(16) + crypt.Profile.profile_id[:16]
        self.checkBox_extend_hops.setChecked(False)  # uncheck checkbox
        self.checkBox_add_to_mailling_list.setChecked(False) # default no mailing list
        self.adopt_validity_pushButton.hide()
        self.valid_until_label.hide()
        self.set_hop_settings()
        self.foreign_card = True
        self.setWindowTitle(f"Visitenkarte  ID: {self.current_card_id[:8]}")

        self.name_lineEdit.setText("")
        self.family_name_lineEdit.setText("")
        self.radius_of_activity_lineEdit.setText("")
        self.street_lineEdit.setText("")
        self.zip_code_lineEdit.setText("")
        self.city_lineEdit.setText("")
        self.country_lineEdit.setText("")
        self.coordinates_lineEdit.setText("")
        self.other_contact_lineEdit.setText("")
        self.company_profession_lineEdit.setText("")
        self.phone_lineEdit.setText("")
        self.website_lineEdit.setText("")
        self.email_lineEdit.setText("")
        self.interests_hobbies_lineEdit.setText("")
        self.skills_offers_textEdit.setText("")
        self.requests_textEdit.setText("")
        self.tags_lineEdit.setText("")
        self.HOPS_image_spinBox.setValue(3)
        self.HOPS_name_spinBox.setValue(3)
        self.HOPS_family_name_spinBox.setValue(3)
        self.HOPS_radius_of_activity_spinBox.setValue(3)
        self.HOPS_street_spinBox.setValue(3)
        self.HOPS_zip_code_spinBox.setValue(3)
        self.HOPS_city_spinBox.setValue(3)
        self.HOPS_country_spinBox.setValue(3)
        self.HOPS_coordinates_spinBox.setValue(3)
        self.HOPS_other_contact_spinBox.setValue(3)
        self.HOPS_company_profession_spinBox.setValue(3)
        self.HOPS_phone_spinBox.setValue(3)
        self.HOPS_website_spinBox.setValue(3)
        self.HOPS_email_spinBox.setValue(3)
        self.HOPS_interests_hobbies_spinBox.setValue(3)
        self.HOPS_skills_offers_spinBox.setValue(3)
        self.HOPS_requests_spinBox.setValue(3)
        self.HOPS_tags_spinBox.setValue(3)
        self.label_range.setText(f"Reichweite: {max(self.hop_list())}")  # update view of range label

    def hop_list(self):
        """reurns a list with the values of all hops. to determine for examble the max or min of all hops"""
        hops = [self.HOPS_tags_spinBox.text(), self.HOPS_requests_spinBox.text(),
                self.HOPS_skills_offers_spinBox.text(),
                self.HOPS_interests_hobbies_spinBox.text(), self.HOPS_email_spinBox.text(),
                self.HOPS_website_spinBox.text(),
                self.HOPS_phone_spinBox.text(), self.HOPS_company_profession_spinBox.text(),
                self.HOPS_coordinates_spinBox.text(), self.HOPS_other_contact_spinBox.text(),
                self.HOPS_country_spinBox.text(), self.HOPS_city_spinBox.text(), self.HOPS_zip_code_spinBox.text(),
                self.HOPS_street_spinBox.text(), self.HOPS_radius_of_activity_spinBox.text(),
                self.HOPS_family_name_spinBox.text(),
                self.HOPS_name_spinBox.text(), self.HOPS_image_spinBox.text()]
        return hops

    def increase_hops(self):
        """increases the hoops value of all spinboxes"""

        maxhop = int(max(self.hop_list()))
        if maxhop < 4:
            self.HOPS_image_spinBox.setValue(int(self.HOPS_image_spinBox.text()) + 1)
            self.HOPS_name_spinBox.setValue(int(self.HOPS_name_spinBox.text()) + 1)
            self.HOPS_family_name_spinBox.setValue(int(self.HOPS_family_name_spinBox.text()) + 1)
            self.HOPS_radius_of_activity_spinBox.setValue(int(self.HOPS_radius_of_activity_spinBox.text()) + 1)
            self.HOPS_street_spinBox.setValue(int(self.HOPS_street_spinBox.text()) + 1)
            self.HOPS_zip_code_spinBox.setValue(int(self.HOPS_zip_code_spinBox.text()) + 1)
            self.HOPS_city_spinBox.setValue(int(self.HOPS_city_spinBox.text()) + 1)
            self.HOPS_country_spinBox.setValue(int(self.HOPS_country_spinBox.text()) + 1)
            self.HOPS_coordinates_spinBox.setValue(int(self.HOPS_coordinates_spinBox.text()) + 1)
            self.HOPS_other_contact_spinBox.setValue(int(self.HOPS_other_contact_spinBox.text()) + 1)
            self.HOPS_company_profession_spinBox.setValue(int(self.HOPS_company_profession_spinBox.text()) + 1)
            self.HOPS_phone_spinBox.setValue(int(self.HOPS_phone_spinBox.text()) + 1)
            self.HOPS_website_spinBox.setValue(int(self.HOPS_website_spinBox.text()) + 1)
            self.HOPS_email_spinBox.setValue(int(self.HOPS_email_spinBox.text()) + 1)
            self.HOPS_interests_hobbies_spinBox.setValue(int(self.HOPS_interests_hobbies_spinBox.text()) + 1)
            self.HOPS_skills_offers_spinBox.setValue(int(self.HOPS_skills_offers_spinBox.text()) + 1)
            self.HOPS_requests_spinBox.setValue(int(self.HOPS_requests_spinBox.text()) + 1)
            self.HOPS_tags_spinBox.setValue(int(self.HOPS_tags_spinBox.text()) + 1)
            self.label_range.setText(f"Reichweite: {max(self.hop_list())}")  # update view of max hops label

    def decrease_hops(self):
        """decreases the hoops value of all spinboxes"""
        minhop = int(min(self.hop_list()))

        if minhop > 0:
            self.HOPS_image_spinBox.setValue(int(self.HOPS_image_spinBox.text()) - 1)
            self.HOPS_name_spinBox.setValue(int(self.HOPS_name_spinBox.text()) - 1)
            self.HOPS_family_name_spinBox.setValue(int(self.HOPS_family_name_spinBox.text()) - 1)
            self.HOPS_radius_of_activity_spinBox.setValue(int(self.HOPS_radius_of_activity_spinBox.text()) - 1)
            self.HOPS_street_spinBox.setValue(int(self.HOPS_street_spinBox.text()) - 1)
            self.HOPS_zip_code_spinBox.setValue(int(self.HOPS_zip_code_spinBox.text()) - 1)
            self.HOPS_city_spinBox.setValue(int(self.HOPS_city_spinBox.text()) - 1)
            self.HOPS_country_spinBox.setValue(int(self.HOPS_country_spinBox.text()) - 1)
            self.HOPS_coordinates_spinBox.setValue(int(self.HOPS_coordinates_spinBox.text()) - 1)
            self.HOPS_other_contact_spinBox.setValue(int(self.HOPS_other_contact_spinBox.text()) - 1)
            self.HOPS_company_profession_spinBox.setValue(int(self.HOPS_company_profession_spinBox.text()) - 1)
            self.HOPS_phone_spinBox.setValue(int(self.HOPS_phone_spinBox.text()) - 1)
            self.HOPS_website_spinBox.setValue(int(self.HOPS_website_spinBox.text()) - 1)
            self.HOPS_email_spinBox.setValue(int(self.HOPS_email_spinBox.text()) - 1)
            self.HOPS_interests_hobbies_spinBox.setValue(int(self.HOPS_interests_hobbies_spinBox.text()) - 1)
            self.HOPS_skills_offers_spinBox.setValue(int(self.HOPS_skills_offers_spinBox.text()) - 1)
            self.HOPS_requests_spinBox.setValue(int(self.HOPS_requests_spinBox.text()) - 1)
            self.HOPS_tags_spinBox.setValue(int(self.HOPS_tags_spinBox.text()) - 1)
            self.label_range.setText(f"Reichweite: {max(self.hop_list())}")  # update view of range label

    def get_coordinates(self):
        coordinates = get_coordinates(self, f"{self.street_lineEdit.text()} {self.zip_code_lineEdit.text()} {self.city_lineEdit.text()} {self.country_lineEdit.text()}")
        if coordinates != "":
            self.coordinates_lineEdit.setText(str(coordinates))


class Ui_DialogEnterImportPassword(QMainWindow, Ui_DialogEnterImportPassword):
    """shows a small gui to import a database where a password is need (usually when no friendship was made)"""

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_OK.clicked.connect(self.start_import_with_password)
        self.lineEdit_entered_password.setFocus()  # cursor beim start in lineedit

    def start_import_with_password(self):
        import_password = str(self.lineEdit_entered_password.text())
        self.lineEdit_entered_password.setText("")
        frm_main_window.import_database(import_password)
        # frm_main_window.reload_table_view()
        self.close()


class Dialog_Enter_Password(QMainWindow, Ui_DialogEnterPassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.wrong_passwort_counter = 0
        self.pushButton_OK.clicked.connect(self.check_password)
        self.lineEdit_entered_password.returnPressed.connect(self.check_password)
        self.change_existing_password = False
        self.show_seed_words = False

    def init_and_show(self):
        self.lineEdit_entered_password.setText("")
        self.change_existing_password = False
        self.show_seed_words = False
        self.show()

    def check_password(self):
        entered_password = self.lineEdit_entered_password.text()
        entered_password_hash = crypt.hash_string(entered_password, crypt.Profile.user_pw_salt)
        password_correct = (entered_password_hash == crypt.Profile.user_pw_hash)
        #dprint("hashes:", entered_password_hash, crypt.Profile.user_pw_hash)

        if password_correct:
            self.lineEdit_entered_password.setText("")
            self.close()  # close password window
            if self.change_existing_password:
                dialog_new_password.change_password = True
                # dialog_new_password.label
                dialog_new_password.init_and_show()
                self.change_existing_password = False
                return

            if self.show_seed_words:
                self.show_seed_words = False
                seed_words = crypt.aes_decrypt(crypt.Profile.aes_encrypted_seed_words,
                                                               crypt.Profile.aes_key).decode("utf-8")
                #dprint(crypt.Profile.aes_encrypted_seed_words, seed_words)
                show_message_box("Schlüsselwörter zum Profil", f"Die Schlüsselwörter zum Profil lauten:\n{seed_words}")

                return

            crypt.init_profile(entered_password)
            frm_main_window.statusbar.showMessage("Passwort korrekt. Profil erfolgreich geladen.", timeout=10000)

            localdb.password = crypt.Profile.database_key
            localdb.init_password(conf.ENCRYPT_LOCAL_DATABASE)

            #add own pubkey to db, necessary when only db-file was deleted and not profile
            rsa_keypair = crypt.Profile.rsa_key_pair
            localdb.add_own_public_key_to_database(crypt.Profile.rsa_key_pair_id,
                                                   crypt.rsapubkey_to_rsapukeystring(
                                                       crypt.Profile.rsa_key_pair.public_key()), rsa_keypair)

            localdb.update_database_friends_info(crypt.Profile.rsa_key_pair_id, rsa_keypair)

            # start clean database (remove old cards etc., disable expired friendship)
            if not localdb.clean_database(crypt.Profile.profile_id, check_system_time=True):
                show_message_box("Wichtig!",
                                 """Die richtige Systemzeit ist wichtig. Bei falscher Zeit kann es passieren das die Einträge aus """
                                 """der Datenbank gelöscht werden!""")
                msgbox = QMessageBox.question(self, "Bitte System Datum / Zeit prüfen!",
                                              f"""Ist die Uhrzeit / Datum auf dem PC korrekt?""")
                if msgbox == QMessageBox.Yes:
                    localdb.clean_database(crypt.Profile.profile_id, check_system_time=False)



            frm_main_window.set_gui_depending_profile_status()  # if necessary change window title
            frm_main_window.update_table_view()  # show current table

            frm_main_window.tableView.setColumnWidth(0, 10)
            if conf.GUI_COLUMN_SELECTION[0] == 0:
                frm_main_window.tableView.hideColumn(0)


        if not password_correct:
            if self.wrong_passwort_counter < 3:
                self.wrong_passwort_counter += 1
                show_message_box("Fehler", "Passwort ist falsch!")
                self.lineEdit_entered_password.setText("")
            else:
                show_message_box("Fehler", "Passwort ist falsch!")
                show_message_box("Hinweis", "Passwort kann unter Profil zurück gesetzt werden.")
                self.close()

    def change_password(self):
        """called when user wants to change the password"""
        self.lineEdit_entered_password.setText("")
        self.label_enter_password.setText("Aktuelles (altes) Passwort eingeben:")
        self.change_existing_password = True
        self.show_seed_words = False
        self.show()


    def show_seed(self):
        """called when user wants to see the seed words"""
        self.lineEdit_entered_password.setText("")
        self.label_enter_password.setText("Aktuelles Passwort eingeben:")
        self.change_existing_password = False
        self.show_seed_words = True
        self.show()




class Dialog_New_Password(QMainWindow, Ui_DialogNewPassword):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_save_password.clicked.connect(self.save_password)
        self.lineEdit_new_password_retyped.returnPressed.connect(self.save_password)
        self.change_password = False

    def init_and_show(self):
        self.pushButton_save_password.setText("Passwort speichern")
        self.pushButton_save_password.setEnabled(True)
        self.show()


    def save_password(self):
        new_password = self.lineEdit_new_password.text()
        retyped_password = self.lineEdit_new_password_retyped.text()
        if len(new_password) < 8:
            show_message_box("Fehler", "Passwort muss min. 8 Zeichen lang sein.")
            return

        if new_password != retyped_password:
            show_message_box("Fehler", "Passwörter stimmen nicht überein!")
            return

        self.pushButton_save_password.setText("Moment ...")
        self.pushButton_save_password.setEnabled(False)
        QApplication.processEvents()  # update gui instantly to see button changes to inform user

        if self.change_password:
            crypt.Profile.old_aes_key = crypt.Profile.aes_key  # save old aes key
            crypt.Profile.aes_key = ""  # remove old key for new key (derived from  new password)
            crypt.Profile.user_pw_hash = crypt.hash_string(new_password, crypt.Profile.user_pw_salt)
            self.change_password = False

        # print("seed und pw\n", crypt.Profile.rsa_key_word_seeds[0], "\n", crypt.Profile.user_pw)
        profile_filename = os.path.join(os.getcwd(), conf.PROGRAMM_FOLDER, "profile.dat")
        crypt.save_profile(profile_filename, new_password)
        crypt.init_profile(new_password)  # instantly init Pofile that all profile variables are set
        localdb.password = crypt.Profile.database_key
        localdb.init_password(conf.ENCRYPT_LOCAL_DATABASE)  # db neu anlegen bzw. initialisieren

        rsa_keypair = crypt.Profile.rsa_key_pair
        localdb.add_own_public_key_to_database(crypt.Profile.rsa_key_pair_id,
                                               crypt.rsapubkey_to_rsapukeystring(
                                                crypt.Profile.rsa_key_pair.public_key()), rsa_keypair)
        dialog_new_password.close()
        frm_main_window.set_gui_depending_profile_status()
        frm_main_window.update_table_view()
        show_message_box("Passwort geändert", "Passwort erfolgreich geändert!")

    def closeEvent(self, event):
        """set gui to default on close"""
        self.lineEdit_new_password.setText("")
        self.lineEdit_new_password_retyped.setText("")


class Dialog_Generate_Profile(QMainWindow, Ui_DialogGenerateProfile):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.textBrowser_new_seed.setText(crypt.generate_word_seed())
        self.btn_new_seed_words.clicked.connect(self.generate_new_word_seed)
        self.btn_create_profile.clicked.connect(self.create_profile)
        # crypt.save_profile()

    def generate_new_word_seed(self):
        # seed = crypt.generate_word_seed(self)
        self.textBrowser_new_seed.setText(crypt.generate_word_seed())
        # print(seed)

    def create_profile(self):
        seed = self.textBrowser_new_seed.toPlainText()
        retyped_seed = self.textEdit_new_seed_confirmed.toPlainText()
        profile_name = str(self.lineEdit_profile_name.text())
        # ignore spaces when compare
        if seed.replace(" ", "") == retyped_seed.replace(" ", ""):
            # seed correct retyped
            crypt.Profile.rsa_seed_words = seed
            conf.PROFILE_SET_PROFILE_NAME = profile_name
            conf.write()
            dialog_generate_profile.close()
            dialog_new_password.init_and_show()
            frm_main_window.set_gui_depending_profile_status()
        else:
            # print("schlüsselwörter falsch")
            show_message_box("Fehler!", "Schlüsselwörter stimmen nicht überein. Bitte prüfen!")


class Frm_Mainwin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_column_selction_entries()

        # database actions
        self.pushButton_add_businesscard.clicked.connect(self.show_business_card)  # button
        self.pushButton_add_own_businesscard.clicked.connect(self.own_business_card) # button
        self.actionAdd_BusinessCard.triggered.connect(self.show_business_card)  # menu Klick -> FUnktion ausführen

        # profile actions
        self.actionLogIn.triggered.connect(self.profile_login)  # menu login
        self.actionLogOut.triggered.connect(self.log_out)  # menu logout
        self.actionGenerate_Profile.triggered.connect(dialog_generate_profile.show)
        self.actionForgotPassword.triggered.connect(dialog_restore_profile.restore_forgotten_password)  # menu
        self.actionRestoreProfile.triggered.connect(dialog_restore_profile.restore_old_profile)  # menu
        self.actionChangePassword.triggered.connect(dialog_enter_password.change_password)
        self.actionShowSeedWords.triggered.connect(dialog_enter_password.show_seed) # show seed words
        self.actionProfilSettings.triggered.connect(dialog_profile_settings.show_and_init)

        # friendship actions
        self.actionAddFriendship.triggered.connect(self.show_add_friendship)  # menu add friend
        self.actionFriendshipList.triggered.connect(self.show_friendship_list)  # menu - show all friends
        self.actionEMail_to_friends.triggered.connect(dialog_display_content.email_to_friends_helper)

        # import export actions
        self.action_import_database_from_friends.triggered.connect(self.import_database)
        self.action_import_database_with_password.triggered.connect(self.import_database_with_password)
        self.action_generate_database_for_friends.triggered.connect(self.export_database)
        self.action_generate_database_with_password.triggered.connect(self.export_database_with_password)
        self.actionHTML_Export.triggered.connect(dialog_html_export.init_and_show)

        # other actions
        self.actionCleanDatabase.triggered.connect(self.clean_database)
        self.actionExit.triggered.connect(self.exit_app)
        self.lineEdit_filter.textChanged.connect(self.update_table_view)
        self.comboBox_filter.currentIndexChanged.connect(self.update_table_view)
        self.tableView.doubleClicked.connect(self.table_click)
        self.action_mailinglist.triggered.connect(dialog_display_content.email_to_mailing_list)
        self.action_mail_import.triggered.connect(dialog_mail_import.init_and_show)

        self.comboBox_column_selection.currentIndexChanged.connect(self.column_selected)


        #for testing
        #self.actiontest.triggered.connect(self.file_dialog)
        #self.com
        #self.mousePressEvent(self.mousepressed)

    def init_column_selction_entries(self) -> None:
        """
        Adds all colmuns to to the column-selcetion-combobox
        :return:
        """
        all_columns = ['NR.', 'Freunde','NAME', 'TELEFON', 'E-MAIL', 'WWW', 'PLZ', 'ORT', 'ENTFERNUNG', 'ANGEBOT',
                       'INTERESSEN', 'GESUCH', 'STICHWÖRTER', 'GÜLTIGKEIT']
        for col in all_columns:
            self.comboBox_column_selection.addItem(col)

        if conf.GUI_COLUMN_SELECTION == []:
            conf.GUI_COLUMN_SELECTION = [1 for el in all_columns] # 1 means actvive column, 0 unactive
            conf.write()

        for index in range(len(conf.GUI_COLUMN_SELECTION)):
            if conf.GUI_COLUMN_SELECTION[index] == 0:
                itemtext = self.comboBox_column_selection.itemText(index + 1)
                itemtext = "___" + itemtext.lower() + "___"  # mark as inactive (to hide this column)
                self.comboBox_column_selection.setItemText(index + 1, itemtext)
                self.tableView.hideColumn(0)


    def column_selected(self) -> None:
        """
        activates / deactivates the columns for showing in table view. deactivated are uses lower chars and
        start with "___" and ends with "___"
        :return:
        """
        selected_index = self.comboBox_column_selection.currentIndex()
        if selected_index == 0: # ignore first column, is only description of the combobox
            return


        itemtext = self.comboBox_column_selection.itemText(selected_index)
        if itemtext.startswith("_"):
            itemtext = itemtext.upper()[3:-3] # mark as acitve
            conf.GUI_COLUMN_SELECTION[selected_index - 1] = 1
        else:
            itemtext = "___" + itemtext.lower() + "___" # mark as inactive (to hide this column)
            conf.GUI_COLUMN_SELECTION[selected_index - 1] = 0
        self.comboBox_column_selection.setItemText(selected_index, itemtext)
        self.comboBox_column_selection.setCurrentIndex(0)
        self.comboBox_column_selection.showPopup() # reopen after click, to more quickly activate / deactivate other col
        self.update_table_view()


    def exit_app(self):
        """exits the app"""
        self.log_out()
        self.close()




    def clean_database(self):
        profile_id = crypt.Profile.rsa_key_pair_id
        localdb.clean_database(profile_id, check_system_time=False)
        self.update_table_view()

    def log_out(self):
        if crypt.Profile.profile_is_initialized:
            localdb.save_and_close_database(conf.ENCRYPT_LOCAL_DATABASE)
            crypt.close_profile()
            self.set_gui_depending_profile_status()
            self.tableView.setModel(None)  # clears the table
            print("logged out")

    def show_friendship_list(self):
        dialog_friendship_list.init_and_show()

    def show_add_friendship(self):
        dialog_add_friendship.init_and_show()
        pass

    def update_table_view(self):
        """shows / update the current bussincards in the table view"""

        date_time_now = str(datetime.now().replace(microsecond=0))

        #delted and expired cards does't have to filtered here
        # in complete_table are only not deleted cards and expired cards would be filtered at startup

        filter_selection = self.comboBox_filter.currentIndex()
        if filter_selection == 0: # all cards
            where_filter = f"hidden = 0 and valid_until > '{date_time_now}'"
        elif filter_selection == 1: # only own cards
            where_filter = f"creator = '{crypt.Profile.profile_id}'"
        elif filter_selection == 2: # not own cards
            where_filter = f"hidden = 0 and creator != '{crypt.Profile.profile_id}'"
        elif filter_selection == 3: # own expired cards
            where_filter = f"creator == '{crypt.Profile.profile_id}' and valid_until < '{date_time_now}'"
        elif filter_selection == 4: # hidden cards
            where_filter = "hidden = 1"

        # colum selection is also done over a combobox, but selection is save in config,
        # first column ist ID column, hide when not wanted
        # still be searched with proxy filter (improvement?), ID is need when clicked on table to get ID in function table_click
        self.tableView.showColumn(0)
        if conf.GUI_COLUMN_SELECTION[0] == 0:
            self.tableView.hideColumn(0) # hide ID when not selected

        column_selection = "local_id AS [NR.], "
        columns = [ ("friend_ids as Freunde", conf.GUI_COLUMN_SELECTION[1]),
                   ("(name || ' ' || family_name) AS Name", conf.GUI_COLUMN_SELECTION[2]),
                   ("phone as Telefon", conf.GUI_COLUMN_SELECTION[3]),
                   ("email as [E-Mail]", conf.GUI_COLUMN_SELECTION[4]),
                   ("website AS www", conf.GUI_COLUMN_SELECTION[5]),
                   ("zip_code AS PLZ", conf.GUI_COLUMN_SELECTION[6]),
                   ("city AS Ort", conf.GUI_COLUMN_SELECTION[7]),
                   ("distance AS [Entfernung]", conf.GUI_COLUMN_SELECTION[8]),
                   ("skills_offers AS Angebot", conf.GUI_COLUMN_SELECTION[9]),
                   ("interests_hobbies AS [Interessen]", conf.GUI_COLUMN_SELECTION[10]),
                   ("requests AS Gesuch", conf.GUI_COLUMN_SELECTION[11]),
                   ("tags AS Stichwörter", conf.GUI_COLUMN_SELECTION[12]),
                   ("valid_until AS Gültigkeit", conf.GUI_COLUMN_SELECTION[13])
                   ]

        # filter the columns based on the value in conf.GUI_COLUMN_SELECTION
        selected_columns = [col[0] for col in columns if col[1] == 1]

        # join the selected columns using join() function
        column_selection += ", ".join(selected_columns)

        table_view_model = QtSql.QSqlRelationalTableModel()
        # card id has to be the first column, needed for table_click func (will only be hidden when column not selected)
        Qquery = QtSql.QSqlQuery(f"""SELECT {column_selection} FROM complete_table WHERE {where_filter};""")
        table_view_model.setQuery(Qquery)
        table_view_model.select()
        number_of_all_items = table_view_model.rowCount()

        filtertext = self.lineEdit_filter.text()
        def build_filter_models(filtertext, model):
            """
            build multiple proxy filter models in a row to have a logical AND when multiple words are typed as filtertext
            :param filtertext:
            :param model:
            :return:
            """
            # Remove multiple whitespaces
            filtertext = re.sub(r'\s+', ' ', filtertext)

            # Create the initial proxy model
            proxy_model = QSortFilterProxyModel()
            proxy_model.setSourceModel(model)
            for word in filtertext.split(" "):
                new_model = QSortFilterProxyModel()
                new_model.setSourceModel(proxy_model)
                new_model.setFilterKeyColumn(-1)  # -1 for all columns
                new_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
                new_model.setFilterWildcard(word)
                proxy_model = new_model
            return proxy_model

        self.proxy_model = build_filter_models(filtertext, table_view_model)
        number_of_filtered_items = self.proxy_model.rowCount()
        self.tableView.setModel(self.proxy_model)
        self.tableView.verticalHeader().setVisible(False) # hide index column
        self.tableView.setSortingEnabled(True)

        # show number of items
        if number_of_filtered_items == number_of_all_items:
            if number_of_all_items == 1:
                self.label_statistics.setText(f"{number_of_all_items} Eintrag")
            else:
                self.label_statistics.setText(f"{number_of_all_items} Einträge")
        else:
            if number_of_all_items == 1:
                self.label_statistics.setText(f"{number_of_filtered_items} von {number_of_all_items} Eintrag")
            else:
                self.label_statistics.setText(f"{number_of_filtered_items} von {number_of_all_items} Einträgen")


    def table_click(self, index):
        """determines the card id an opens the window gui """

        selected_local_id = self.proxy_model.data(self.proxy_model.index(index.row(), 0))
        selected_card_id = localdb.sql(f"SELECT card_id FROM local_card_info WHERE local_id = {selected_local_id};")[0][0]
        dialog_display_content.show_card_id(selected_card_id)

    def set_gui_depending_profile_status(self):
        """changes the gui depending on whether the profile exists and is active or inactive."""

        # helpers for better readability
        profile_exists = crypt.Profile.profile_exist
        profile_initialized = crypt.Profile.profile_is_initialized

        profile_name = conf.PROFILE_SET_PROFILE_NAME
        window_title = f"{__title__}  v{__version__}"
        if profile_initialized:
            short_profile_id = str(crypt.Profile.rsa_key_pair_id[:8])

        def hide(object): #helper
            object.setVisible(False)

        def show(object):
            object.setVisible(True)

        def disable(object):
            object.setEnabled(False)

        def enable(object):
            object.setEnabled(True)

        #changings of GUI
        if profile_initialized:
            hide(self.actionGenerate_Profile)
            hide(self.actionRestoreProfile)
            hide(self.actionGenerate_Profile)
            hide(self.actionRestoreProfile)
            hide(self.actionLogIn)
            hide(self.actionForgotPassword)
            show(self.actionProfilSettings)
            show(self.actionLogOut)
            show(self.actionChangePassword)
            show(self.actionShowSeedWords)
            show(self.actionCleanDatabase)
            enable(self.menuFriends)
            enable(self.menuExtended)
            enable(self.actionAdd_BusinessCard)
            enable(self.pushButton_add_businesscard)
            enable(self.pushButton_add_own_businesscard)
            enable(self.comboBox_column_selection)
            enable(self.comboBox_filter)
            enable(self.lineEdit_filter)
            self.setWindowTitle(f"""{window_title}  -  Profil: {profile_name} (ID: {short_profile_id})""")

        if profile_exists and not profile_initialized:
            hide(self.actionGenerate_Profile)
            hide(self.actionRestoreProfile)
            hide(self.actionProfilSettings)
            hide(self.actionForgotPassword)
            hide(self.actionShowSeedWords)
            hide(self.actionLogOut)
            hide(self.actionChangePassword)
            hide(self.actionCleanDatabase)
            show(self.actionForgotPassword)
            show(self.actionLogIn)
            disable(self.menuFriends)
            disable(self.menuExtended)
            disable(self.actionAdd_BusinessCard)
            disable(self.pushButton_add_businesscard)
            disable(self.pushButton_add_own_businesscard)
            disable(self.comboBox_column_selection)
            disable(self.comboBox_filter)
            disable(self.lineEdit_filter)
            self.setWindowTitle(f"{window_title}  -  Profil nicht geladen")
            self.label_statistics.setText("")

        if not profile_exists:
            show(self.actionGenerate_Profile)
            show(self.actionRestoreProfile)
            hide(self.actionProfilSettings)
            hide(self.actionForgotPassword)
            hide(self.actionChangePassword)
            hide(self.actionShowSeedWords)
            hide(self.actionLogIn)
            hide(self.actionLogOut)
            hide(self.actionCleanDatabase)

            disable(self.menuFriends)
            disable(self.menuExtended)
            disable(self.actionAdd_BusinessCard)
            disable(self.pushButton_add_businesscard)
            disable(self.pushButton_add_own_businesscard)
            disable(self.comboBox_column_selection)
            disable(self.comboBox_filter)
            disable(self.lineEdit_filter)
            self.setWindowTitle(f"{window_title} - (Kein Profil gefunden)")
            self.label_statistics.setText("")


    def import_database_with_password(self):
        dialog_enter_import_password.show()

    def export_database_with_password(self):
        password = str(functions.PWGen(10))
        show_message_box("Datenbank Passwort",
                         f"""Damit der Empfänger die Datenbank importieren kann benötigt dieser folgendes Passwort:\n\n{password}\n""")
        self.export_database(password)

    def export_database(self, export_password=False):
        """
        exports database to a file which can send to friends that they can import collected ads / businesscards etc
        :return:
        """

        friends_are_exiting = (1 == localdb.sql(f"""SELECT EXISTS 
        ( SELECT pubkey_id FROM friends WHERE active_friendship = True);""")[0][0])
        if export_password == False and not friends_are_exiting:
            show_message_box("Keine Freunde", "Es gibt keine Freunde an die exportiert werden kann.")
            return

        # update data_card with friends_info (that friends know my friends)
        localdb.update_database_friends_info(crypt.Profile.rsa_key_pair_id, crypt.Profile.rsa_key_pair, do_update=True)

        export_filename = str(QFileDialog.getSaveFileName(self, 'Datenbank speichern',
                                                          os.path.join(os.getcwd(), conf.EXPORT_FOLDER,
                                       f"{crypt.Profile.rsa_key_pair_id[:8]}_talents.fdb"), filter="*.fdb")[0])
        if export_filename == "":
            return
        if not export_filename.endswith('.fdb'):
            export_filename = export_filename.split(".")[0] + ".fdb"

        current_time = str(datetime.now().replace(microsecond=0))
        localdb.sql(f"""UPDATE local_status SET value = ? WHERE status_name = 'last_friend_export'; """,
                    (current_time,)) # write last export time to database


        # export cards, but not when to much hops or expired
        card_ids = localdb.sql_list(f"""SELECT dc_head.card_id FROM (dc_dynamic_head INNER JOIN dc_head ON
                      dc_head.card_id = dc_dynamic_head.card_id) WHERE dc_head.maxhop > dc_dynamic_head.hops 
                      AND dc_head.valid_until > '{current_time}'""")

        hidden_card_ids = localdb.sql_list(f"""SELECT card_id FROM local_card_info WHERE hidden = 1;""")


        card_ids = list(set(card_ids) - set(hidden_card_ids)) # remove hidden card_ids, not allowed to share (unappropiate)
        #dprint(card_ids)

        # all creators of data_cards (publickeys data_cards are ignored) - needed to filter out not need public keys
        cards_creators = localdb.sql("""SELECT dc_head.creator FROM (dc_dynamic_head INNER JOIN 
        dc_head ON dc_head.card_id = dc_dynamic_head.card_id) WHERE dc_head.deleted = False and dc_head.maxhop > 
        dc_dynamic_head.hops and dc_head.type != 'publickeys'""")
        needed_publickey_ids = [creator[0] for creator in cards_creators]
        # needed_publickey_ids = []
        # for creator in cards_creators:
        #     needed_publickey_ids.append(creator[0])

        # read all cards from db and store it in dict-format (format for export to frieds etc)
        temp_allcards = [localdb.convert_db_to_dict(id, True) for id in card_ids]

        # temp_allcards = []
        # for id in card_ids:
        #     temp_allcards.append(localdb.convert_db_to_dict(id, True))  #

        # filter out not need pubkeys (friends does not need them to verify signature)
        allcards = [card for card in temp_allcards if not (card['dc_head']['type'] == "publickeys" and card['dc_head']['creator'] not in needed_publickey_ids)]

        # allcards = []
        # for card in temp_allcards:
        #     if not (card['dc_head']['type'] == "publickeys" and card['dc_head']['creator'] not in needed_publickey_ids):
        #         allcards.append(card)

        if len(allcards) == 0:  # if nochting to export end function
            frm_main_window.statusbar.showMessage(f"Datenbank ist leer. Nichts zum teilen!", timeout=10000)
            return

        public_keys_of_friends = []

        # be my own friend that self import is possible
        public_keys_of_friends.append(crypt.Profile.rsa_key_pair.public_key().exportKey())  # add with byteformat

        for pkey in localdb.sql("SELECT publickey FROM friends WHERE active_friendship = True;"):
            public_keys_of_friends.append(crypt.rsapubkeystring_to_rsapubkey(pkey[0]).exportKey())

        hybrid_encrypted = crypt.hybrdid_encryption(allcards, public_keys_of_friends, export_password)

        functions.save_var_to_file(hybrid_encrypted, export_filename)
        frm_main_window.statusbar.showMessage(f"Datei unter {export_filename} gespeichert.", timeout=10000)

    def import_database(self, import_password=False):
        ownpupkeyid = crypt.Profile.rsa_key_pair_id
        date_time_now = datetime.now().replace(microsecond=0)
        new_imported_cardids = [] # stores new card_ids
        updated_cardids = [] # stores updated card_ids

        def signature_is_correct(data_card, pubkeys_dict):
            needed_pubkey_id = data_card['dc_head']['creator']
            if needed_pubkey_id in pubkeys_dict.keys():
                rsa_pupkey = crypt.rsapubkeystring_to_rsapubkey(
                    pubkeys_dict[needed_pubkey_id])  # convert key to needed rsa-format
            else:
                warnings.warn("Signature could not be verified. Pupblic Key Missing!")
                return False
            signature = data_card['dc_dynamic_head']['signature']
            return crypt.sign_is_correct(functions.special_hash_from_dict(data_card).encode("utf8"), signature,
                                         rsa_pupkey)

        # collect all needed information from existing cards in the database
        pubkeys = localdb.sql_tuble_to_dict(localdb.sql("SELECT pubkey_id, publickey FROM publickeys;"))
        existing_card_hops = localdb.sql_tuble_to_dict(localdb.sql(f"""SELECT card_id, hops FROM dc_dynamic_head;"""))
        existing_card_creator = localdb.sql_tuble_to_dict(localdb.sql(f"""SELECT card_id, creator FROM dc_head;"""))
        #existing_card_edited_date = localdb.sql_tuble_to_dict(localdb.sql(f"""SELECT card_id, edited FROM dc_head;"""))
        existing_card_version_number = localdb.sql_tuble_to_dict(localdb.sql(f"""SELECT card_id, version FROM dc_head;"""))
        existing_card_ids = [item[0] for item in
                             localdb.sql(f"SELECT card_id FROM dc_head;")]  # list of all existing card_ids


        #check for files in input folder
        files = [file for file in os.listdir(conf.IMPORT_FOLDER) if file.endswith('fdb')]
        files_from_import_folder = True
        if len(files) == 0: # open select file dialog when import folder empty
            files = [QFileDialog.getOpenFileName(self, 'Datei öffnen', conf.IMPORT_FOLDER, filter="*.fdb")[0]]
            files_from_import_folder = False

        for file in files:
            if not file.endswith('.fdb'):
                continue # catch when no file selected on file open dialog

            if files_from_import_folder:
                file_path = os.path.join(os.getcwd(), conf.IMPORT_FOLDER, file)
            else:
                file_path = file
            encrypted_file = functions.load_var_from_file(file_path)
            new_data_dict = crypt.hybrdid_decryption(encrypted_file, crypt.Profile.rsa_key_pair,
                                                     import_password)

            if new_data_dict == False:  # decryption fails -> next file
                show_message_box("Import fehlgeschlagen", f"""Der Import folgender Datei ist fehlgeschlagen.
                Falsches Passwort oder die Datei ist nicht von einem Freund.\n{file}""")
                if files_from_import_folder: # move files to subfolder to keep import folder clean
                    os.replace(file_path, os.path.join(os.getcwd(), conf.IMPORT_FAILED_SUBFOLDER, os.path.basename(file_path)))
                continue

            # first check and import temporary new pubkeys need for check of signature
            for new_data_card in new_data_dict:
                #print("pukey check ID", new_data_card['dc_head']['card_id'], new_data_card['dc_head']['type'])
                if new_data_card['dc_head']['type'] == "publickeys":  # if pubkey
                    print("pubkey:", new_data_card['data']['pubkey_id'][0])
                    if not new_data_card['data']['pubkey_id'][0] in pubkeys.keys():
                        new_pubkey_id = new_data_card['data']['pubkey_id'][0]
                        new_pubkey = new_data_card['data']['publickey'][0]
                        pubkeys[new_pubkey_id] = new_pubkey
                        # ic(f"new pub key with id: {new_pubkey_id}")
                        if not signature_is_correct(new_data_card, pubkeys):
                            # remove from pubkeys if not correct
                            pubkeys.pop[new_pubkey_id]  # removethis wrong pubkey  from pubkeys
                            log.info(f"signature of new pubkey {new_pubkey_id} was not correct")

            # now import the datacards
            for new_data_card in new_data_dict:
                # ic(new_data_card)
                new_card_id = new_data_card['dc_head']['card_id']
                new_edited = new_data_card['dc_head']['edited']  # date and time of last edit
                new_version_number = new_data_card['dc_head']['version']  # version number of new card
                new_hops = new_data_card['dc_dynamic_head']['hops']  # hops counter of the new card
                new_marked_as_deleted = (new_data_card['dc_head']['deleted'] == 1)  # marker if card is deleted
                own_created_card = (new_data_card['dc_head']['creator'] == ownpupkeyid)

                # prevent manipulated card_ids (the last 16 signs of an card_id always are the first 16 signs of creator_id
                # so the last 16 signs of the card_id can't be faked, so it is impossible to inject cards with same card_id
                # to enforce card_id collisions (only for security reasons, very unlikely case in a friend to friend network)
                if new_card_id[-16:] != new_data_card['dc_head']['creator'][:16] and \
                        new_data_card['dc_head']['type'] != "publickeys": # pupkeys id is a special case (don't check it)
                    continue

                # FILTER OUT CARDS from future
                if new_edited > str(date_time_now + timedelta(days=1)):
                    continue  # next card (ignore when edited time is more than one day in the future, to ignore timezones)

                # Friends can act as backup for own created cards. (when local db gets lost) but only when hops >= 2
                # because friend won't share back ow cards with hops = 1 (friend is not allowed to do)
                if own_created_card and signature_is_correct(new_data_card, pubkeys):
                    new_data_card['dc_dynamic_head']['hops'] = 0
                    all_hops = [item[1][1] for item in new_data_card['data'].items()]
                    number_of_salts = max(all_hops) - min(all_hops) + 1
                    # new_salts needed later after import of own cards
                    new_salts = ",".join([binascii.hexlify(os.urandom(8)).decode() for i in range(number_of_salts)])

                card_exists = (new_card_id in existing_card_ids)

                # if imported card not exists & signature ist correct, import the new card
                if not card_exists:
                    #print(f"card {new_card_id} does not exists")
                    if new_marked_as_deleted:  # cards which are not in local db an marked as deleted are not needed
                        continue
                    if signature_is_correct(new_data_card, pubkeys):
                        localdb.import_new_datacard(new_data_card)
                        if own_created_card: # update salts and signature
                            sql_command = (f"""UPDATE dc_dynamic_head SET salts = ? WHERE card_id = ? ;""")
                            localdb.sql(sql_command, (new_salts, new_card_id))
                            special_hash = localdb.special_hash_from_sql(new_card_id).encode("utf-8")
                            signature = crypt.sign(special_hash, crypt.Profile.rsa_key_pair).decode("utf-8")
                            sql_command = (f"""UPDATE dc_dynamic_head SET signature = ? WHERE card_id = ? ;""")
                            localdb.sql(sql_command, (signature, new_card_id))
                            print(f"Restored own card: {new_card_id}")
                        if new_data_card['dc_head']['type'] != "publickeys":
                            new_imported_cardids.append(new_card_id) # count (but not publickeys)

                    else:
                        log.info(f"Wrong card signature. New card {new_card_id} not imported!")

                if card_exists:  # 3 cases when cards exists - newler version, same Version, older version
                    print(f"card {new_card_id} exists")

                    # if version is older than ignore and check next card
                    if new_version_number < existing_card_version_number[new_card_id]:  # FILTER OUT CARD
                        print(f"Card {new_card_id} too old. Card not updated.")
                        continue  # next card

                    # if new card newer than the existing card in the local db. -> update this card
                    if new_version_number > existing_card_version_number[new_card_id]:
                        print(f"card {new_card_id} is newer -> update")
                        if signature_is_correct(new_data_card, pubkeys):  # check signature
                            localdb.import_update_existing_datacard(new_data_card)
                            updated_cardids.append(new_card_id)
                            if own_created_card:
                                sql_command = (f"""UPDATE dc_dynamic_head SET salts = ? WHERE card_id = ? ;""")
                                localdb.sql(sql_command, (new_salts, new_card_id))
                                special_hash = localdb.special_hash_from_sql(new_card_id).encode("utf-8")
                                signature = crypt.sign(special_hash, crypt.Profile.rsa_key_pair).decode("utf-8")
                                sql_command = (f"""UPDATE dc_dynamic_head SET signature = ? WHERE card_id = ? ;""")
                                localdb.sql(sql_command, (signature, new_card_id))
                                print(f"Restored newer version of own card: {new_card_id}")
                        else:
                            log.info(f"Wrong card signature. Existing card {new_card_id} not updated!")
                        continue  # next card

                    # if new card has the same version
                    if new_version_number == existing_card_version_number[new_card_id]:
                        print(f"card {new_card_id} is equal")
                        # update if cards hops is lower then in the existing card (to update hop counter)
                        # that shows that the card has come over a new shorter way (probably  new friendship) than before
                        if new_hops < existing_card_hops[new_card_id]:
                            if signature_is_correct(new_data_card, pubkeys):  # check signature
                                localdb.import_update_existing_datacard(new_data_card)
                            else:
                                log.info(f"Wrong card signature ({new_card_id}). Card hops not updated!")
                        continue  # next card


            frm_main_window.statusbar.showMessage(f"{file_path} erfolgreich importiert.", timeout=10000)

        if files_from_import_folder:  # move files to subfolder to keep import folder clean
            os.replace(file_path, os.path.join(os.getcwd(), conf.IMPORT_DONE_SUBFOLDER, os.path.basename(file_path)))

        # claculated distances of new and updated cards
        localdb.update_distances( new_imported_cardids + updated_cardids, conf.PROFILE_SET_COORDINATES)
        if len(new_imported_cardids) > 0:
            localdb.recalculate_local_ids() # recalc new local_ids
        frm_main_window.update_table_view()
        frm_main_window.statusbar.showMessage(f"{len(new_imported_cardids)} neue Einträge und {len(updated_cardids)} aktuallisierte Einträge erfolgreich importiert.", timeout=20000)


    def profile_login(self):
        """
        used to login on profile. if no profile exists prompt to create / restore profile
        """
        # check if profile exists and try to load profile
        profile_filename = os.path.join(os.getcwd(), conf.PROGRAMM_FOLDER, "profile.dat")
        profile_exist = os.path.isfile(profile_filename)  # checks if the file exists in app folder
        if profile_exist:
            crypt.Profile.profile_exist = True
            crypt.load_profile_dat(profile_filename)
            self.set_gui_depending_profile_status()
            dialog_enter_password.init_and_show()
        else:
            # no profile exists
            self.set_gui_depending_profile_status()
            dialog_profile_create_selection.show()

    def show_business_card(self):
        dialog_business_card.show_and_init()

    def own_business_card(self):
        # todo what happend when own card is created an old own card is reimported from friends (after db delteion)
                # then there will be two own businesscards in db!
        creator = crypt.Profile.rsa_key_pair_id
        own_card_id = localdb.sql_list(f"""SELECT card_id FROM dc_head WHERE type = 'business_card' AND foreign_card = 0 
                                        AND deleted = 0 AND creator = '{creator}';""")
        if len(own_card_id) == 0: # no own card exists
            dialog_business_card.show_and_init(foreign_card=False)
        if len(own_card_id) == 1:
            dialog_display_content.show_card_id(own_card_id[0])


    def show_dialog_generate_profile(self):
        dialog_profile_create_selection.show()
        # dialog_new_password.show()



app = QApplication()

# prepared translation possibility
translator = QTranslator()
# language file needs to be added in pyinstaller (or spec file for pyinstaller)
translator.load("talent_de.qm", functions.resource_path("translations"))
app.installTranslator(translator)

dialog_html_export = Dialog_HTML_Export()
dialog_mail_import = Dialog_Mail_Import()
dialog_generate_profile = Dialog_Generate_Profile()
dialog_restore_profile = Dialog_Restore_Profile()
dialog_new_password = Dialog_New_Password()
dialog_enter_password = Dialog_Enter_Password()
dialog_enter_import_password = Ui_DialogEnterImportPassword()
dialog_business_card = Dialog_Business_Card()
dialog_add_friendship = Dialog_Add_Friendship()
dialog_friendship_list = Dialog_Friendship_list()
dialog_profile_create_selection = Dialog_Profile_Create_Selection()
dialog_display_content = Dialog_Display_Content()
dialog_profile_settings = Dialog_Profile_Settings()

db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(localdb.db_file)


frm_main_window = Frm_Mainwin()
frm_main_window.show()
frm_main_window.profile_login()

# app.setStyle('Fusion')
app.exec()

if crypt.Profile.profile_is_initialized:  # save only when profile was initialized correctly with password
    localdb.save_and_close_database(conf.ENCRYPT_LOCAL_DATABASE) # close db
    conf.write() # save config on close