# benötige funktionen / Klassen
import ast
import calendar
import inspect
import random
import zlib
from math import sqrt
import binascii
# import datetime
import pickle, os, json
import sqlite3
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
import base64
# from os import getcwd
import gzip, os, re
from Crypto.Hash import SHA256
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy import distance as geopydist

import ntplib

def dprint(*args):
    """debugprint with file and linelumber from where it is called"""
    frame = inspect.stack()[1]
    _, filename = os.path.split(frame[1])
    print (f"{filename}:{frame[2]}", *args)

def parse_mail_text(text: str) -> dict:
    """
    parse the mail text from the webform for import
    """
    occur = [m.start() for m in re.finditer('<card_type>', text)]
    if len(occur) != 2:  # element must occur 2 times, else there is an error
        return "<card_type> nicht gefunden"# card type not found
    card_type = text[(occur[0] + len('<card_type>')):occur[1]].replace('/>', '>')  # in php > is escape by /
    #dprint("card_type=", card_type)
    if not card_type == 'business_card':
        return f"Unbekannter card_type: {card_type}" # if not business_card exit

    content_dict = {'card_type': '', 'name': '', 'family_name': '', 'street': '', 'zip_code': '', 'city': '',
                    'country': '', 'radius_of_activity': '', 'company_profession': '', 'phone': '', 'website': '',
                    'email': '', 'other_contact': '', 'interests_hobbies': '', 'skills_offers': '', 'requests': '',
                    'tags': ''}

    content_elements = re.findall(r"<[a-z_]+>", text) # find all content_elements
    elements = [i for n, i in enumerate(content_elements) if i not in content_elements[:n]] # remove duplicates & keep order

    for el in elements:
        occur =[m.start() for m in re.finditer(el, text)]
        if len(occur) != 2: # element must occur 2 times, else there is an error
            continue
        elementtext = text[(occur[0] + len(el)):occur[1]].replace('/>','>') # in php > is escape by /
        content_dict[el[1:-1]] = elementtext
    return content_dict

def adapt_dist(string, length = 6):
    """takes the dist and adds whitespace and unit. needed for sorting in gui table that uknown distance is at the end"""
    if len(string) == 0:
        return " ?"
    spaces = ' ' * (length - len(string))
    return spaces + string + ' km'

def get_coordinates(location):
    """ Determines the coordinates for a searched location with the help of openstreetmaps

    :param location: searched location e.g. "berlin"
    :return:
    """
    geolocator = Nominatim(user_agent="TalentTalent")
    try:
        result = geolocator.geocode(location)
        found_address = result.address
        coordinates = f"""{round(result.latitude, 2)}, {round(result.longitude, 2)}"""
        return True, found_address, coordinates
    except:
        return False, 0, 0

def geo_distance(two_coordinates, string_mode = True):
    """calculates distance between two coordinates

    :param two_coordinates: string with coordinates eparated by semicolon  like: '53.1, 10.5;52.1, 13.3'
    :return: string with distance in kilometers or empty string on error
    """
    if len(two_coordinates.split(";")) != 2:
        if string_mode:
            return ""
        else:
            return 999999
    if isValidCoordinate(two_coordinates.split(";")[0]) and isValidCoordinate(two_coordinates.split(";")[1]):
        point_A = (two_coordinates.split(";")[0])
        point_B = (two_coordinates.split(";")[1])
        if string_mode:
            return str(round(geopydist.distance(point_A, point_B).kilometers, 0)).split(".")[0]
        else:
            return round(geopydist.distance(point_A, point_B).kilometers, 1)
    else:
        if string_mode:
            return ""
        else:
            return 999999


def system_clock_ntp_difference():
    """returns the time diff in seconds between local time an ntp (time-server) time.

    :return: time diff in seconds, returns 0 at error (time server connection failed)
    """
    time_server = '0.pool.ntp.org'
    ntp = ntplib.NTPClient()
    try:
        ntpResponse = ntp.request(time_server, timeout=2)
    except:
        return 0
    if (ntpResponse):
      now = float(datetime.now().strftime('%s'))
      diff = now-ntpResponse.tx_time
      return round(float(diff), 6)

    return 0

def format_date_string(datestring) -> str:
    """ format the database date time format to to an ordinary format

    :param datestring: date in form: "2020-12-18  17:11:09"   or  "2020-12-18"
    :return: formatet date, for example:  "18.12.2020 17:11:09"
    """
    newdatestring = str(datestring).strip() # leading and trailing whitespace removed
    # check format of string ("2020-12-18  17:11:09"   or  "2020-12-18")
    if re.fullmatch(r'([0-9]{4}(-[0-9]{2}){2}( [0-9]{2}(:[0-9]{2}){2}){0,1})', newdatestring):
        if newdatestring.find(" ") > 7: # long format with time
            dt = datetime.strptime(newdatestring, "%Y-%m-%d %H:%M:%S")
            return dt.strftime('%d.%m.%Y %H:%M:%S')
            #print(dt.strftime('%d.%m.%Y, %H:%M:%S'))
        else: # shot format, only date, no time
            dt = datetime.strptime(newdatestring, "%Y-%m-%d")
            return dt.strftime('%d.%m.%Y')
    return datestring # on error return don't format string

def dict_to_friendship_string(dictionary, linelen=64):
    """Converts a dictionary  with friendship information like pubkey ect. into a string which can send to friend"""
    if isinstance(dictionary, dict):
        byte = json.dumps(dictionary).encode('utf-8')
    else:
        pass  # fehlermeldung
    byte = zlib.compress(byte)
    base32 = base64.b32encode(byte)  # base64.b64encode(byte)
    bstring = base32.decode("utf8")

    # fill with 890 that all lines will have same length, 089 easy can filtered out because not in base32-set
    random.seed(str(dictionary))  # use seed the the fill will always be the same
    while len(bstring) % linelen != 0:
        rand = random.randrange(len(bstring))
        bstring = bstring[:rand] + '089'[random.randrange(3)] + bstring[rand:]
    # insert newline after linelen
    bstring = "".join(bstring[i:i + linelen] + "\n" for i in range(0, len(bstring), linelen))
    return str(bstring)


def friendship_string_to_dict(string):
    """Converts friendship string back to the dict with friendship information. like pubkey etc."""
    # remove non base32 chars (for litle failure tolerance of wrong user input)
    base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567="
    for char in string:
        if char not in base32chars:
            string = string.replace(char, "")
    encoded = string.encode("utf8")
    decoded = base64.b32decode(encoded)
    try:
        decompressed = zlib.decompress(decoded)
    except:
        raise Exception("checksum mismatch")
    decoded_dict = json.loads(decompressed.decode('utf-8'))
    return decoded_dict


def PWGen(pwlength=10, alphabet=''):
    if alphabet == "":
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"  # without I and O preventing miss
    mypw = ""
    for i in range(pwlength):
        index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[index]
    return mypw


def isValidEmail(email):
    # mthis regexp match not exact rfc mail format, but will catch a lot of errors
    if re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
        return True
    return False


