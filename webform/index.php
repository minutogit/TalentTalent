<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  /* Grundlegende Styling-Optionen */
  * {
    box-sizing: border-box;
    font-family: Arial, sans-serif;
  }

  body {
    background-color: #E8F4E5;
  }

  .container {
    background-color: #B2DFC8;
    border-radius: 10px;
    margin: 20px auto;
    max-width: 1000px;
    padding: 20px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.2);
  }

  h1 {
    text-align: center;
    color: #045D45;
  }

  label, legend {
    color: #045D45;
    font-weight: bold;
    margin-top: 5px;  /* 5px Platz oberhalb des Labels */
  }

  input[type=text], input[type=email], input[type=number], input[type=tel], select, textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #89C7A7;
    border-radius: 8px;
    background-color: #ffffff;
    transition: background-color 0.3s;
  }

  input[type=text]:focus, input[type=email]:focus, input[type=number]:focus, input[type=tel]:focus, select:focus, textarea:focus {
    background-color: #E1F9E8;
  }

  button[type=submit] {
    background-color: #15AC5D;
    color: white;
    margin: 5px 0; /* 5px Platz ober- und unterhalb des Buttons */
    padding: 12px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  button[type=submit]:hover {
    background-color: #129448;
  }

  /* Styling für das Layout */
  .col-left {
    float: left;
    width: 30%;
    margin-top: 6px;
  }

  .col-right {
    float: left;
    width: 70%;
    margin-top: 6px;
  }

  .row:after {
    content: "";
    display: table;
    clear: both;
  }
.refresh-btn {
    background-color: #f4f4f4; /* Hintergrundfarbe des Buttons */
    border: 1px solid #ccc; /* Rahmen des Buttons */
    padding: 2px 10px; /* Innenabstand des Buttons */
    cursor: pointer; /* Hand-Cursor beim Überfahren des Buttons */
    font-size: 14px; /* Schriftgröße des Buttons */
    transition: background-color 0.3s; /* sanfte Farbübergangsanimation */
    margin: 5px 0; /* Abstand oben und unten um den Button herum */
}

.refresh-btn:hover {
    background-color: #e6e6e6; /* Hintergrundfarbe des Buttons beim Überfahren */
}

.refresh-btn i {
    margin-right: 5px; /* Abstand zwischen dem Icon und dem Text */
}
    @media screen and (max-width: 800px) {
      .col-left, .col-right {
        width: 100%;
      }

      .col-left {
        margin-top: 10px;
      }

      button[type=submit] {
        margin-top: 5px;
        margin-bottom: 5px;
      }
    }

    footer {
      text-align: center;
      margin-top: 0px;
      padding: 0px;
    }

    .captcha_style {
      float: left;
      width: 200px;
      margin-top: 10px;
    }
</style>

</head>
<body onload="generateCaptcha(event);">
  <div class="container">
  <h1 style="text-align: center;">Regional vernetzt - Angebotsliste</h1>
  <p>Gegenseitige Unterst&uuml;tzung und Zusammenarbeit sind das Gebot der Stunde. Was sind deine F&auml;higkeiten
  und Talente? Wo kannst du gelegentlich Unterst&uuml;tzung gebrauchen?</br>Trage nur Informationen ein, mit denen du einverstanden bist, wenn sie ggf. von vielen anderen Menschen eingesehen werden k&ouml;nnen.</br>Wenn du dich eingetragen hast, erh&auml;ltst du
    gelegentlich per E-Mail eine Liste mit Angeboten / Gesuchen von Menschen aus deiner Region, die offen
    sind f&uuml;r alternative Tauschsysteme oder einfach nur helfen wollen.</p>
  </div>
  <p></p>
  <div class="container">
    <form action="mail.php" method="POST" onsubmit="return validateForm()" name="myForm">
      <fieldset  class="fieldset1">
        <legend>Adressdaten</legend>
        <div class="row">
          <div class="col-left">
            <label for="name">Rufname*</label>
          </div>
          <div class="col-right">
            <input type="text" id="name" name="name" placeholder="Dein Rufname" required>
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="family_name">Familien Name</label>
          </div>
          <div class="col-right">
            <input type="text" id="family_name" name="family_name" placeholder="Dein Familienname">
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="company_profession">Unternehmen / Beruf</label>
          </div>
          <div class="col-right">
            <input type="text" id="company_profession" name="company_profession" placeholder="">
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="street">Stra&szlig;e</label>
          </div>
          <div class="col-right">
            <input type="text" id="street" name="street" placeholder="">
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="zip_code">PLZ*</label>
          </div>
          <div class="col-right">
            <input type="number" id="zip_code" name="zip_code" placeholder="Postleitzahl ..." required>
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="city">Ort*</label>
          </div>
          <div class="col-right">
            <input type="text" id="city" name="city" placeholder="Stadt / Wohnort" required>
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="country">Land</label>
          </div>
          <div class="col-right">
            <input type="text" id="country" name="country" placeholder="">
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="radius_of_activity">Aktivit&auml;tsradius (in km)</label>
          </div>
          <div class="col-right">
            <input type="number" id="radius_of_activity" name="radius_of_activity" placeholder="In welchem Umkreis bist du regional aktiv? z.B. 10km">
          </div>
        </div>
      </fieldset>
      <fieldset  class="fieldset1">
      <legend>Kontaktm&ouml;glichkeiten</legend>
        <div class="row">
          <div class="col-left">
            <label for="phone">Telefon</label>
          </div>
          <div class="col-right">
            <input type="tel" id="phone" name="phone" placeholder="">
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="website">Internetseite</label>
          </div>
          <div class="col-right">
            <input type="text" id="website" name="website" placeholder="www...">
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="email">E-Mail*</label>
          </div>
          <div class="col-right">
            <input type="email" id="email" name="email" placeholder="meine@e-mail.de" required>
          </div>
        </div>
        <div class="row">
          <div class="col-left">
            <label for="other_contact">Sonstiges</label>
          </div>
          <div class="col-right">
            <input type="text" id="other_contact" name="other_contact" placeholder="Sonstige Kontaktm&ouml;glichkeiten">
          </div>
        </div>
      </fieldset>
      <fieldset  class="fieldset1">
      <legend>Angebote, Gesuche, ...</legend>
      <div class="row">
        <div class="col-left">
          <label for="interests_hobbies">Interesssen Hobbys</label>
        </div>
        <div class="col-right">
          <input type="text" id="interests_hobbies" name="interests_hobbies" placeholder="Um eventuell Gleichgesinnte zu finden.">
        </div>
      </div>
      <div class="row">
        <div class="col-left">
          <label for="skills_offers">Angebote, F&auml;higkeiten*</label>
        </div>
        <div class="col-right">
          <textarea id="skills_offers" name="skills_offers"
                    placeholder="Was kannst du alles? Womit kannst du anderen helfen? Was stellst du her? Was bereitet dir Freude? (Stichpunktartig auf den Punkt bringen. Wenn m&ouml;glich, keine langen S&auml;tze.)" style="height:150px" required></textarea>
        </div>
      </div>
      <div title="Damit andere Wissen was du gebrauchen kannst und der Austausch in Gang kommt." class="row">
        <div class="col-left">
          <label for="requests">Gesuche*</label>
        </div>
        <div class="col-right">
          <textarea id="requests" name="requests"
                    placeholder="Was kannst du gebrauchen? Was w&uuml;rdest du in Anspruch nehmen? Was h&auml;ttest du gerne im regionalen Netzwerk?"
                    style="height:100px" required></textarea>
        </div>
      </div>
      <div title="F&uuml;r zum Beispiel Hinweise auf Tauschsysteme, Gruppen oder Sonstiges in einem Wort." class="row">
        <div class="col-left">
          <label for="tags">Stichw&ouml;rter</label>
        </div>
        <div class="col-right">
          <input type="text" id="tags" name="tags" placeholder="z.B. Minuto, Helfa, Gradido (Gruppename, Zahlungsmittel, ..)">
        </div>
      </div>
      </fieldset>
      <fieldset  class="fieldset1">
        <div class="row">
        <?php if (!(isset($_GET['id']) && isset($_GET['key']))): ?>
          <label>
        <input type="radio" id="new_entry2" name="entry_type" value="Neueintrag" required> Bitte neu eintragen
        </label>
        <?php endif; ?>
        <label>
          <input type="radio" id="update_entry2" name="entry_type" value="Eintrag aktualisieren" required> Meinen Eintrag aktualisieren
        </label>
        <label>
          <input type="radio" id="remove_entry2" name="entry_type" value="Eintragung l&ouml;schen" required> Meinen Eintrag aus der Liste l&ouml;schen
        </label>
        </div>
      </fieldset>
      <div class="row">
        <div class="col-left">
          <label for="requests">Nachricht an den Listenverwalter</label>
        </div>
        <div class="col-right">
          <textarea id="message_to_collector" name="message_to_collector"
                    placeholder="Schreibe bei Bedarf eine Nachricht / Hinweis an den lokalen Verwalter der Liste."
                    style="height:100px"></textarea>
        </div>
      </div>

      <div class="row">
      <div class="captcha_style">
        <label>Code</label>
        <div>
          <input style="color:red;" type="text" name="maincaptcha" readonly id="mainCaptcha"/>
          <button onclick="generateCaptcha(event);" id="refresh" class="refresh-btn"><i style="font-size:17px"></i>Code erneuern</button>
        </div>
      </div>
      </div>
      <div class="row">
        <div class="captcha_style">
          <label>Code wiederholen:</label>
          <input type="number" name="checkcaptcha" id="txtInput"/>
        </div>
      </div>
      <div class="row">
        <span id="error" style="color:red;"></span>
        <span id="success" style="color:green;"></span>
      </div>
      <button type="submit" >   Senden   </button>
        <?php if (isset($_GET['id']) && isset($_GET['key'])): ?>
            <input type="hidden" name="id" value="<?php echo htmlspecialchars($_GET['id'], ENT_QUOTES, 'UTF-8'); ?>">
            <input type="hidden" name="key" value="<?php echo htmlspecialchars($_GET['key'], ENT_QUOTES, 'UTF-8'); ?>">
        <?php endif; ?>
    </form>
  </div>
  <script type="text/javascript">
   <?php
    include 'settings.php'; // Settings / Einstellungen

    function deriveIVfromID($id) {
        // Hash the ID with SHA-256
        $hashedID = hash('sha256', $id, true);

        // Return the first 16 bytes of the hashed value as the IV
        return substr($hashedID, 0, 16);
    }

    function CustomDecrypt($encryptedData, $key, $id) {
        // Derive IV from ID
        $iv = deriveIVfromID($id);

        // Decode the encrypted data from base64
        $decodedData = base64_decode($encryptedData);

        // Decrypt the data using AES-256-CBC
        $data = openssl_decrypt($decodedData, 'aes-256-cbc', $key, 0, $iv);

        // Return the decrypted data
        return $data;
    }
    function decryptData($encryptedData, $key, $id) {
        // Implement decryption logic using AES or any other encryption algorithm
        $decryptedData = CustomDecrypt($encryptedData, $key, $id); // Implement AES decryption function
        return $decryptedData;
    }

    // Check if ID and key are provided in the query parameters
    if (isset($_GET['id']) && isset($_GET['key'])) {
        // Retrieve ID and key from query parameters
        $id = $_GET['id'];
        $key = $_GET['key'];

        $temptxtFile = 'encrypted-form-data/' . $id . '.temptxt';
        $txtFile = 'encrypted-form-data/' . $id . '.txt';
        $fileToRead = '';

        // Determine which file to read
        if (file_exists($temptxtFile)) {
            $fileToRead = $temptxtFile;
        } elseif (file_exists($txtFile)) {
            $fileToRead = $txtFile;
        }
        if(file_exists($fileToRead)) {
            $encryptedData = file_get_contents($fileToRead);

            // Decrypt the data
            $decryptedData = decryptData($encryptedData, $key, $id);
            //echo $decryptedData;

            // Check if decryption is successful
            if ($decryptedData !== false) {
                 // Extract the form fields from the decrypted data
                list($name, $family_name, $street, $zip_code, $city, $country, $radius_of_activity, $company_profession, $phone, $website, $email, $other_contact, $interests_hobbies, $skills_offers, $requests, $tags, $message_to_collector, $entry_type) = explode('|', $decryptedData);

                // Decode the URL-encoded form fields
                $name = urldecode($name);
                $family_name = urldecode($family_name);
                $street = urldecode($street);
                $zip_code = urldecode($zip_code);
                $city = urldecode($city);
                $country = urldecode($country);
                $radius_of_activity = urldecode($radius_of_activity);
                $company_profession = urldecode($company_profession);
                $phone = urldecode($phone);
                $website = urldecode($website);
                $email = urldecode($email);
                $other_contact = urldecode($other_contact);
                $interests_hobbies = urldecode($interests_hobbies);
                $skills_offers = urldecode($skills_offers);
                $requests = urldecode($requests);
                $tags = urldecode($tags);
                $message_to_collector = urldecode($message_to_collector);
                $entry_type = urldecode($entry_type);

                $variables = compact('name', 'family_name', 'street', 'zip_code', 'city', 'country', 'radius_of_activity', 'company_profession', 'phone', 'website', 'email', 'other_contact', 'interests_hobbies', 'skills_offers', 'requests', 'tags', 'message_to_collector', 'entry_type');

                // Echo the variables as JavaScript
                echo "var formData = " . json_encode($variables) . ";";
                // Rename .temptxt file to .txt and send confirmation mail
                if ($fileToRead === $temptxtFile) {
                    echo "alert(\"$website_alert_confirmation_text\");"; // JavaScript alert for confirmation
                    $headers = "From: $from_email \r\n";
                    $headers .= "Content-Type: text/plain; charset=UTF-8 \r\n";

                    // send the email
                    mail($recipient, ($confirmation_mail_subject . " ID-" . $id), $confirmation_mail_text, $headers);
                    $renameResult = rename($temptxtFile, $txtFile);

                }
            } else {
              // if decryption fails go to index.php
              echo "alert(\"Daten nicht gefunden.\");"; // JavaScript alert
              echo 'window.location.href = "index.php";
              </script></body></html>';
              exit;
            }
        } else {
            // if file not exists go to index.php
            echo "alert(\"Daten nicht gefunden.\");"; // JavaScript alert
            echo 'window.location.href = "index.php";
            </script></body></html>';
            exit;
        }
    }
    ?>

    if (typeof formData !== 'undefined') {
        document.getElementById('name').value = formData.name;
        document.getElementById('family_name').value = formData.family_name;
        document.getElementById('street').value = formData.street;
        document.getElementById('zip_code').value = formData.zip_code;
        document.getElementById('city').value = formData.city;
        document.getElementById('country').value = formData.country;
        document.getElementById('radius_of_activity').value = formData.radius_of_activity;
        document.getElementById('company_profession').value = formData.company_profession;
        document.getElementById('phone').value = formData.phone;
        document.getElementById('website').value = formData.website;
        document.getElementById('email').value = formData.email;
        document.getElementById('other_contact').value = formData.other_contact;
        document.getElementById('interests_hobbies').value = formData.interests_hobbies;
        document.getElementById('skills_offers').value = formData.skills_offers;
        document.getElementById('requests').value = formData.requests;
        document.getElementById('tags').value = formData.tags;
        document.getElementById('message_to_collector').value = formData.message_to_collector;
    }

        function generateCaptcha(event) {
            event.preventDefault();
            const alpha = '0123456789';
            let code = '';
            for (let i = 0; i < 4; i++) {
                code += alpha[Math.floor(Math.random() * alpha.length)];
            }
            const el = document.getElementById("mainCaptcha");
            el.value = code;
            el.style.fontFamily = 'Geneva, Verdana, sans-serif';
            el.style.fontSize = 'large';
        }


       //validate the form
       function validateForm() {
          let x = document.forms["myForm"]["checkcaptcha"].value;
          let y = document.forms["myForm"]["maincaptcha"].value;

          if (x == "") {
              document.getElementById('error').innerHTML = "Bitte den Code eingeben.";
              return false;
          }
          if(x!==y){
              document.getElementById('error').innerHTML = "Code stimmt nicht!";
              return false;
          }
          if(x===y){
              document.getElementById('error').innerHTML = "";
            //  alert("Captcha entered successfully");
              return true;
          }
        }
       // automatically generate captcha after page laod
        $(window).on('load', function () {
            generateCaptcha(event);
        });
   </script>

</body>
<footer>
  <p>Die Angebotsliste wird verwaltet mit: <a href="https://github.com/minutogit/TalentTalent/">TalentTalent</a>.</p>
</footer>
</html>