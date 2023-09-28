<?php
// preventing sending an empty mail when this file is loaded directly (without webform before)
if (!isset($_POST['email']) || $_POST['email'] == "") {
    die("-");
}

include 'settings.php'; // Settings / Einstellungen
$base_url = "webform.domain.com";  // url of the webform


// check if settings are correct, if not exit script
if ($from_email == "myemail@domain.com" || $from_email == "myemail@domain.com") {
  die("Fehler. Bitte E-Mail Adressen in settings.php anpassen.");
}

function deriveIVfromID($id) {
    // Hash the ID with SHA-256
    $hashedID = hash('sha256', $id, true);

    // Return the first 16 bytes of the hashed value as the IV
    return substr($hashedID, 0, 16);
}

function CustomEncrypt($data, $key, $id) {
    // Derive IV from ID
    $iv = deriveIVfromID($id);

    // Encrypt the data using AES-256-CBC
    $encryptedData = openssl_encrypt($data, 'aes-256-cbc', $key, 0, $iv);

    // Return the result as a base64-encoded string
    return base64_encode($encryptedData);
}


function encryptData($name, $family_name, $street, $zip_code, $city, $country, $radius_of_activity, $company_profession, $phone, $website, $email, $other_contact, $interests_hobbies, $skills_offers, $requests, $tags, $message_to_collector, $entry_type, $key, $id) {
  // Implement encryption logic using AES or any other encryption algorithm
  // Concatenate form fields and separate them with a unique separator (e.g., '|')
$data = urlencode($name) . '|' .
        urlencode($family_name) . '|' .
        urlencode($street) . '|' .
        urlencode($zip_code) . '|' .
        urlencode($city) . '|' .
        urlencode($country) . '|' .
        urlencode($radius_of_activity) . '|' .
        urlencode($company_profession) . '|' .
        urlencode($phone) . '|' .
        urlencode($website) . '|' .
        urlencode($email) . '|' .
        urlencode($other_contact) . '|' .
        urlencode($interests_hobbies) . '|' .
        urlencode($skills_offers) . '|' .
        urlencode($requests) . '|' .
        urlencode($tags) . '|' .
        urlencode($message_to_collector) . '|' .
        urlencode($entry_type);
  $encryptedData = CustomEncrypt($data, $key, $id); // Implement AES encryption function
  return $encryptedData;
}

function generateRandomKey() {
  // Generate a random key using the OpenSSL library
  $key = openssl_random_pseudo_bytes(16); // 16 bytes = 128 bits
  // Convert the binary key to hexadecimal representation
  $hexKey = bin2hex($key);
  return $hexKey;
}

function esc($string) {
    $string = addslashes($string); // escape
    $string = str_replace(">", "/>", $string); // special escape > , needed for later parsing in python
    return $string;
}

//variables
$name = $_POST['name'];
$family_name = $_POST['family_name'];
$street = $_POST['street'];
$zip_code = $_POST['zip_code'];
$city = $_POST['city'];
$country = $_POST['country'];
$radius_of_activity = $_POST['radius_of_activity'];
$company_profession = $_POST['company_profession'];
$phone = $_POST['phone'];
$website = $_POST['website'];
$email = $_POST['email'];
$other_contact = $_POST['other_contact'];
$interests_hobbies = $_POST['interests_hobbies'];
$skills_offers = $_POST['skills_offers'];
$requests = $_POST['requests'];
$tags = $_POST['tags'];
$card_type = "<card_type>business_card<card_type>\n";  // placeholder for more possible contents (ads, events, ...)
$message_to_collector = $_POST['message_to_collector'];
$entry_type = $_POST['entry_type'];



$confirmation_needed = true;
$folder = 'encrypted-form-data/';

