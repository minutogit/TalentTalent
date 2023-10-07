# Python code to merge dict using a single
# expression
import html, re
from functions import format_date_string, geo_distance, dprint, order_dict, isValidCoordinate
#import html2text


def complete_url(url):
    """complets add http to url link when missing. (doesn't check correct syntax"""

    if str(url).count(".") == 2 and str(url).lower().find("www.") == 0:
        #print(f"FIX http://{url}")
        return f"http://{url}"
    if str(url).count(".") == 1 and str(url).lower().find("http") == -1: # when only domain.com is typed (without www.)
        #print(f"FIX http://{url}")
        return f"http://{url}"

    return url

def make_html_links(key, value) -> str:

    if key == "website":
        return str(f'<a href="{complete_url(value)}">{value}</a>')
    elif key == "email" and value.find("@") > 0:
        return str(f'<a href="mailto:{value}">{value}</a>')
    elif key == "phone" and len(value) > 2:
        return str(f'<a href="tel:{value}">{value}</a>')
    elif key == "coordinates":
        if geo_distance(value) == "":
            return str(f'<a href="https://www.google.com/maps/place/{str(value.split(";")[0]).replace(" ","")}">{value.split(";")[0]}</a>')
        else:
            return str(f'<p><a href="https://www.google.com/maps/place/{str(value.split(";")[0]).replace(" ","")}">{value.split(";")[0]}</a> ({geo_distance(value)} km)</p>')
    else:
        return value

def make_html_links_for_export(key, value) -> str:

    if key == "website":
        return str(f'<a href="{complete_url(value)}">{value}</a>')
    elif key == "email" and value.find("@") > 0:
        return str(f'<a href="mailto:{value}">{value}</a>')
    elif key == "phone" and len(value) > 2:
        return str(f'<a href="tel:{value}">{value}</a>')
    elif key == "coordinates":
        if str(value).strip().startswith(';'):
            return ""
        if geo_distance(value) == "":
            return str(f'<a href="https://www.google.com/maps/place/{str(value.split(";")[0]).replace(" ","")}">({value.split(";")[0]})</a>')

        return str(f'<a href="https://www.google.com/maps/place/{str(value.split(";")[0]).replace(" ","")}">({geo_distance(value)}km)</a>')
    else:
        return value



def concat_dicts(dict1, dict2):
    """concatenate two dicts"""
    res = {**dict1, **dict2}
    return res

html_head = """<!DOCTYPE html>
<html>
    <head>
        <title>-</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <style>
        th, td {
          padding: 1px;
        }
        tr:nth-child(even) {
          background-color: rgba(150, 212, 212, 0.4);
        }
        </style>\n 
    </head>
<body>"""

html_export_head = """<!DOCTYPE html>
<html>
    <head>
        <title>-</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta charset="UTF-8">
        <style>
            /* Allgemeine Stilverbesserungen */
            .list-entry {
                border: 1px solid black;
                border-radius: 8px;
                margin-bottom: 2px;
                padding: 2px;
            }
    
            .list-entry div {
                padding: 1px 0;
            }
    
            .list-entry div:first-child {
                border-bottom: 1px solid #aaa;
                padding-bottom: 2px;
            }
    
            @media print {
                #filterGroup,
                #toggleFilter {
                    display: none;
                }
            }
    
            input[type="text"] {
                padding: 10px;
                border: 1px solid #aaa;
                border-radius: 4px;
                width: 80%;
            }
    
            button {
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                background-color: #007BFF;
                color: white;
                cursor: pointer;
            }
    
            button:hover {
                background-color: #0056b3;
            }
    
            #filterGroup {
                display: flex;
                align-items: center;
            }
    
            @media (max-width: 768px) {
                #filterGroup {
                    flex-direction: column;
                }
    
                input[type="text"] {
                    width: 100%;
                    margin-bottom: 10px;
                }
            }
        </style>\n 
    </head>
<body>"""

