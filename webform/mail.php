<?php
include 'settings.php'; // Settings / Einstellungen

// check if settings are correct, if not exit script
if ($from_email == "myemail@domain.com" || $from_email == "myemail@domain.com") {
  die("Fehler. Bitte E-Mail Adressen in settings.php anpassen.");
}

function esc($string) {
    $string = addslashes($string); // escape
    $string = str_replace(">", "/>", $string); // special escape > , needed for later parsing in python
    return $string;
}


//escaped for import
$name = esc($_POST['name']);
$family_name = esc($_POST['family_name']);
$street = esc($_POST['street']);
$zip_code = esc($_POST['zip_code']);
$city = esc($_POST['city']);
$country = esc($_POST['country']);
$radius_of_activity = esc($_POST['radius_of_activity']);
$company_profession = esc($_POST['company_profession']);
$phone = esc($_POST['phone']);
$website = esc($_POST['website']);
$email = esc($_POST['email']);
$other_contact = esc($_POST['other_contact']);
$interests_hobbies = esc($_POST['interests_hobbies']);
$skills_offers = esc($_POST['skills_offers']);
$requests = esc($_POST['requests']);
$tags = esc($_POST['tags']);
$maxhop = esc($_POST['maxhop']);
$card_type = "<card_type>business_card<card_type>\n";  // placeholder for more possible contents (ads, events, ...)
$message_to_collector = esc($_POST['message_to_collector']);
$entry_type = esc($_POST['entry_type']);


$entrant_email = esc($_POST['email']);
$collector_info = "Hinweis: Den Inhalt dieser Mail unveraendert einfach kopieren und mit TalentTalent importieren.\nZur zusaetzlichen Sicherheit eventuell warten bis der Eintrager die Mail nochmal weiterleitet.";
$mailcontent_collector="<name>$name<name>\n<family_name>$family_name<family_name>\n<street>$street<street>\n<zip_code>$zip_code<zip_code>\n<city>$city<city>\n<country>$country<country>\n<radius_of_activity>$radius_of_activity<radius_of_activity>\n<company_profession>$company_profession<company_profession>\n<phone>$phone<phone>\n<website>$website<website>\n<email>$email<email>\n<other_contact>$other_contact<other_contact>\n<interests_hobbies>$interests_hobbies<interests_hobbies>\n<skills_offers>$skills_offers<skills_offers>\n<requests>$requests<requests>\n<tags>$tags<tags>\n<maxhop>$maxhop<maxhop>\n\n\nEintragungstyp: $entry_type\n\nEintrag von: $name $family_name  ($street $zip_code $city $country)\nNachricht:$message_to_collector\n\n\n$collector_info";
$entrant_info = "WICHTIG! Antworte nochmal kurz auf diese Mail, um die Eintragung zu bestaetigen! Folgender Inhalt wird dann in die Liste eingetragen.\n\n";
$mailcontent_entrant = $entrant_info . "Name:\t$name\nFamilienname:\t$family_name\nStrasse:\t$street\nPLZ:\t$zip_code\nOrt:\t$city\nLand:\t$country\nAktivitaetsradius:\t$radius_of_activity\nUnternehmen/Beruf:\t$company_profession\nTelefon:\t$phone\nInternetseite:\t$website\nE-Mail:\t$email\nSonstiger Kontakt:\t$other_contact\nInteressen/Hobbies:\t$interests_hobbies\nAngebot/Faehigkeiten:\t$skills_offers\nGesuch:\t$requests\nStichwoerter:\t$tags\n\nmax Reichweite zum teilen:\t$maxhop\n\nEintragungstyp:\t $entry_type\n\nDeine Nachricht:\t$message_to_collector";
$mailcontent_entrant = stripslashes($mailcontent_entrant);  //unescape the text and decode html-special-chars
$headers = "From: $from_email \r\n"; // Add the cc header
mail($recipient, $subject, ($card_type . $mailcontent_collector), $headers) or die("Fehler!"); // mail to collector

$headers_entrant = "From: $from_email \r\n"; // Add the cc header
mail($entrant_email, $subject, $mailcontent_entrant, $headers_entrant) or die("Fehler!"); // Mail to the entrant


echo '<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>';
echo htmlentities("Vielen Dank für die Eintragung. Du solltest gleich eine E-Mail an $email erhalten. (Notfalls im Spam Ordner nachschauen.)");
echo "</br></br><strong>";
echo htmlentities("Antworte dem Verwalter der Liste nochmal kurz auf diese Mail.");
echo "</strong>";
echo htmlentities(" (Dient zur Überprüfung, ob dies auch tatsächlich deine E-Mail Adresse ist.)");
echo "</p>";
?>