def isValidCoordinate(string) -> bool:
    """
    this regexp check if string is a coordinate (ex: "50.98, 11.03"(
    :param string:
    :return:
    """
    if re.fullmatch(r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$', string):
        return True
    return False


def short_SHA256(msg, length=16):
    return SHA256.new(msg.encode("utf8")).hexdigest()[:length]


def special_hash_from_dict(data_card):
    # todo beschreibung einfügen
    # order of content can be ignored (hash of elements are sorted)

    hash_list = []
    # calc hash from header
    header = data_card['dc_head']
    temp_hash_list = []
    for element in header:
        temp_hash_list.append(short_SHA256(str(header[element])))
    temp_hash_list.sort()  # when sorted the order of the elements in the header can be ignored


    header_string = ""
    for element in temp_hash_list:
        header_string += element
    header_string += str(data_card['dc_dynamic_head']['salts'][-1])  # + salt

    hash_list.append(short_SHA256(header_string))

    content = data_card['data']
    max_hop = data_card['dc_head']['maxhop']
    current_hop = max_hop
    for salt in reversed(data_card['dc_dynamic_head']['salts']):
        for element in content:
            if content[element][1] == current_hop:
                if (content[element][2] == '0'):  # if not deleted calc hash
                    temp_string = str(content[element][0]) + str(content[element][1]) + str(salt)

                    hash_list.append(short_SHA256(temp_string))  # gekürzer sha256 reicht
                else:  # else hash is saved in content
                    # when deleted hash is in deleted
                    hash_list.append(content[element][2])
        current_hop -= 1

    hash_list.sort()  # when sorted the order of the elements in the header can be ignored

    temp_string = ""
    for element in hash_list:
        temp_string += element
    specialhash = SHA256.new(temp_string.encode("utf8")).hexdigest()

    return specialhash


def add_months(time: timedelta, number_of_months: int) -> timedelta:
    """ Add a given number of months to a timedelta object.
    If the day of the resulting date is out of range for the new month (e.g. the 31st of a month with only 30 days),
    the day is set to the last day of the month.

    :param time: The timedelta object to add months to.
    :param number_of_months: The number of months to add. Must be a positive integer.
    :return: The resulting timedelta object.
    """
    if not isinstance(number_of_months, int) or number_of_months < 1:
        raise ValueError("number_of_months must be a positive integer")

    year, month = divmod(time.month - 1 + number_of_months, 12)
    newyear = time.year + year
    newmonth = month + 1
    last_day_of_month = calendar.monthrange(newyear, newmonth)[1]
    newday = min(time.day, last_day_of_month)
    return time.replace(year=newyear, month=newmonth, day=newday)

def add_years(time, number_of_years):
    """add a years to a """
    newtime = time
    for year in range(number_of_years):
        newtime += timedelta(days=365)
        if newtime.day != time.day:  # leap year +1 day
            newtime += timedelta(days=1)
    return newtime


def str_to_date(datestring):
    """
    converts a datestring in to datetime object.
    :param date_string: string in this both '2020-12-18 15:11:09' or '2020-12-18'
    :return: datatime object
    """
    if not re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{1,2}:[0-9]{2}:[0-9]{2}$", datestring) == None:
        format = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S")
    if not re.search("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", datestring) == None:
        return datetime.strptime(datestring, "%Y-%m-%d")
    raise Exception("datestring has wrong format:", datestring)


def save_in_json(filename, data):
    with open(filename, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, indent=1, sort_keys=True, ensure_ascii=False)


def load_from_json(filename):
    with open(filename, encoding='utf8') as json_data_file:
        data = json.load(json_data_file)
    return data

#todo codeimproving: func also in cryptofunctions
def sign(msg, keyPair):
    # Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
    hash = SHA256.new(msg)
    signer = PKCS115_SigScheme(keyPair)
    signature = signer.sign(hash)
    return binascii.hexlify(signature)

class config():

    def __init__(self, filename='config.json'):
        # temporäre globale variablen / Einstellungen, die nicht Datei gespeichert werden
        self.TEMP_STARTUP_PASSWORD = ""
        self.PROGRAMM_FOLDER = 'TalentData'  # Verzeichnis wo Daten gespeichert werden
        self.EXPORT_FOLDER = 'TalentExport'  # folder where data is exported
        self.IMPORT_FOLDER = 'TalentImport'  # folder from where data is imported
        self.IMPORT_DONE_SUBFOLDER = os.path.join(self.IMPORT_FOLDER, 'importiert')  # imported files
        self.IMPORT_FAILED_SUBFOLDER = os.path.join(self.IMPORT_FOLDER, 'import_fehlgeschlagen')  # failed import-files


        self.ENCRYPT_LOCAL_DATABASE = False  # Set if local DB should be stored encryped


        if not os.path.exists(os.path.join(os.getcwd(), self.PROGRAMM_FOLDER)):
            os.makedirs(os.path.join(os.getcwd(), self.PROGRAMM_FOLDER))

        if not os.path.exists(os.path.join(os.getcwd(), self.EXPORT_FOLDER)):
            os.makedirs(os.path.join(os.getcwd(), self.EXPORT_FOLDER))

        if not os.path.exists(os.path.join(os.getcwd(), self.IMPORT_FOLDER)):
            os.makedirs(os.path.join(os.getcwd(), self.IMPORT_FOLDER))

        if not os.path.exists(os.path.join(os.getcwd(), self.IMPORT_DONE_SUBFOLDER)):
            os.makedirs(os.path.join(os.getcwd(), self.IMPORT_DONE_SUBFOLDER))

        if not os.path.exists(os.path.join(os.getcwd(), self.IMPORT_FAILED_SUBFOLDER)):
            os.makedirs(os.path.join(os.getcwd(), self.IMPORT_FAILED_SUBFOLDER))

        self.confchanged = False  # bei änderungen der config auf True, damit dann settings gespeichert werden
        pass

    def read(self, filename=('config.json')):

        configfilename = os.path.join(os.getcwd(), self.PROGRAMM_FOLDER, filename)
        # wenn keine config existiernt mit passwort anlegen
        if not os.path.isfile(configfilename):
            self.load_default_settings()
            save_in_json(configfilename, self.data)
            print('Config existiert nicht. Default Config angelegt.')
        else:
            self.data = load_from_json(configfilename)

        self.PROFILE_SET_PROFILE_NAME = self.data['profile_settings']['profile_name']
        self.PROFILE_SET_NAME  = self.data['profile_settings']['name']
        self.PROFILE_SET_FAMILIY_NAME  = self.data['profile_settings']['family_name']
        self.PROFILE_SET_EMAIL  = self.data['profile_settings']['email']
        self.PROFILE_SET_STREET  = self.data['profile_settings']['street']
        self.PROFILE_SET_ZIP_CODE  = self.data['profile_settings']['zip_code']
        self.PROFILE_SET_CITY  = self.data['profile_settings']['city']
        self.PROFILE_SET_COUNTRY  = self.data['profile_settings']['country']
        self.PROFILE_SET_COMPANY_PROFESSION  = self.data['profile_settings']['company_profession']
        self.PROFILE_SET_RADIUS_OF_ACTIVITY  = self.data['profile_settings']['radius_of_activity']
        self.PROFILE_SET_COORDINATES  = self.data['profile_settings']['coordinates']
        self.PROFILE_SET_PHONE  = self.data['profile_settings']['phone']
        self.PROFILE_SET_WEBSITE  = self.data['profile_settings']['website']
        self.PROFILE_SET_INTERESTS_HOBBIES = self.data['profile_settings']['interests_hobbies']


        self.GUI_COLUMN_SELECTION = ast.literal_eval(str(self.data['gui']['column_selection'])) # interpret string as python-list
        self.S2_UNUSED2 = self.data['gui']['s2sett2']

    def write(self, filename='config.json'):
        configfilename = os.path.join(os.getcwd(), self.PROGRAMM_FOLDER, filename)
        self.data['profile_settings']['profile_name'] = self.PROFILE_SET_PROFILE_NAME
        self.data['profile_settings']['name'] = self.PROFILE_SET_NAME
        self.data['profile_settings']['family_name'] = self.PROFILE_SET_FAMILIY_NAME
        self.data['profile_settings']['email'] = self.PROFILE_SET_EMAIL
        self.data['profile_settings']['street'] = self.PROFILE_SET_STREET
        self.data['profile_settings']['zip_code'] = self.PROFILE_SET_ZIP_CODE
        self.data['profile_settings']['city'] = self.PROFILE_SET_CITY
        self.data['profile_settings']['country'] = self.PROFILE_SET_COUNTRY
        self.data['profile_settings']['company_profession'] = self.PROFILE_SET_COMPANY_PROFESSION
        self.data['profile_settings']['radius_of_activity'] = self.PROFILE_SET_RADIUS_OF_ACTIVITY
        self.data['profile_settings']['coordinates'] = self.PROFILE_SET_COORDINATES
        self.data['profile_settings']['phone'] = self.PROFILE_SET_PHONE
        self.data['profile_settings']['website'] = self.PROFILE_SET_WEBSITE
        self.data['profile_settings']['interests_hobbies'] = self.PROFILE_SET_INTERESTS_HOBBIES

        self.data['gui']['column_selection'] = str(self.GUI_COLUMN_SELECTION)
        self.data['gui']['s2sett2'] = self.S2_UNUSED2

        save_in_json(configfilename, self.data)

        self.confchanged = False  # nach speicherung wieder auf false setzen

        print('Config saved')

    def load_default_settings(self):
        # Neue Settings auch die obige write Funktion anpassen, sonnst werden änderungen innerhalb des Programms nicht gespeichert
        self.data = {'profile_settings': {'profile_name': '', 'name': '', 'family_name': '', 'street': '', 'zip_code': '',
                                          'city': '', 'country': '', 'company_profession': '', 'email': '',
                                          'radius_of_activity': '', 'coordinates': '', 'phone': '', 'website': '',
                                          'interests_hobbies': ''},
                     'gui': {'column_selection': [], 's2sett2': "-"}
                     }

    # zum abfragen ob config gespeichert werden muss
    def config_changed(self):
        return self.confchanged

    def set_config_changed(self):
        self.confchanged = True


def save_var_to_file(variable, filename):
    """ Saves variable like a dict to a file

        :param variable: var to save
        :param filename: name for the file
    """
    with open(filename, 'wb') as file:
        pickle.dump(variable, file)


def load_var_from_file(filename):
    """ Saves variable like a dict to a file

        :param variable: var to save
        :param filename: name of the file
        :return: variable
    """
    with open(filename, 'rb') as file:
        # Call load method to deserialize
        myvar = pickle.load(file)
    return myvar


def rand_hex(length):
    """
    :param length: determines the length of the string
    :return: rand string of hex values
    """
    return binascii.hexlify(os.urandom(length)).decode()[:length]


class local_card_db:
    def __init__(self, file, folder):
        # self.filename = file
        self.use_encrypted_db = False # todo feature to encrpyt the database
        self.encrypted_db_filename = os.path.join(os.getcwd(), folder, "crypt" + file)
        self.decrypted_db_filename = os.path.join(os.getcwd(), folder, file)
        self.db_filename = self.decrypted_db_filename
        if self.use_encrypted_db:
            self.db_filename = self.encrypted_db_filename
        self.password = ''


    def hide_data_card(self,card_id):
        """
                marks the content as hidden if it is considered locally inappropriate.

                :param card_id:
                :return:
                """
        self.sql("UPDATE local_card_info SET hidden = 1 WHERE card_id = ?;", (card_id, ))


    def unhide_data_card(self,card_id):
            """
                    marks the content as not hidden (for example, if it was wrongly considered inadequate)

                    :param card_id: ID of the car
                    :return:
                    """
            self.sql("UPDATE local_card_info SET hidden = 0 WHERE card_id = ?;", (card_id, ))


    def datacard_to_sql_update(self, datacard):
        """ Generate from a datacard the sql commands for needed tables to update the existing datacard in the sql database.

        :param datacard: datacard dict
        :return: sql-commands for the update of the datacards
        """


        # newsalts = ""
        # for salt in datacard['dc_dynamic_head']['salts']:
        #     newsalts += f"{str(salt)},"
        # datacard['dc_dynamic_head']['salts'] = newsalts[:-1]

        # convert salts back from list to comma separated string
        datacard['dc_dynamic_head']['salts'] = ','.join(str(salt) for salt in datacard['dc_dynamic_head']['salts'])

        commands = []
        for tablename in datacard.keys():

            sql_command = "UPDATE "
            # sql_values = ""
            sql_data_tuble = ()
            table = tablename
            if table == 'data':
                table = datacard['dc_head']['type']
            sql_command += f"{table} SET "

            for column in datacard[tablename].keys():
                if column == "card_id":
                    continue  # ignore card_id here, card_id is set on the end

                data = datacard[tablename][column]
                if tablename == 'data':
                    sql_command += f"{column} = ?, "
                    sql_data_tuble += (data[0],)
                    sql_command += f"HOPS_{column} = ?, "
                    sql_data_tuble += (data[1],)
                    sql_command += f"DELETED_{column} = ?, "
                    sql_data_tuble += (data[2],)
                else:
                    sql_command += f"{column} = ?, "
                    sql_data_tuble += (data,)

            sql_command = sql_command[:-2]  # remove the last 2 elements in the string

            card_id = datacard['dc_head']['card_id']
            sql_command += f" WHERE card_id = ?;"
            sql_data_tuble += (card_id,)

            commands.append([sql_command, sql_data_tuble])

        return commands

    def datacard_to_sql_insert(self, datacard):
        """ Generate from a datacard the sql insert commands for the needed tables to import a new non existing
        datacard to the sql database.

        :param datacard: datacard dict
        :return: sql-commands for the import of the datacards
        """

        # convert salts back from list to comma separated string
        newsalts = ""
        for salt in datacard['dc_dynamic_head']['salts']:
            newsalts += f"{str(salt)},"
        datacard['dc_dynamic_head']['salts'] = newsalts[:-1]

        commands = []
        for tablename in datacard.keys():
            table = tablename
            sql_command = "INSERT INTO "
            sql_values = ""
            sql_data_tuble = ()
            if table == 'data':
                table = datacard['dc_head']['type']
            sql_command += f"{table} ( "

            for column in datacard[tablename].keys():
                data = datacard[tablename][column]
                if tablename == 'data':
                    sql_command += f"{column}, "
                    sql_data_tuble += (data[0],)
                    sql_command += f"HOPS_{column}, "
                    sql_data_tuble += (data[1],)
                    sql_command += f"DELETED_{column}, "
                    sql_data_tuble += (data[2],)
                    sql_values += "?, ?, ?, "
                else:
                    sql_command += f"{column}, "
                    sql_data_tuble += (data,)
                    sql_values += "?, "

            # add card_id to data part
            if tablename == 'data':
                card_id = datacard['dc_head']['card_id']
                sql_command += "card_id, "
                sql_data_tuble += (card_id,)
                sql_values += "?, "

            sql_command = sql_command[:-2]  # remove the last 2 elements in the string
            sql_values = sql_values[:-2]  # remove the last 2 elements in the string
            sql_command += f") VALUES ( {sql_values} );"

            commands.append([sql_command, sql_data_tuble])

        # insert card_id in local_card_info table
        sql_command = f"INSERT INTO local_card_info ( card_id ) VALUES ( ? );"
        sql_data_tuble = (card_id,)
        commands.append([sql_command, sql_data_tuble])

        return commands

    def convert_db_to_dict(self, card_id, increase_hop=False, add_hops_info=True):
        """
        Convert an sqlite DB entry to an dictionary (which is send to friends)
        :param card_id: ID of the card which will be converted to a datacard dict
        :param increase_hop if True the hop counter will be increased (i.e. when exported to friend)
        :param add_hops_info adds the hops info to the data part in form of a list, if not only content is added
        :return:
        """

        # create head dict
        columns = self.list_tables_colums('dc_head')
        cursor = self.conn.execute(f"select * from dc_head WHERE card_id = '{card_id}'")
        output = cursor.fetchall()[0]
        cursor.close()

        dc_head = {}
        for i in range(len(columns)):
            dc_head[columns[i]] = output[i]

        # create content dict
        columns = self.list_tables_colums(dc_head['type'])
        cursor = self.conn.execute(f"select * from {dc_head['type']} WHERE card_id = '{card_id}'")
        output = cursor.fetchall()[0]
        cursor.close()


        card_type_content = {}

        hops_info = {}
        for i in range(len(columns)):
            if (str(columns[i]).find("DELETED_") > -1 or str(columns[i]).find("HOPS_") > -1):
                hops_info[columns[i]] = output[i]
                continue
            if columns[i] != "card_id":
                if add_hops_info:
                    card_type_content[columns[i]] = [output[i]]
                else:
                    card_type_content[columns[i]] = output[i]

        if add_hops_info:
            # add hops info to content
            for element in card_type_content:
                # print(element)
                card_type_content[element].append(hops_info[("HOPS_" + str(element))])
                card_type_content[element].append(hops_info[("DELETED_" + str(element))])

        if not add_hops_info:
            for element in card_type_content:
                if hops_info[('DELETED_' + str(element))] != '0':
                    card_type_content[element] = "" # delete content if deleted

        columns = self.list_tables_colums('dc_dynamic_head')
        cursor = self.conn.execute(f"select * from dc_dynamic_head WHERE card_id = '{card_id}'")
        output = cursor.fetchall()[0]
        cursor.close()

        dc_dynamic_head = {}
        for i in range(len(columns)):
            # print(f"{columns[i]}={output[i]}")
            dc_dynamic_head[columns[i]] = output[i]

        dc_dynamic_head['salts'] = str(dc_dynamic_head['salts']).split(',')


        # hop counter needs to increased when the data is exported for friends
        if increase_hop:
            simulate_hops = 1  # normaly set to 1, for debug (simulate more hops) you can set higher
            for loop in range(simulate_hops):
                dc_dynamic_head['hops'] += 1
                hops = dc_dynamic_head['hops']
                # elemente der datenkarte löschen wenn der freund zu weit entfernt

                # salt festlegen der genutzt wird.
                for sal in dc_dynamic_head['salts']:
                    # print('sal: ',sal)
                    if sal != "-":
                        salt = sal
                        break

                delete_salt = False
                for data_element in card_type_content:
                    # wenn hops größer als für das element erlaubt, dann läschen
                    if hops > card_type_content[data_element][1]:
                        delete_salt = True
                        if card_type_content[data_element][2] == '0': # marked as not deleted (when deleted hash is content)
                            temp_string = str(card_type_content[data_element][0]) + str(
                                card_type_content[data_element][1]) + str(salt)
                            card_type_content[data_element][0] = "" # delete content
                            card_type_content[data_element][2] = short_SHA256(temp_string) # write hash to deleted val


                # salt löschen mit den inhalt gesaltet wurde (damit kurzer ihhalt nicht per Brutforce
                if delete_salt:
                    dc_dynamic_head['salts'] = ["-" if i == salt else i for i in dc_dynamic_head['salts']]


        data_card = {}
        data_card['dc_head'] = dc_head
        data_card[
            'dc_dynamic_head'] = dc_dynamic_head  # parts that are not hashed (are changed by friends / neigbors and which are not static)
        data_card['data'] = card_type_content

        return data_card

    def datacard_exist(self, card_id):
        """
        check if the datacard with the id exists

        :param card_id:
        :return: True or False
        """
        cursor = self.conn.execute(f"select * from dc_head WHERE card_id = '{card_id}'")
        output = cursor.fetchall()
        cursor.close()
        if len(output) > 0:
            return True

        return False

    def friend_exist(self, pubkey_id):
        """
        check if the friend with the pubkey_id exists

        :param pubkey_id: pubkey_id of the friend
        :return: True or False
        """
        cursor = self.conn.execute(f"select * from friends WHERE pubkey_id = '{pubkey_id}'")
        output = cursor.fetchall()
        cursor.close()
        if len(output) > 0:
            return True

        return False

    def special_hash_from_sql(self, card_id):

        cursor = self.conn.execute(f"select salts from dc_dynamic_head WHERE card_id = '{card_id}'")
        output = cursor.fetchall()[0]
        cursor.close()
        salts = str(output[0]).split(",")
        salts = list(map(lambda x: x.replace('-', ''), salts))  # replace "-" with ""

        # create head
        columns = self.list_tables_colums('dc_head')
        cursor = self.conn.execute(f"select * from dc_head WHERE card_id = '{card_id}'")
        output = cursor.fetchall()[0]
        cursor.close()

        temp_hash_list = []
        for i in range(len(columns)):
            temp_hash_list.append(short_SHA256(str(output[i])))
            if columns[i] == "type":
                contenttype = str(output[i])

        temp_hash_list.sort()  # when sorted the order of the elements in the header can be ignored

        header_string = ""
        for element in temp_hash_list:
            header_string += element

        header_string += salts[-1]  # + salt

        hash_list = []
        hash_list.append(short_SHA256(header_string))

        # hash content
        columns = self.list_tables_colums(contenttype)
        cursor = self.conn.execute(f"select * from {contenttype} WHERE card_id = '{card_id}'")
        output = cursor.fetchall()[0]
        cursor.close()

        # determine maxhop and maxe dict from sql answer
        content = {}
        max_hop = 0
        for i in range(len(columns)):
            content[columns[i]] = output[i]
            if str(columns[i]).find("HOPS_") == 0:
                if int(output[i]) > max_hop:
                    max_hop = int(output[i])

        current_hop = max_hop

        for salt in reversed(salts):
            for i in range(len(columns)):
                if not (str(columns[i]).find("HOPS_") > -1 or str(columns[i]).find("DELETED_") > -1 or str(
                        columns[i]).find("card_id") > -1):
                    if int(content[("HOPS_" + str(columns[i]))]) == current_hop:
                        if (content[("DELETED_" + str(columns[i]))] == '0'):  # if not deleted calc hash
                            string_to_hash = str(output[i]) + str(content[("HOPS_" + str(columns[i]))]) + salt
                            hash_list.append(short_SHA256(string_to_hash))
                        else:  # else hash is saved in Deleted
                            hash_list.append(str(content[("DELETED_" + str(columns[i]))]))
            current_hop -= 1

        hash_list.sort()  # when sorted the order of the elements in the header can be ignored

        temp_string = ""
        for element in hash_list:
            temp_string += element
        # print(temp_string)
        specialhash = SHA256.new(temp_string.encode("utf8")).hexdigest()
        return specialhash

    def add_own_public_key_to_database(self, key_id, publickey_pemformat, rsa_keypair):
        """ adds the own pupkey to the database if is not in the database
        :param key_id:
        :param publickey_pemformat:
        :return:
        """

        output = self.sql(f"select * from publickeys WHERE pubkey_id = '{key_id}'")
        own_pupkey_in_database = (len(output) > 0)

        # if key_id not exist add key
        if not own_pupkey_in_database:
            date_time_now = datetime.now().replace(microsecond=0)

            maxhop = 5  # the max distribution of pubkeys is not limited by maxhop, instead it should only by
            # distributed to friends when the pub key is needed it will be exported (when a an other datacard exists
            # where the key is need to verify signature)
            version = 0
            deleted = False
            valid_until = add_months(date_time_now, 360) #30 years "endless" valid. so this datacard don't expires von db-clean
            edited = date_time_now
            created = date_time_now
            type = "publickeys"
            creator = key_id

            # special case: card_id of the own_pubkey should be always the same (not random), because when friend import
            # the same pubkey_id with different card_id the import function have to be more complex to catch this case
            # it is much easier to make the card_id static (on db reset the card id will be identical)
            card_id = key_id

            # insert dc_head
            sql_command = (f"""INSERT INTO dc_head ( version, maxhop, deleted, valid_until, edited, created, type, creator, card_id )
                               VALUES ( ? , ?, ?, ?, ?, ?, ?, ?, ? ); """)
            self.sql(sql_command, (version, maxhop, deleted, valid_until, edited, created, type, creator, card_id))

            sql_command = (
                "INSERT INTO publickeys (card_id, publickey, pubkey_id, HOPS_publickey, HOPS_pubkey_id) VALUES ( ?, ?, ?, ?, ? );")
            self.sql(sql_command, (
                card_id, publickey_pemformat, key_id, maxhop, maxhop))  # hops for every part to max

            salts = (binascii.hexlify(os.urandom(8)).decode())  # one salt ist added

            # insert dynamic head
            sql_command = (f"""INSERT INTO dc_dynamic_head (salts, signature, hops, card_id) 
                               VALUES ('{salts}',  NULL, 0, '{card_id}');""")
            self.sql(sql_command)

            # calc signature and add to database
            special_hash = self.special_hash_from_sql(card_id).encode("utf-8")
            signature = sign(special_hash, rsa_keypair).decode("utf-8")

            sql_command = f"""UPDATE dc_dynamic_head SET signature = '{signature}' 
                                          WHERE card_id = '{card_id}';"""
            self.sql(sql_command)


    def remove_datacards(self, card_ids) -> bool:
        """removes multiple datacards from all tables (head, dynamic_head, ...)

        :param card_ids: list of all card_ids
        :return: True when cards removed, or False when no cards have been removed
        """
        if not isinstance(card_ids, list):
            raise ValueError("card_ids must be a list")

        if len(card_ids) > 0:
            # building one sql command to remove all cards
            where_condition = ""
            for card_id in card_ids:
                where_condition += f"card_id = '{card_id}' OR "
            where_condition = where_condition[:-4] #remove last "OR"

            #delete in all tables # todo improve to look in all tables of db and when exists then remove
            for sql_table in ["dc_head", "dc_dynamic_head", "business_card", "local_card_info"]:
                sql_command = f"DELETE FROM {sql_table} WHERE {where_condition};"
                #print(sql_command)
                self.sql(sql_command)
            return True
        return False


    def clean_database(self,profile_id, check_system_time = True):
        """remove expired cards from database. removed unused pubkeys. deactivateds friendship when expired

        :param profile_id:
        :param check_system_time:
        :return: True when cleaing was susccessful, False when system time was wrong or could checked
        """
        print("clean database")

        # this time check routine will stop (return) and gui will ask user if system time is correct,
        # to reduce possibility of mass delete cards from database when system time is to much in the future
        local_time_diff = system_clock_ntp_difference()
        internet_time_unknown = (local_time_diff == 0)
        last_clean = self.sql(f"SELECT value FROM local_status WHERE status_name = 'last_db_clean';")[0][0]
        # last clean over 30 days ago ?
        last_clean_too_long_ago = (last_clean < str((datetime.now() - timedelta(days=28)).replace(microsecond=0)))
        last_clean_in_future = (last_clean > str((datetime.now()).replace(microsecond=0)))

        if check_system_time and internet_time_unknown and last_clean_too_long_ago:
            # #when system-time could not checked if correct and last check long ago (the user will be asked if system date is correct)
            return False
        #if time is wrong more than 86400 seconds (one day) return  (user will get prompt)
        if check_system_time and (abs(local_time_diff) > 86400 or last_clean_in_future): # return when time is wrong! -> (user will get prompt)
            #print("local time incorrect or could not checked. database not cleaned")
            return False # time check failed or clock diff larger than 1 day


        #set time limit when exiperd cards have to be deleted (expiration older than 3 days ago, to keep for a while)
        delete_time_limit = str((datetime.now() - timedelta(days=3)).replace(microsecond=0))

        #### REMOVE EXPIRED DATA CARDS ####
        #clean all expired cards which are not local created, and expired datacards which are local created and marked as deletet
        # (to keep local expired until marked as deleted)
        sql_command = f"""SELECT card_id FROM dc_head WHERE (valid_until < '{delete_time_limit}' AND creator != '{profile_id}') 
        OR (valid_until < '{delete_time_limit}' AND creator = '{profile_id}' AND deleted = True);"""
        cards = self.sql_list(sql_command)
        self.remove_datacards(cards) # remove all expired cards


        #### REMOVE NOT NEEDED PUBKEYS ####
        # selects pukeys where need from existing data_cards in db (but not pubkeys of pubkey-datacards)
        needed_pubkey_ids = self.sql_list(f"""SELECT DISTINCT creator FROM dc_head WHERE type != 'publickeys';""") #
        needed_pubkey_ids += self.sql_list(f"""SELECT pubkey_id FROM friends;""")# friends pubkeys also needed
        needed_pubkey_ids.append(profile_id)

        # determine all pubkeys in db and remove needed keys -> unused will be left -> remove them
        remove_pubkeys = self.sql_list(f"""SELECT DISTINCT creator FROM dc_head;""") # collect all keys
        remove_pubkeys += self.sql_list(f"""SELECT pubkey_id FROM publickeys;""") # collect all keys

        remove_pubkeys = [*set(remove_pubkeys)]  # removes duplicates from list
        for key in needed_pubkey_ids:
            if key in remove_pubkeys:
                remove_pubkeys.remove(key) # remove needed keys

        # remove unneded pubkeys from datacards tables
        self.remove_datacards(remove_pubkeys) # with pubkeys: card_id and pubkey_id is identical (so the ids of pubkeys can be used to remove)
        # remove unneded pubkeys from publickeys table
        for key in remove_pubkeys:
            self.sql(f"DELETE FROM publickeys WHERE pubkey_id = '{key}';")


        # set friendship to inactive when expired
        self.sql(f"UPDATE friends SET active_friendship = 0 WHERE expire_date < '{delete_time_limit}';")

        # save last_db clean time
        self.sql(f"UPDATE local_status SET value = '{str((datetime.now()).replace(microsecond=0))}' WHERE status_name = 'last_db_clean';")
        print("database cleaned")
        return True # clean succesful


    def extend_table(self, table_name):
        """
        extends a table for each column with hop column and deleted column. this is needed for share different parts of a a data_card with differents hops
        So some parts are only visible to direct friends (hop = 1) and other for friends of friends (hop = 2) or more hops

        :param table_name: name of the table to add columns
        :return:
        """
        all_columns = self.list_tables_colums(table_name)
        # add columns for all column aexcept card_id (card_id is the foreign key)
        for column in all_columns:
            if column != "card_id":  #
                sqlite_command = (
                        "ALTER TABLE " + table_name + " ADD COLUMN HOPS_" + column + " INT (1) DEFAULT (0)")  # mit hop erweitert
                self.cursor.execute(sqlite_command)
                sqlite_command = (
                        "ALTER TABLE " + table_name + " ADD COLUMN DELETED_" + column + " CHAR (16) DEFAULT (0)")  # mit DELETED erweitert
                self.cursor.execute(sqlite_command)

        # Commit your changes in the database
        self.conn.commit()

    def init_password(self, encrypted_database):
        # self.password = password

        self.conn = self.open_cdb(encrypted_database)
        self.cursor = self.conn.cursor()

        self.init_standard_tables()

    def import_new_datacard(self, datacard):
        """ import a new not existing datacard (dict format) to the local database

        :param datacard:
        :return:
        """
        sql_commands = self.datacard_to_sql_insert(datacard)
        for command in sql_commands:
            sql_com = command[0]
            sql_com_data = command[1]
            # ic(sql_com)
            self.sql(sql_com, sql_com_data)
            # ic("command done!")

    def import_update_existing_datacard(self, datacard):
        """updates an existing datacards in the local database when it is imported from friends

        :param datacard:
        :return:
        """

        sql_commands = self.datacard_to_sql_update(datacard)
        for command in sql_commands:
            sql_com = command[0]
            sql_com_data = command[1]
            # ic(sql_com)
            self.sql(sql_com, sql_com_data)
        pass

    def init_standard_tables(self):
        # sqlite info: STRING will convert it into a numeric value, while TEXT will not perform any conversion
        if not self.table_exists("dc_head"):
            sqlite_command = """ CREATE TABLE dc_head (
                                card_id          CHAR (32) PRIMARY KEY
                                                      UNIQUE
                                                      NOT NULL,
                                creator     CHAR (32) NOT NULL,
                                type        CHAR,
                                created     DATETIME,
                                edited      DATETIME,
                                valid_until DATE,
                                version     INT DEFAULT (0),
                                deleted     BOOLEAN DEFAULT (0),
                                maxhop      INT (1)
                            );"""
            self.sql(sqlite_command)

        # stores need status info like: last_database_clean, last_export, ...
        if not self.table_exists("local_status"):
            sqlite_command = """CREATE TABLE local_status (
                                status_name       TEXT PRIMARY KEY  UNIQUE,
                                value      TEXT,
                                comment    TEXT
                            );"""
            self.sql(sqlite_command)
            self.init_status_table() # write first needed values to table


        if not self.table_exists("dc_dynamic_head"):
            sqlite_command = """ CREATE TABLE dc_dynamic_head (
                                card_id                    REFERENCES dc_head (card_id),
                                hops      INT (1),
                                signature TEXT,
                                salts     TEXT
                            );"""
            self.sql(sqlite_command)

        if not self.table_exists("business_card"):
            # the first colum has to be the current_element_id
            sqlite_command = """CREATE TABLE business_card (
                                card_id                    REFERENCES dc_head (card_id),
                                image              TEXT,
                                name               TEXT,
                                family_name        TEXT,
                                radius_of_activity TEXT,
                                street             TEXT,
                                zip_code           INTEGER,
                                city               TEXT,
                                country            TEXT,
                                coordinates        TEXT,
                                company_profession TEXT,
                                phone              TEXT,
                                website            TEXT,
                                email              TEXT,
                                other_contact      TEXT,
                                interests_hobbies  TEXT,
                                skills_offers      TEXT,
                                requests           TEXT,
                                tags               TEXT
                            );
                            """
            self.sql(sqlite_command)
            self.extend_table("business_card")


        if not self.table_exists("local_card_info"):
            # stores information which are not shared to other. (distance or to hide card locally ...)
            sqlite_command = """CREATE TABLE local_card_info (
                                card_id    REFERENCES dc_head (card_id),
                                hidden     BOOLEAN DEFAULT (0),
                                distance   CHAR (8),
                                mailing_list TEXT (64) DEFAULT ('')                                
                            );
                            """
            self.sql(sqlite_command)


        if not self.table_exists("complete_table"):
            sqlite_command = """CREATE VIEW complete_table AS SELECT * FROM (business_card INNER JOIN dc_head ON 
            dc_head.card_id = business_card.card_id INNER JOIN local_card_info ON 
            dc_head.card_id = local_card_info.card_id) WHERE deleted = False;"""
            self.sql(sqlite_command)

        if not self.table_exists("publickeys"):
            sqlite_command = """CREATE TABLE publickeys (pubkey_id CHAR (32) PRIMARY KEY, publickey TEXT, 
            card_id CHAR (32) REFERENCES dc_head (card_id)); """
            self.sql(sqlite_command)
            self.extend_table("publickeys")

        if not self.table_exists("friends"):
            sqlite_command = """CREATE TABLE friends (
                                pubkey_id         CHAR (32) PRIMARY KEY  UNIQUE,
                                publickey         TEXT,
                                active_friendship BOOLEAN   DEFAULT (0),
                                name              TEXT,
                                friend_since_date      CHAR (30),
                                expire_date       CHAR (30),
                                comment           TEXT,
                                email     TEXT
                            );"""
            self.sql(sqlite_command)


    def init_status_table(self):
        """initialize status table with needed values after table creation"""
        date_time_now = str(datetime.now().replace(microsecond=0))
        #(table_creation, last_db_clean, last_export)
        sql_command = (f"""INSERT INTO local_status VALUES 
                        ( 'db_creation' , ? , 'timestamp of the creation of the database'), 
                        ( 'last_db_clean' , ? , 'timestamp of last table clean'), 
                        ( 'last_friend_export' , ? , 'timestamp of last export of datacard to friends'); """)
        self.sql(sql_command, (date_time_now, date_time_now, date_time_now))

    def list_all_tables(self):
        cursor = self.conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [
            v[0] for v in cursor.fetchall()
            if v[0] != "sqlite_sequence"
        ]
        cursor.close()
        return tables

    def list_tables_colums(self, tablename):
        cursor = self.conn.execute('select * from ' + tablename)
        column_names = [description[0] for description in cursor.description]
        cursor.close()
        return column_names

    def table_exists(self, tablename, printoutput=False):
        try:
            self.cursor.execute("SELECT * FROM " + tablename + ";")
            if printoutput:
                print("table " + tablename + " exists")
            return True
        except sqlite3.OperationalError:
            if printoutput:
                print("no such table: " + tablename)
            return False

    def sql(self, sql_command, args=""):
        """ excecutes an SQLite Command and returns the answer

        :param command: SQL-Querry
        :param args:
        :return: sql-answer
        """
        result = self.cursor.execute(sql_command, args)
        self.conn.commit()
        # if returnval:
        return result.fetchall()

    def duplicate_data_card(self,card_id, new_card_id):
        """
        duplicates an existing card_id with a new_card_id in all needed tables of the database.
        :param card_id: old card_id which is to duplicate
        :param new_card_id: new id for the duplicated content
        :return:
        """
        card_type = str(self.sql_list(f"SELECT type FROM dc_head WHERE card_id = '{card_id}'")[0])
        all_tables = ['dc_head', 'dc_dynamic_head', card_type, 'local_card_info']

        for table in all_tables:
            table_columns = self.list_tables_colums(table)
            all_columns = ', '.join(table_columns)
            new_colums = all_columns.replace("card_id", f"\"{new_card_id}\"")
            #dprint(all_columns, "\n", new_colums)
            sql_command = f"""INSERT INTO {table} ({all_columns}) SELECT {new_colums} 
                              FROM {table} WHERE card_id = '{card_id}';"""
            self.sql(sql_command)

        # #dprint(card_type)
        #
        # #copy into dc_dynamic_head
        # table_columns = self.list_tables_colums("dc_dynamic_head")
        # all_columns = ', '.join(table_columns)
        # new_colums = all_columns.replace("card_id", f"\"{new_card_id}\"")
        # #dprint(all_columns, "\n", new_colums)
        # sql_command = f"""INSERT INTO dc_dynamic_head ({all_columns}) SELECT {new_colums} FROM dc_dynamic_head WHERE card_id = '{card_id}';"""
        # #dprint(sql_command, "\n")
        # self.sql(sql_command)
        #
        # # copy into card_type table (for example business_card)
        # table_columns = self.list_tables_colums(card_type)
        # all_columns = ', '.join(table_columns)
        # new_colums = all_columns.replace("card_id", f"\"{new_card_id}\"")
        # #dprint(all_columns, "\n", new_colums)
        # sql_command = f"""INSERT INTO {card_type} ({all_columns}) SELECT {new_colums} FROM {card_type} WHERE card_id = '{card_id}';"""
        # #dprint(sql_command, "\n")
        # self.sql(sql_command)
        #
        # # copy into card_type table (for example business_card)
        # table_columns = self.list_tables_colums(card_type)
        # all_columns = ', '.join(table_columns)
        # new_colums = all_columns.replace("card_id", f"\"{new_card_id}\"")
        # # dprint(all_columns, "\n", new_colums)
        # sql_command = f"""INSERT INTO {card_type} ({all_columns}) SELECT {new_colums} FROM {card_type} WHERE card_id = '{card_id}';"""
        # # dprint(sql_command, "\n")
        # self.sql(sql_command)

    def sql_list(self, sql_command, args="") ->list:
        """ excecutes an SQLite Command with only on selected column and returns  the answer as list

        :param command: SQL-Querry
        :param args:
        :return: sql-answer
        """
        result = self.cursor.execute(sql_command, args).fetchall()
        self.conn.commit()
        newlist = []
        if len(result) > 0:
            if len(result[0]) > 1:
                raise Exception("Only on colum can be selected with this command.")
            for el in result:
                newlist.append(el[0])

        return newlist



    def sql_dict(self, sql_command):
        """Returns data from an SQL query as a list of dicts."""
        try:
            self.conn.row_factory = sqlite3.Row
            things = self.conn.execute(sql_command).fetchall()
            unpacked = [{k: item[k] for k in item.keys()} for item in things]
            return unpacked
        except Exception as e:
            print(f"Failed to execute. Query: {sql_command}\n with error:\n{e}")
            return []

    def sql_tuble_to_dict(self, sql_list):
        """ Convert a sql answer (list of tubles (only with 2 elements ) to a dict where the first element of the tuble will be the key of the dict)
            Only tubles with
        example sql: [("1", "abc"), ("2", "def")] -> {"1": "abc", "2": "def"}

        :param sql_list:
        :return: dict like: {"1": "abc", "2": "def"}
        """
        #dprint(sql_list)
        if len(sql_list[0]) != 2:
            raise Exception("Wrong Tuble length")
        new_dict = {}
        for element in sql_list:
            new_dict[element[0]] = element[1]

        return new_dict


    def update_distances(self,card_ids, local_coordinate):
        """updates the distances off all cards in card_ids"""
        #dprint(card_ids)
        for card_id in card_ids:
            type = self.sql_list(f"""SELECT type FROM dc_head WHERE card_id = '{card_id}'""")[0]
            if type == 'publickeys':
                continue # pubkeys has no coordinates
            [coordinate] = self.sql(f"""SELECT coordinates FROM {type} WHERE card_id = '{card_id}'""")[0]
            distance = geo_distance(f"{coordinate};{local_coordinate}")
            dprint(card_id, type, coordinate, distance, adapt_dist(distance))
            self.sql(f"""UPDATE local_card_info SET distance = ? WHERE card_id = ?; """, (adapt_dist(distance), card_id))

    def close(self):
        # Close the connection
        print("close db connection")
        self.conn.close()

    def key_creation(self, password):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), salt=b'\xfaz\xb5\xf2|\xa1z\xa9\xfe\xd1F@1\xaa\x8a\xc2',
                         iterations=1024, length=32, backend=default_backend())
        key = Fernet(base64.urlsafe_b64encode(kdf.derive(password)))
        return key

    def encryption(self, b, password):
        f = self.key_creation(password)
        safe = f.encrypt(b)
        return safe

    def decryption(self, safe, password):
        f = self.key_creation(password)
        b = f.decrypt(safe)
        return b

    def open_cdb(self, encrypted_database=False):
        # ic(encrypted_database)
        if not encrypted_database:
            # if encrypted db-file exist, decrypte it and delete it (usually on change from encrypted to unenrypted usage)
            if os.path.isfile(self.encrypted_db_filename):
                # ic("verschlüsstelte datei existiert")
                f = gzip.open(self.encrypted_db_filename)
                safe = f.read()
                f.close()
                content = self.decryption(safe, self.password)
                content = content.decode('utf-8')
                os.remove(self.decrypted_db_filename)  # delete unencrypted db
                con = sqlite3.connect(self.decrypted_db_filename)
                con.executescript(content)
                os.remove(self.encrypted_db_filename)  # delete encrypted db
                return con

            con = sqlite3.connect(self.decrypted_db_filename)
            return con
        else:
            # if decrypted db-file exist, just open it it and delete it (usually on change from encrypted to unenrypted usage)
            if os.path.isfile(self.decrypted_db_filename):
                # ic("unverschlüsstelte datei existiert")
                con = sqlite3.connect(self.decrypted_db_filename)
                os.remove(self.encrypted_db_filename)  # delete msy be old encrypted db

                # save to decrypted DB
                fp = gzip.open(self.encrypted_db_filename, 'wb')
                b = b''
                for line in con.iterdump():
                    b += bytes('%s\n', 'utf8') % bytes(line, 'utf8')
                b = self.encryption(b, self.password)
                fp.write(b)
                fp.close()
                return con

            f = gzip.open(self.encrypted_db_filename)
            safe = f.read()
            f.close()
            content = self.decryption(safe, self.password)
            content = content.decode('utf-8')
            con = sqlite3.connect(':memory:')
            # con = sqlite3.connect(self.decrypted_db_filename)
            con.executescript(content)
            return con

    def save_and_close_database(self, encrypt_db):
        # fixme check when decrypted if it works correctly!
        if encrypt_db:
            fp = gzip.open(self.encrypted_db_filename, 'wb')
            b = b''
            for line in self.conn.iterdump():
                b += bytes('%s\n', 'utf8') % bytes(line, 'utf8')
            b = self.encryption(b, self.password)
            fp.write(b)
            fp.close()
            os.remove(self.decrypted_db_filename)  # remove temp decrypted db
        self.close()