html_export_script = """
<script>
    const filterInput = document.getElementById('suchfilter');
    const toggleButton = document.getElementById('toggleFilter');
    const countSpan = toggleButton.querySelector('span');
    const filterGroup = document.getElementById('filterGroup');
    const entries = document.querySelectorAll('.list-entry');

    toggleButton.addEventListener('click', () => {
        if (filterGroup.style.display === 'none') {
            filterGroup.style.display = 'flex';
            filterInput.focus();
            updateButtonCount(entries.length);
            filterEntries(); // Filter the entries based on the current search text
        } else {
            filterGroup.style.display = 'none';
            toggleButton.firstElementChild.nodeValue = "Suche";
            countSpan.innerText = "";
        }
    });

    filterInput.addEventListener('keyup', filterEntries); // Filter the entries on keyup

    function filterEntries() {
        const searchTerms = filterInput.value.toLowerCase().split(' ');
        let visibleCount = 0;

        entries.forEach(entry => {
            const text = entry.innerText.toLowerCase();
            let allTermsFound = true;

            for (let term of searchTerms) {
                if (!text.includes(term)) {
                    allTermsFound = false;
                    break;
                }
            }

            if (allTermsFound) {
                entry.style.display = 'block';
                visibleCount++;
            } else {
                entry.style.display = 'none';
            }
        });

        updateButtonCount(visibleCount);
    }

    function updateButtonCount(visibleCount) {
        countSpan.innerText = `(${visibleCount} von ${entries.length})`;
    }
</script>
"""

html_export_searchfilter = """
<div style="display: flex; align-items: center;">
    <button id="toggleFilter">Suche<br><span></span></button>
    <div id="filterGroup" style="display: none; margin-left: 10px;">
        <label for="suchfilter" style="margin-right: 3px;">Filter:</label>
        <input type="text" id="suchfilter" placeholder="Suche...">
    </div>
</div>
"""

def filter_dict(input_dict) -> dict:
    """remove meta infos like DELETED_ or HOPS_ from dict with datacard meta info, and set delted marked values to '' """

    #collect keys to remove
    keys_to_remove = []
    for key, value in input_dict.items():
        if str(key).find("HOPS_") == 0 or str(key).find("DELETED_") == 0:
            #print(f"remove {key}")
            keys_to_remove.append(str(key))
        if len(str(value).strip()) == 0: # clear value when only whitespaces and tabs
            input_dict[key] = ""

    #revove the keys from dict
    for key in keys_to_remove:
        try:
            input_dict.pop(key)
        except:
            continue #uncritical -> continue

    return input_dict

def group_dict_keys(input_dict, grouping = "") -> dict:
    """groups multiple keys to one new key (example: keys street, zip_code, city, country  to  full_address)

    :param input_dict: dict where are keys to group
    :param grouping: string with the keyword to load the correct keys to group
    :return:
    """

    groups = {}
    #check which keys have to grouped
    if grouping == "business_card":
        #order important! the order of groups defines the order in html output
        groups = {'full_name': ['name', 'family_name'],
                  'full_address': ['street', 'zip_code', 'city', 'country']}
    else:
        return input_dict #no correct grouping found -> return same dict

    group = {}
    if not grouping == "":
        #build grouped keys
        for key, value in groups.items():
            #print(f"key: {key}")
            grouped_key = ""
            for item in value:
                try:
                    grouped_key += (f"{str(input_dict[item]).strip()} ") #strip removes whitespace at beginning and end
                except:
                    continue #uncritical -> continue
            group[key] = grouped_key.strip()

        input_dict = concat_dicts(group, input_dict)

        #remove grouped keys
        for key, value in groups.items():
            for item in value:
                try:
                    input_dict.pop(item)
                except:
                    continue # uncritical

    return input_dict