// Check if ID, key are received from the form, and if the corresponding .txt file exists
if (isset($_POST['id']) && isset($_POST['key']) && file_exists($folder . $_POST['id'] . '.txt')) {
    $id = $_POST['id'];
    $key = $_POST['key'];
    $file_extension = '.txt';
    $confirmation_needed = false;
} else {
    // Generate random ID and key only if not received from form
    $id = uniqid();
    $key = generateRandomKey();
    //temp file will be renamed to txt (for mail-verification / and temp files will be deleted earlier to save space when Spam)
    $file_extension = '.temptxt';
}

// Encrypt form data
$encryptedData = encryptData($name, $family_name, $street, $zip_code, $city, $country, $radius_of_activity, $company_profession, $phone, $website, $email, $other_contact, $interests_hobbies, $skills_offers, $requests, $tags, $message_to_collector, $entry_type, $key, $id); // Implement encryption function

// Check if the folder exists, and if not, create it
if (!file_exists($folder)) {
    mkdir($folder, 0777, true); // Creates the folder recursively
}

// Save encrypted data to a file on the server
$file = $folder . $id . $file_extension;
file_put_contents($file, $encryptedData);



// Determine the protocol
$protocol = (isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on') ? "https://" : "http://";
// Get the domain name
$domainName = $_SERVER['HTTP_HOST'];
// Get the folder/directory name
$folder = dirname($_SERVER['PHP_SELF']);
// Construct the base URL
$base_url = $protocol . $domainName . $folder;
// Add ID and key as query parameters in the email link
$encryptedLink = $base_url . 'index.php?id=' . urlencode($id) . '&key=' . urlencode($key);



$entrant_email = esc($_POST['email']);
if ($confirmation_needed) {
    $collector_info = "Hinweis: Den Inhalt dieser Mail unveraendert einfach kopieren und mit TalentTalent importieren.\nZur zusaetzlichen Sicherheit eventuell warten bis der Eintrag bestaetigt wurde.";
} else {
    $collector_info = "Hinweis: Den Inhalt dieser Mail unveraendert einfach kopieren und mit TalentTalent importieren.\n Wenn neu importiert wird muss alter Eintrag eventuell noch geloescht werden.";
}

$mailcontent_collector = "<name>" . esc($name) . "<name>\n";
$mailcontent_collector .= "<family_name>" . esc($family_name) . "<family_name>\n";
$mailcontent_collector .= "<street>" . esc($street) . "<street>\n";
$mailcontent_collector .= "<zip_code>" . esc($zip_code) . "<zip_code>\n";
$mailcontent_collector .= "<city>" . esc($city) . "<city>\n";
$mailcontent_collector .= "<country>" . esc($country) . "<country>\n";
$mailcontent_collector .= "<radius_of_activity>" . esc($radius_of_activity) . "<radius_of_activity>\n";
$mailcontent_collector .= "<company_profession>" . esc($company_profession) . "<company_profession>\n";
$mailcontent_collector .= "<phone>" . esc($phone) . "<phone>\n";
$mailcontent_collector .= "<website>" . esc($website) . "<website>\n";
$mailcontent_collector .= "<email>" . esc($email) . "<email>\n";
$mailcontent_collector .= "<other_contact>" . esc($other_contact) . "<other_contact>\n";
$mailcontent_collector .= "<interests_hobbies>" . esc($interests_hobbies) . "<interests_hobbies>\n";
$mailcontent_collector .= "<skills_offers>" . esc($skills_offers) . "<skills_offers>\n";
$mailcontent_collector .= "<requests>" . esc($requests) . "<requests>\n";
$mailcontent_collector .= "<tags>" . esc($tags) . "<tags>\n\n";
$mailcontent_collector .= "Eintragungstyp: " . esc($entry_type) . "\n\n";
$mailcontent_collector .= "Eintrag von: " . esc($name . ' ' . $family_name) . "  (" . esc($street . ' ' . $zip_code . ' ' . $city . ' ' . $country) . ")\n";
$mailcontent_collector .= "Nachricht:" . esc($message_to_collector) . "\n\n\n";
$mailcontent_collector .= $collector_info;



if ($confirmation_needed) {
    $entrant_info = "WICHTIG! Klicke den folgenden Link um die Eintragung zu bestaetigen! Bei Bedarf kannst du damit auch Aenderungen vornehmen.\n$encryptedLink\n\n";

} else {
    $entrant_info = "Hier mit dem Link kannst du Aenderungen vornehmen.\n$encryptedLink\n\n";
}

$mailcontent_entrant = $entrant_info . "Name:\t$name\nFamilienname:\t$family_name\nStrasse:\t$street\nPLZ:\t$zip_code\nOrt:\t$city\nLand:\t$country\nAktivitaetsradius:\t$radius_of_activity\nUnternehmen/Beruf:\t$company_profession\nTelefon:\t$phone\nInternetseite:\t$website\nE-Mail:\t$email\nSonstiger Kontakt:\t$other_contact\nInteressen/Hobbies:\t$interests_hobbies\nAngebot/Faehigkeiten:\t$skills_offers\nGesuch:\t$requests\nStichwoerter:\t$tags\n\nEintragungstyp:\t $entry_type\n\nDeine Nachricht:\t$message_to_collector\n";
$mailcontent_entrant = stripslashes($mailcontent_entrant);  //unescape the text and decode html-special-chars
$headers = "From: $from_email \r\n"; // Add the cc header

if ($confirmation_needed) {
    mail($recipient, ($subject . " ID-" . $id), ($card_type . $mailcontent_collector), $headers) or die("Fehler!"); // mail to collector
} else {
    mail($recipient, ($subject_confirmed . " ID-" . $id), ($card_type . $mailcontent_collector), $headers) or die("Fehler!"); // mail to collector
}

$headers_entrant = "From: $from_email \r\n"; // Add the cc header
mail($entrant_email, $subject, $mailcontent_entrant, $headers_entrant) or die("Fehler!"); // Mail to the entrant


echo '<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>';
echo htmlentities("Vielen Dank für die Eintragung. Du solltest gleich eine E-Mail an $email erhalten. (Notfalls im Spam Ordner nachschauen.)");
if ($confirmation_needed) {
    echo "</br></br><strong>";
    echo htmlentities("Bitte bestätige deine Eintragung in dem du den Bestätigungslink in der Mailadresse anklickst!");
    echo "</strong>";
    echo htmlentities(" (Dient zur Überprüfung, ob dies auch tatsächlich deine E-Mail Adresse ist.)");
    echo "</p>";
}

// delete automatically old files to keep server clean
// Read the last run date
$last_run_file = 'last_run.txt';
if (file_exists($last_run_file)) {
    $last_run_date = file_get_contents($last_run_file);
    $last_run_timestamp = strtotime($last_run_date);
} else {
    $last_run_timestamp = 0;  // Set an old timestamp
}

$current_date = date('Y-m-d');
$current_timestamp = strtotime($current_date);
// keep files at least one year (to prevent wrong user settings)
if ($delete_files_after_years < 1) {
    $delete_files_after_years = 1;
}

// If the current date is not equal to the last run date
if ($current_timestamp != $last_run_timestamp) {
    // Record the current date as the last run date
    file_put_contents($last_run_file, $current_date);

    // Now, handle the deletion of old files
    $files = glob('encrypted-form-data/*'); // gets all the files in the directory
    foreach ($files as $file) {
        if (is_file($file)) {
            $file_last_modified_time = filemtime($file);
            if (strpos($file, '.temptxt') !== false && time() - $file_last_modified_time >= 30 * 24 * 60 * 60) {
                // If it's a '.temptxt' file and older than 1 month, delete
                unlink($file);
            } elseif (strpos($file, '.txt') !== false && time() - $file_last_modified_time >= $delete_files_after_years * 365.25 * 24 * 60 * 60) {
                // If it's a '.txt' file and older than the specified number of years, delete
                unlink($file);
            }
        }
    }
}

?>