def is_english_seed_word(word) -> bool:
    """check if a single word is an valid seed word"""
    words = "abandon ability able about above absent absorb abstract absurd abuse access accident account accuse achieve " \
            "acid acoustic acquire across act action actor actress actual adapt add addict address adjust admit adult " \
            "advance advice aerobic affair afford afraid again age agent agree ahead aim air airport aisle alarm album " \
            "alcohol alert alien all alley allow almost alone alpha already also alter always amateur amazing among " \
            "amount amused analyst anchor ancient anger angle angry animal ankle announce annual another answer antenna " \
            "antique anxiety any apart apology appear apple approve april arch arctic area arena argue arm armed armor " \
            "army around arrange arrest arrive arrow art artefact artist artwork ask aspect assault asset assist assume " \
            "asthma athlete atom attack attend attitude attract auction audit august aunt author auto autumn average " \
            "avocado avoid awake aware away awesome awful awkward axis baby bachelor bacon badge bag balance balcony ball " \
            "bamboo banana banner bar barely bargain barrel base basic basket battle beach bean beauty because become " \
            "beef before begin behave behind believe below belt bench benefit best betray better between beyond bicycle " \
            "bid bike bind biology bird birth bitter black blade blame blanket blast bleak bless blind blood blossom " \
            "blouse blue blur blush board boat body boil bomb bone bonus book boost border boring borrow boss bottom " \
            "bounce box boy bracket brain brand brass brave bread breeze brick bridge brief bright bring brisk broccoli " \
            "broken bronze broom brother brown brush bubble buddy budget buffalo build bulb bulk bullet bundle bunker " \
            "burden burger burst bus business busy butter buyer buzz cabbage cabin cable cactus cage cake call calm " \
            "camera camp can canal cancel candy cannon canoe canvas canyon capable capital captain car carbon card cargo " \
            "carpet carry cart case cash casino castle casual cat catalog catch category cattle caught cause caution cave " \
            "ceiling celery cement census century cereal certain chair chalk champion change chaos chapter charge chase " \
            "chat cheap check cheese chef cherry chest chicken chief child chimney choice choose chronic chuckle chunk " \
            "churn cigar cinnamon circle citizen city civil claim clap clarify claw clay clean clerk clever click client " \
            "cliff climb clinic clip clock clog close cloth cloud clown club clump cluster clutch coach coast coconut " \
            "code coffee coil coin collect color column combine come comfort comic common company concert conduct confirm " \
            "congress connect consider control convince cook cool copper copy coral core corn correct cost cotton couch " \
            "country couple course cousin cover coyote crack cradle craft cram crane crash crater crawl crazy cream " \
            "credit creek crew cricket crime crisp critic crop cross crouch crowd crucial cruel cruise crumble crunch " \
            "crush cry crystal cube culture cup cupboard curious current curtain curve cushion custom cute cycle dad " \
            "damage damp dance danger daring dash daughter dawn day deal debate debris decade december decide decline " \
            "decorate decrease deer defense define defy degree delay deliver demand demise denial dentist deny depart " \
            "depend deposit depth deputy derive describe desert design desk despair destroy detail detect develop device " \
            "devote diagram dial diamond diary dice diesel diet differ digital dignity dilemma dinner dinosaur direct " \
            "dirt disagree discover disease dish dismiss disorder display distance divert divide divorce dizzy doctor " \
            "document dog doll dolphin domain donate donkey donor door dose double dove draft dragon drama drastic draw " \
            "dream dress drift drill drink drip drive drop drum dry duck dumb dune during dust dutch duty dwarf dynamic " \
            "eager eagle early earn earth easily east easy echo ecology economy edge edit educate effort egg eight either " \
            "elbow elder electric elegant element elephant elevator elite else embark embody embrace emerge emotion " \
            "employ empower empty enable enact end endless endorse enemy energy enforce engage engine enhance enjoy " \
            "enlist enough enrich enroll ensure enter entire entry envelope episode equal equip era erase erode erosion " \
            "error erupt escape essay essence estate eternal ethics evidence evil evoke evolve exact example excess " \
            "exchange excite exclude excuse execute exercise exhaust exhibit exile exist exit exotic expand expect expire " \
            "explain expose express extend extra eye eyebrow fabric face faculty fade faint faith fall false fame family " \
            "famous fan fancy fantasy farm fashion fat fatal father fatigue fault favorite feature february federal fee " \
            "feed feel female fence festival fetch fever few fiber fiction field figure file film filter final find fine " \
            "finger finish fire firm first fiscal fish fit fitness fix flag flame flash flat flavor flee flight flip " \
            "float flock floor flower fluid flush fly foam focus fog foil fold follow food foot force forest forget fork " \
            "fortune forum forward fossil foster found fox fragile frame frequent fresh friend fringe frog front frost " \
            "frown frozen fruit fuel fun funny furnace fury future gadget gain galaxy gallery game gap garage garbage " \
            "garden garlic garment gas gasp gate gather gauge gaze general genius genre gentle genuine gesture ghost " \
            "giant gift giggle ginger giraffe girl give glad glance glare glass glide glimpse globe gloom glory glove " \
            "glow glue goat goddess gold good goose gorilla gospel gossip govern gown grab grace grain grant grape grass " \
            "gravity great green grid grief grit grocery group grow grunt guard guess guide guilt guitar gun gym habit " \
            "hair half hammer hamster hand happy harbor hard harsh harvest hat have hawk hazard head health heart heavy " \
            "hedgehog height hello helmet help hen hero hidden high hill hint hip hire history hobby hockey hold hole " \
            "holiday hollow home honey hood hope horn horror horse hospital host hotel hour hover hub huge human humble " \
            "humor hundred hungry hunt hurdle hurry hurt husband hybrid ice icon idea identify idle ignore ill illegal " \
            "illness image imitate immense immune impact impose improve impulse inch include income increase index " \
            "indicate indoor industry infant inflict inform inhale inherit initial inject injury inmate inner innocent " \
            "input inquiry insane insect inside inspire install intact interest into invest invite involve iron island " \
            "isolate issue item ivory jacket jaguar jar jazz jealous jeans jelly jewel job join joke journey joy judge " \
            "juice jump jungle junior junk just kangaroo keen keep ketchup key kick kid kidney kind kingdom kiss kit " \
            "kitchen kite kitten kiwi knee knife knock know lab label labor ladder lady lake lamp language laptop large " \
            "later latin laugh laundry lava law lawn lawsuit layer lazy leader leaf learn leave lecture left leg legal " \
            "legend leisure lemon lend length lens leopard lesson letter level liar liberty library license life lift " \
            "light like limb limit link lion liquid list little live lizard load loan lobster local lock logic lonely " \
            "long loop lottery loud lounge love loyal lucky luggage lumber lunar lunch luxury lyrics machine mad magic " \
            "magnet maid mail main major make mammal man manage mandate mango mansion manual maple marble march margin " \
            "marine market marriage mask mass master match material math matrix matter maximum maze meadow mean measure " \
            "meat mechanic medal media melody melt member memory mention menu mercy merge merit merry mesh message metal " \
            "method middle midnight milk million mimic mind minimum minor minute miracle mirror misery miss mistake mix " \
            "mixed mixture mobile model modify mom moment monitor monkey monster month moon moral more morning mosquito " \
            "mother motion motor mountain mouse move movie much muffin mule multiply muscle museum mushroom music must " \
            "mutual myself mystery myth naive name napkin narrow nasty nation nature near neck need negative neglect " \
            "neither nephew nerve nest net network neutral never news next nice night noble noise nominee noodle normal " \
            "north nose notable note nothing notice novel now nuclear number nurse nut oak obey object oblige obscure " \
            "observe obtain obvious occur ocean october odor off offer office often oil okay old olive olympic omit once " \
            "one onion online only open opera opinion oppose option orange orbit orchard order ordinary organ orient " \
            "original orphan ostrich other outdoor outer output outside oval oven over own owner oxygen oyster ozone pact " \
            "paddle page pair palace palm panda panel panic panther paper parade parent park parrot party pass patch path " \
            "patient patrol pattern pause pave payment peace peanut pear peasant pelican pen penalty pencil people pepper " \
            "perfect permit person pet phone photo phrase physical piano picnic picture piece pig pigeon pill pilot pink " \
            "pioneer pipe pistol pitch pizza place planet plastic plate play please pledge pluck plug plunge poem poet " \
            "point polar pole police pond pony pool popular portion position possible post potato pottery poverty powder " \
            "power practice praise predict prefer prepare present pretty prevent price pride primary print priority " \
            "prison private prize problem process produce profit program project promote proof property prosper protect " \
            "proud provide public pudding pull pulp pulse pumpkin punch pupil puppy purchase purity purpose purse push " \
            "put puzzle pyramid quality quantum quarter question quick quit quiz quote rabbit raccoon race rack radar " \
            "radio rail rain raise rally ramp ranch random range rapid rare rate rather raven raw razor ready real reason " \
            "rebel rebuild recall receive recipe record recycle reduce reflect reform refuse region regret regular reject " \
            "relax release relief rely remain remember remind remove render renew rent reopen repair repeat replace " \
            "report require rescue resemble resist resource response result retire retreat return reunion reveal review " \
            "reward rhythm rib ribbon rice rich ride ridge rifle right rigid ring riot ripple risk ritual rival river " \
            "road roast robot robust rocket romance roof rookie room rose rotate rough round route royal rubber rude rug " \
            "rule run runway rural sad saddle sadness safe sail salad salmon salon salt salute same sample sand satisfy " \
            "satoshi sauce sausage save say scale scan scare scatter scene scheme school science scissors scorpion scout " \
            "scrap screen script scrub sea search season seat second secret section security seed seek segment select " \
            "sell seminar senior sense sentence series service session settle setup seven shadow shaft shallow share shed " \
            "shell sheriff shield shift shine ship shiver shock shoe shoot shop short shoulder shove shrimp shrug shuffle " \
            "shy sibling sick side siege sight sign silent silk silly silver similar simple since sing siren sister " \
            "situate six size skate sketch ski skill skin skirt skull slab slam sleep slender slice slide slight slim " \
            "slogan slot slow slush small smart smile smoke smooth snack snake snap sniff snow soap soccer social sock " \
            "soda soft solar soldier solid solution solve someone song soon sorry sort soul sound soup source south space " \
            "spare spatial spawn speak special speed spell spend sphere spice spider spike spin spirit split spoil " \
            "sponsor spoon sport spot spray spread spring spy square squeeze squirrel stable stadium staff stage stairs " \
            "stamp stand start state stay steak steel stem step stereo stick still sting stock stomach stone stool story " \
            "stove strategy street strike strong struggle student stuff stumble style subject submit subway success such " \
            "sudden suffer sugar suggest suit summer sun sunny sunset super supply supreme sure surface surge surprise " \
            "surround survey suspect sustain swallow swamp swap swarm swear sweet swift swim swing switch sword symbol " \
            "symptom syrup system table tackle tag tail talent talk tank tape target task taste tattoo taxi teach team " \
            "tell ten tenant tennis tent term test text thank that theme then theory there they thing this thought three " \
            "thrive throw thumb thunder ticket tide tiger tilt timber time tiny tip tired tissue title toast tobacco " \
            "today toddler toe together toilet token tomato tomorrow tone tongue tonight tool tooth top topic topple " \
            "torch tornado tortoise toss total tourist toward tower town toy track trade traffic tragic train transfer " \
            "trap trash travel tray treat tree trend trial tribe trick trigger trim trip trophy trouble truck true truly " \
            "trumpet trust truth try tube tuition tumble tuna tunnel turkey turn turtle twelve twenty twice twin twist " \
            "two type typical ugly umbrella unable unaware uncle uncover under undo unfair unfold unhappy uniform unique " \
            "unit universe unknown unlock until unusual unveil update upgrade uphold upon upper upset urban urge usage " \
            "use used useful useless usual utility vacant vacuum vague valid valley valve van vanish vapor various vast " \
            "vault vehicle velvet vendor venture venue verb verify version very vessel veteran viable vibrant vicious " \
            "victory video view village vintage violin virtual virus visa visit visual vital vivid vocal voice void " \
            "volcano volume vote voyage wage wagon wait walk wall walnut want warfare warm warrior wash wasp waste water " \
            "wave way wealth weapon wear weasel weather web wedding weekend weird welcome west wet whale what wheat wheel " \
            "when where whip whisper wide width wife wild will win window wine wing wink winner winter wire wisdom wise " \
            "wish witness wolf woman wonder wood wool word work world worry worth wrap wreck wrestle wrist write wrong " \
            "yard year yellow you young youth zebra zero zone zoo".split(" ")  # todo import from file
    word = str(word).replace(" ", "").lower()  # replace whitespace and case of word
    # print(f"'{word}'")
    return word in words