def generate_html_table(input_dict, type = "", filter_empty = True, extra_table_keys = [], extra_colums = False):

    htmlcode = ""
    newtable = ""
    htmlcode += '<table style="width:100%">\n'
    if extra_colums: # to show 2 keys with val in one colum
        even_row = False

    for key, value in input_dict.items():
        #dprint(f"keyval='{key}'=''{value}")
        if filter_empty and value == "":  # remove empty values from table
            continue
        val = str(value).replace("&", "&amp;")
        val = html.escape(val).replace('\n', '<br />\n')  # zeilenumbrüche umwandeln
        val = make_html_links(key, val)
        htmlcode += newtable
        newtable = ""
        if key in extra_table_keys:
            # print(f"neue tabelle ###################################### {key}")
            #if htmlcode != '<table  style="width:100%">\n':
            htmlcode += '</table>\n<table style="width:100%">\n'
            htmlcode += f'''<tr>\n  <td><b>{key_to_text(str(key), type)}:</b></td>\n</tr>\n'''
            htmlcode += f'''<tr>\n  <td>{adapt_text_value(key, val, type)}</td>\n</tr>\n'''

            newtable = '</table>\n<table  style="width:100%">\n'
            continue

        if extra_colums: # to show 2 keys with val in one colum
            if not even_row:
                htmlcode += '<tr>\n'
            htmlcode += f'  <td style="width:10%"><b>{key_to_text(str(key), type)}:</b></td>\n'
            htmlcode += f'  <td style="width:30%">{adapt_text_value(key, val, type)}</td>\n'
            if even_row:
                htmlcode += '</tr>\n'
            even_row = not even_row
            continue


        htmlcode += '<tr>\n'
        htmlcode += f'  <td style="width:10%"><b>{key_to_text(str(key), type)}:</b></td>\n'
        htmlcode += f'  <td>{adapt_text_value(key, val, type)}</td>\n'
        htmlcode += '</tr>\n'

    if extra_colums and even_row:
        htmlcode += f'  <td></td>\n'
        htmlcode += f'  <td></td>\n'
        htmlcode += '</tr>\n'

    htmlcode += '</table>\n'

    return htmlcode

def generate_html_export_table(input_dict, type = "", filter_empty = True, compact_mode = True):

    htmlcode = ""
    column_left = ""
    column_right = ""

    keys_left = ["full_name", "full_address", "name", "family_name", "card_id", "radius_of_activity", "street", "zip_code", "city", "country", "website",
                "coordinates", "company_profession", "phone", "email", "other_contact", "friend_ids", "local_id"]

    # keys which should be writen to text in the export
    keys_in_text = ["requests", "skills_offers", "tags", "interests_hobbies"]

    for key, value in input_dict.items():
        if filter_empty and value == "":  # remove empty values from table
            continue

        val = adapt_html_export_text_value(key, value, type)
        if compact_mode:
            val = make_text_compact(key, val)
        #val = str(val).replace("&", "&amp;")

        val = html.escape(str(val)).replace('\n', '<br />\n')  # zeilenumbrüche umwandeln
        val = make_html_links_for_export(key, val)

        if key in keys_left:
            column_left += val + " "
        else:
            if key in keys_in_text:
                column_right += f"<b>{key_to_text(str(key), type)}: </b>" + val + " "
            else:
                column_right += val + " "

    htmlcode += '<div class="list-entry">\n'
    htmlcode += f'  <div class="entry-part1">{column_left}</div>\n'
    htmlcode += f'  <div class="entry-part2">{column_right}</div>\n'
    htmlcode += '</div>\n'

    return htmlcode

def make_text_compact(key, text):
    """remove linebreaks or double whitespace etc. to save space an have a more compact text"""

    # adapt only the following keys
    keys_to_replace = ["requests", "skills_offers", "tags", "interests_hobbies"]
    if key in keys_to_replace:
        text = re.sub(' +',' ',text) # remove multiple whitespaces
        text = text.strip() # remove leading and trailing whitespaces
        text = text.replace("\n", ";") # replace newline with semicolon
        text = text.replace(";;", ";") # replace multiple semicolons with one semicolon
        text = text.replace(";", "; ") # add space after semicolon
        text = text.replace(",;", ";")
        text = text.replace(" ;", ";")
        if text.endswith("; "):
            text = text[:-2] # remove last semicolon

    return text

def generate_html_export_infohead(input_dict):
    """inserts the first line with infos to the export. Date, Location, Nummber of Entrys ..."""
    htmlcode = f"<p><b>Liste vom:</b> {input_dict['current_date']} -- "
    htmlcode += f"<b>Einträge:</b> {input_dict['number_of_entrys']} -- "
    if isValidCoordinate(input_dict['coordinates']):
        htmlcode += f"<b>Entfernungen von:</b> {input_dict['zip_code']} {input_dict['city']} ({input_dict['coordinates']})"
    htmlcode += "</p>"
    return htmlcode


def friend_data_to_html(content_dict, type = "", filter = False, full_html = False, filter_empty = False, grouping ="", own_filter_list = []):
    #content_dict = data_card_dict['data']

    htmlcode = ""
    if full_html:
        htmlcode += html_head

    #keys in extra_table_keys will become two rows, firstrow the head, second row the content (usually for long content)
    extra_table_keys = ['skills_offers', 'requests']

    htmlcode += '<table style="width:100%">\n'

    #remove own unwanted keys
    if own_filter_list != []:
        for el in own_filter_list:
            content_dict.pop(el)

    if filter:
        content_dict = filter_dict(content_dict)

    #try to group keys to on key with more content
    if grouping != "":
        content_dict = group_dict_keys(content_dict, grouping)

    #generate table
    htmlcode += generate_html_table(content_dict, type=type, extra_table_keys=extra_table_keys, filter_empty=filter_empty)

    if full_html:
        htmlcode += "</body>\n</html>\n" #insert end of html
    return htmlcode

def data_card_to_html(data_card_dict, show_details, type="", filter = False, full_html = False, filter_empty = False, grouping ="", own_filter_list = []):
    """
    :param input_dict: dict with values
    :param filter: bool to remove unwanted meta-info from data-card-dict
    :param full_html: bool inserts head and foot for complete html file
    :param filter_empty: bool to remove dict item from table if value of dict item is empty
    :param grouping: string: groups multiple keys to one new key (example: keys street, zip_code, city, country  to  full_address)
    :return: html-code
    """


    content_dict = data_card_dict['data']
    card_details = data_card_dict['dc_head']
    #extra_info.pop('card_id', None) # entferne card ID
    card_details['hops'] = data_card_dict['dc_dynamic_head']['hops']
    for el in ['type', 'deleted', 'version']: # filter out unwanted details in dc_head
        card_details.pop(el)


    htmlcode = ""
    if full_html:
        htmlcode += html_head

    #keys in extra_table_keys will become two rows, firstrow the head, second row the content (usually for long content)
    extra_table_keys = ['skills_offers', 'requests']


    #remove own unwanted keys
    if own_filter_list != []:
        for el in own_filter_list:
            content_dict.pop(el)

    if filter:
        content_dict = filter_dict(content_dict)

    #try to group keys to on key with more content
    content_dict = group_dict_keys(content_dict, grouping)
    #dprint(content_dict)
    #generate table

    htmlcode += generate_html_table(content_dict, type=type, extra_table_keys=extra_table_keys,filter_empty=filter_empty)
    if show_details:
        htmlcode += '<hr width=”100%”\n>'
        htmlcode += generate_html_table(card_details, type='card_details', extra_colums=True)

    if full_html:
        htmlcode += "</body>\n</html>\n" #insert end of html
    return htmlcode

def data_card_html_export(data_card_dict, type="", filter = False, filter_empty = False, grouping ="",
                          own_filter_list = [], compact_mode = True):
    """ needed to export all cards to a html file (for later printing or pdf generation)

    :param input_dict: dict with values
    :param filter: bool to remove unwanted meta-info from data-card-dict
    :param full_html: bool inserts head and foot for complete html file
    :param filter_empty: bool to remove dict item from table if value of dict item is empty
    :param grouping: string: groups multiple keys to one new key (example: keys street, zip_code, city, country  to  full_address)
    :return: html-code
    """

    content_dict = data_card_dict['data']
    card_details = data_card_dict['dc_head']
    card_details['hops'] = data_card_dict['dc_dynamic_head']['hops']
    for el in ['type', 'deleted', 'version']: # filter out unwanted details in dc_head
        card_details.pop(el)

    #remove own unwanted keys
    if own_filter_list != []:
        for el in own_filter_list:
            content_dict.pop(el)

    # remove not needed meta info etc.
    if filter:
        content_dict = filter_dict(content_dict)

    #try to group keys to on key with more content
    content_dict = group_dict_keys(content_dict, grouping)

    # order the dict, beginning with the local_id
    content_dict = order_dict(content_dict, ['local_id'])

    #generate table
    htmlcode = generate_html_export_table(content_dict, type=type,filter_empty=filter_empty, compact_mode=compact_mode)

    return htmlcode


def adapt_text_value(key, value, type) -> str:
    """change the text value of some special elements when on special conditions. for exaple to display good time format

    :param key: key of the dict
    :param value: value of the dict
    :param type: type of dict. (business_card, friend, ...)
    :return:
    """
    if type == "friend":
        if key == "active_friendship" and value == "1":
            return str("aktive Freundschaft")
        if key == "active_friendship" and value == "0":
            return str("Freundschaft abgelaufen")
        if key == "friend_since_date":
            return format_date_string(value) # nice date format
        if key == "expire_date":
            return format_date_string(value) # nice date format

    if type == "card_details":
        if key == "card_id":
            return value[:16] # shorten card_id to first 16 chars
        if key == "creator":
            return value[:16] # shorten creator to first 16 chars
        if key == "foreign_card" and value == "0":
            return str("Nein")
        if key == "foreign_card" and value == "1":
            return str("Ja")
        if key == "hops" and value == "0":
            return str("0 (eigener Eintrag)")
        if key == "hops" and value == "1":
            return str("1 (Eintrag vom Freund)")
        if key == "hops" and value == "2":
            return str("2 (Vom Freundesfreund)")
        if key == "created":
            return format_date_string(value) # nice date format
        if key == "valid_until":
            return format_date_string(value) # nice date format
        if key == "edited":
            return format_date_string(value) # nice date format

    if type == "business_card":
        if key == "radius_of_activity":
            return f"{value} km"

    return value # change nothing when unknown type
def adapt_html_export_text_value(key, value, type) -> str:
    """change the text value of some elements on html export

    :param key: key of the dict
    :param value: value of the dict
    :param type: type of dict. (business_card, friend, ...)
    :return:
    """

    if type == "business_card":
        if key == "radius_of_activity":
            return f"(Aktionsradius: {value}km)"
        if key == "local_id":
            return f"{value})"
        if key == "friend_ids":
            return f"(Freund: {str(value).split(',')[0]})"



    return value # change nothing when unknown type



def key_to_text(key, type) -> str:
    """for the correct display of the html output the keys need corresponding names

    :param key: key where the correct name is needed
    :return: string with the name for the key
    """
    key_text = {}
    if type == "business_card":
        key_text = {"full_name": "Name", "name": "Rufname", "family_name": "Familienname", "card_id": "Anzeigen-ID",
                "image": "Bild", "radius_of_activity": "Aktionsradius", "street": "Straße",
                "zip_code": "PLZ", "city": "Ort", "country": "Land", "website": "Internetseite",
                "coordinates": "Koordinaten", "company_profession": "Unternehmen / Beruf", "phone": "Telefon",
                "email": "E-Mail", "other_contact": "weiterer Kontakt", "interests_hobbies": "Interessen", "requests": "Gesuch",
                "skills_offers": "Angebot", "tags": "Stichwörter",
                "full_address": "Adresse", "friend_ids": "Freunde", "local_id": "Nr"}

    if type == "friend":
        key_text = {"name": "Name", "comment": "Kommentar", "active_friendship": "Freundschaftsstatus",
                "friend_since_date": "Freund seit", "expire_date": "Ablauf der Freundschaft", "pubkey_id": "Profil-ID",
                "publickey": "öffentlicher Schlüssel", "email": "E-Mail"}

    if type == "card_details":
            key_text = {"card_id": "ID", "creator": "Ersteller ID", "created": "Erstellt",
                    "valid_until": "Gültig bis", "expire_date": "Ablauf der Freundschaft", "edited": "letzte Bearbeitung",
                    "hops": "Freund-Distanz", "maxhop": "Max-Freund-Distanz", "foreign_card": "Fremdeintrag"}


    if key in key_text.keys():
        return key_text[key]
    return key
