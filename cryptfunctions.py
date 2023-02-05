# from icecream import ic #ic for debugging ouputs while coding (better than print) https://github.com/gruns/icecream

from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import HMAC, SHA256, SHAKE128
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.PublicKey import RSA
from struct import pack
import base64, os, hashlib, binascii, struct, zlib, json
from mnemonic import mnemonic
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
#import hashlib
import functions
from functions import dprint

# opencv-python  - remove

class profiles_management():
    def __init__(self):
        self.user_pw = ""
        self.user_pw_salt = ""
        self.aes_key_salt = ""
        self.encrypted_key = ""
        self.decrypted_key = ""
        self.rsa_key_word_seeds = []  # the firs word seed ist the normal used identity, (later possible more than one identity)
        self.rsa_key_pairs = []  # list of rsa keypairs (digital identitys) derived from word seeds
        self.start_profile_exist = False

    def save_profile(self):
        """save the profile to the file profile.dat

        profile = {}

        :return:
        """
        pass


class CryptoClass:
    def __init__(self):
        pass

    class Profile():
        """
        Class for Profile Management.
        """
        user_pw_salt = ""  # salt for hashing the user password
        user_pw_hash = ""  # salted hash of the user password
        profile_name = ""  # used to give the profile a name. shown in main window title
        profile_id = ""  # ID of the main profile, needed for password reset to check if seed words is identical
        pubkey_string = ""  # stores the exported pupbkey as string

        aes_key_salt = ""  # salt for deriving aes key
        aes_key = ""  # aes key is the derived hash of the entered password and aes_key_salt
        old_aes_key = ""  # needed for password change

        private_key = None  # key need for identity
        rsa_seed_words = ""  # seed words to derive rsa key, temporary used to generate rsa_key_pair
        rsa_key_pair = None  # rsa keypair derived from private key

        rsa_key_pair_id = None  # rsa keypair id (derived from public key, same as profile id)
        profile_exist = False  # store if profile file exists
        profile_is_initialized = False  # set to True when when Profile correct initialized with user-password
        aes_encrypted_private_key = None  # load at startup
        aes_encrypted_seed_words = None
        database_key = None  # key when db encryption is enabled (derived from seed words)
        aes_encrypted_database_key = None

    def close_profile(self):
        """used to close the profile on logout - resets all profile values"""
        self.Profile.user_pw_salt = ""
        self.Profile.user_pw_hash = ""
        self.Profile.profile_name = ""
        self.Profile.profile_id = ""
        self.Profile.pubkey_string = ""
        self.Profile.aes_key_salt = ""  # salt for deriving aes key
        self.Profile.aes_key = ""  # aes key is the derived hash of the entered password and aes_key_salt
        self.Profile.old_aes_key = ""  # needed for password change
        self.Profile.private_key = None  # the first key the normal used identity, (later possible more than one identity)
        self.Profile.rsa_seed_words = ""  # temporary used to generate rsa_key_pair
        self.Profile.rsa_key_pair = None  # list of rsa keypairs (digital identitys) derived from private key
        self.Profile.rsa_key_pair_id = None  # list of rsa keypairs ids (derived from public key)
        self.Profile.profile_is_initialized = False  # set to True when when Profile correct initialized with user-password
        self.Profile.aes_encrypted_private_key = None  # load at startup
        self.Profile.aes_encrypted_seed_words = None
        self.Profile.aes_encrypted_database_key = None
        self.Profile.database_key = None # key when db encryption is enabled (derived from seed words)

    def seed_is_identic_with_profile_seed(self):
        """used to check if the same seed words are used, when the user forgots the password and want to set a new one"""
        if not self.Profile.profile_exist:
            return False  # seed can't be checked because no old profile founf
        rsa_keypair = self.generate_rsa_key(self.Profile.rsa_seed_words)
        profile_id_from_seed = self.get_publickey_id(self.rsapubkey_to_rsapukeystring(rsa_keypair.publickey()))
        #print("profile_ids newsedd and profile_seed:", profile_id_from_seed, self.Profile.profile_id)
        if profile_id_from_seed != self.Profile.profile_id:
            return False
        return True

    def save_profile(self, filename, user_password):
        if self.Profile.user_pw_salt == "":
            self.Profile.user_pw_salt = binascii.hexlify(os.urandom(32)).decode()
        if self.Profile.aes_key_salt == "":
            self.Profile.aes_key_salt = binascii.hexlify(os.urandom(32)).decode()
        self.Profile.user_pw_hash = self.hash_string(user_password, self.Profile.user_pw_salt)

        # schlüssel ableiten
        if self.Profile.aes_key == "":
            self.Profile.aes_key = self.hash_string(user_password, self.Profile.aes_key_salt).encode("utf-8")

        set_new_password = (
                len(self.Profile.rsa_seed_words) == 0)  # when new password is set, the len of word seed is 0
        if not set_new_password:  # only on first start (profile generation) the key is derived from seed
            rsa_keypair = self.generate_rsa_key(
                self.Profile.rsa_seed_words)  # derive rsa key from the first seed words
            self.Profile.private_key = rsa_keypair.exportKey("PEM")
            self.Profile.database_key = self.hash_string( self.Profile.rsa_seed_words, "staticsalt").encode("utf-8")

        if set_new_password:
            self.Profile.private_key = None
            # get private key from old aes-key
            private_key = self.aes_decrypt(self.Profile.aes_encrypted_private_key, self.Profile.old_aes_key)  # .decode("utf-8")
            self.Profile.private_key = private_key


        if self.Profile.rsa_key_pair == None:  # some variables need to be initialized after first profile generation
            private_key = self.Profile.private_key
            self.Profile.rsa_key_pair = RSA.importKey(private_key)
            self.Profile.rsa_key_pair_id = self.get_publickey_id(self.rsapubkey_to_rsapukeystring(self.Profile.rsa_key_pair.public_key()))
            self.Profile.pubkey_string = self.rsapubkey_to_rsapukeystring(self.Profile.rsa_key_pair.public_key())
            self.Profile.profile_id = self.get_publickey_id(
                self.rsapubkey_to_rsapukeystring(self.Profile.rsa_key_pair.public_key()))


        self.Profile.aes_encrypted_private_key = None

        self.Profile.aes_encrypted_private_key = self.aes_encrypt(self.Profile.private_key, self.Profile.aes_key)

        self.Profile.aes_encrypted_seed_words = self.aes_encrypt(self.Profile.rsa_seed_words.encode("utf-8"),
                                                                 self.Profile.aes_key)


        self.Profile.aes_encrypted_database_key = self.aes_encrypt(self.Profile.database_key, self.Profile.aes_key)

        profile_dict = {'user_pw_hash': self.Profile.user_pw_hash, 'user_pw_salt': self.Profile.user_pw_salt,
                        'aes_encrypted_seed_words': self.Profile.aes_encrypted_seed_words,
                        'profile_id': self.Profile.profile_id,
                        'aes_key_salt': self.Profile.aes_key_salt,
                        'aes_encrypted_private_key': self.Profile.aes_encrypted_private_key,
                        'aes_encrypted_database_key': self.Profile.aes_encrypted_database_key}

        functions.save_var_to_file(profile_dict, filename)
        self.Profile.profile_exist = True

    def load_profile_dat(self, filename):
        """
        Loads profile Data from profile file
        :param filename:
        :return:
        """
        profile_dict = functions.load_var_from_file(filename)
        self.Profile.user_pw_hash = profile_dict['user_pw_hash']
        self.Profile.user_pw_salt = profile_dict['user_pw_salt']
        self.Profile.aes_key_salt = profile_dict['aes_key_salt']
        self.Profile.aes_encrypted_seed_words = profile_dict['aes_encrypted_seed_words']
        self.Profile.profile_id = profile_dict['profile_id']
        self.Profile.aes_encrypted_private_key = profile_dict['aes_encrypted_private_key']
        self.Profile.aes_encrypted_database_key = profile_dict['aes_encrypted_database_key']


    def init_profile(self, user_password):
        """
        Init the profile after the correct password is entered
        :return:
        """

        # derive aes key
        self.Profile.aes_key = self.hash_string(user_password, self.Profile.aes_key_salt).encode("utf-8")
        self.Profile.profile_is_initialized = True

        #for encrypted_private_key in self.Profile.aes_encrypted_private_key:
        private_key = self.aes_decrypt(self.Profile.aes_encrypted_private_key, self.Profile.aes_key)  # .decode("utf-8")
        self.Profile.rsa_key_pair = RSA.importKey(private_key)
        self.Profile.rsa_key_pair_id = self.get_publickey_id(self.rsapubkey_to_rsapukeystring(self.Profile.rsa_key_pair.public_key()))
        self.Profile.pubkey_string = self.rsapubkey_to_rsapukeystring(self.Profile.rsa_key_pair.public_key())
        self.Profile.profile_id = self.get_publickey_id(
            self.rsapubkey_to_rsapukeystring(self.Profile.rsa_key_pair.public_key()))
        self.Profile.database_key = self.aes_decrypt(self.Profile.aes_encrypted_database_key, self.Profile.aes_key)

        return True

    def rsapubkey_to_rsapukeystring(self, rsapubkey):
        key_der_format = rsapubkey.exportKey("DER")
        base64_bytes = base64.b64encode(key_der_format)
        base64_string = base64_bytes.decode("utf8")
        return base64_string

    def rsapubkeystring_to_rsapubkey(self, rsapupkey_string):
        """
        converts a base64 decoded rsakey string to an pupkey with rsa-format.

        :param rsapupkey_string: base64 encoded rsakey-string
        :return: public RsaKey object.
        """
        back = rsapupkey_string.encode("utf8")
        # ic(back)
        byte_decoded = base64.b64decode(back)
        rsakey = RSA.import_key(byte_decoded)
        return rsakey

    def generate_word_seed(self):
        '''generate seed of 12 words
        used for rsa key

        :return: a string of 12 words like: "robust goose pill garlic trigger minute quiz tower cook eager twelve"
        '''
        mnemo = mnemonic.Mnemonic('english')
        words = mnemo.generate(strength=128)
        return words

    def check_word_seed(self, seed) -> bool:
        """check if word seed is valid"""
        mnemo = mnemonic.Mnemonic('english')
        return mnemo.check(seed)

    def word_seed_is_ok(self, words):
        '''returns oky if original english word seed
        :param words: String of words to check if ok
        :return: true if original words
        '''
        mnemo = mnemonic.Mnemonic('english')
        return mnemo.check(words)

    def rsa_encrypt(self, message, public_key, encoded=False):
        """
        :param message: string msg to encrypt
        :param public_key: public key in PEM Format
        :param encoded:
        :return:
        """

        rsa_key = RSA.importKey(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        if not encoded:
            message = str.encode(message)
        # ic(message)

        return base64.b64encode(cipher.encrypt(message))

    def rsa_decrypt(self, encrypted_message, private_key):
        rsa_key = RSA.importKey(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        try:
            return cipher.decrypt(base64.b64decode(encrypted_message))
        except binascii.Error:
            return None

    # todo codeimproving: same func also in functions
    def sign(self, msg, keyPair):
        # Sign the message using the PKCS#1 v1.5 signature scheme (RSASP1)
        hash = SHA256.new(msg)
        signer = PKCS115_SigScheme(keyPair)
        signature = signer.sign(hash)
        return binascii.hexlify(signature)

    def sign_is_correct(self, message, signature, pubKey):
        ''' Checks if the signature is correct.

        :param message: Signed message to check
        :param signature: Signature of the message
        :param keyPair: RSA keypair with the public key to check the signature.
        :return: True if signature ist correct else False
        '''

        # print(type(pubKey))
        # if isinstance(pubKey, bytes):
        #     pubKey = serialization.load_pem_public_key(bytes(pubKey))
        #    #ic("converted key from pem format")

        # Verify valid PKCS#1 v1.5 signature (RSAVP1)
        signature = binascii.unhexlify(signature)
        # pubKey = keyPair.publickey()
        # msg = b'Message for RSA signing'
        hash = SHA256.new(message)
        verifier = PKCS115_SigScheme(pubKey)
        try:
            verifier.verify(hash, signature)
            # print("Signature is valid.")
            return True
        except:
            pass
            # print("Signature is invalid.")
        return False

    def get_publickey_id(self, publickey):
        """ calculate the ID from a publickey.
        The ID is derived from the first 16 digits of the sha256 hash of the publickey.
        :param publickey: publickey in base64-encoded format
        :return: ID from public key as string
        """
        # ic.disable()
        if isinstance(publickey, bytes):
            # ic("publickey is byte:", publickey)
            publickey = publickey.decode("utf8")

        return functions.short_SHA256(publickey, 32)

    def generate_rsa_key(self, word_seed):
        """ Generates from an seed (string) a RSA keypair.

            :param word_seed: String f
            :return: RSA Keypair
            """
        # word seed string to short. less the 20 chars or less than 12 words raise error
        if len(word_seed.replace(" ", "")) < 20 or len(word_seed.split(" ")) < 12:
            raise Exception(f"Word seed: '{word_seed}' too short!")

        # TODO Maybe an security issue how the keypair is generated from the seed. Is this really secure?
        # based on https://stackoverflow.com/questions/18264314/#answer-18266970
        seed_128 = HMAC.new(
            bytes(word_seed, 'utf-8') + b'Application: 2nd key derivation'
        ).digest()

        class PRNG(object):

            def __init__(self, seed):
                self.index = 0
                self.seed = seed
                self.buffer = b""

            def __call__(self, n):
                while len(self.buffer) < n:
                    self.buffer += HMAC.new(
                        self.seed + pack("<I", self.index)).digest()
                    self.index += 1
                result, self.buffer = self.buffer[:n], self.buffer[n:]
                return result

        return RSA.generate(2048, randfunc=PRNG(seed_128))

    def aes_encrypt(self, cleartext, password, checksum=True, compress=True):
        IV_SIZE = 16  # 128 bit, fixed for the AES algorithm
        KEY_SIZE = 32  # 256 bit meaning AES-256, can also be 128 or 192 bits
        SALT_SIZE = 16  # This size is arbitrary

        # print(os.urandom(16))
        salt = os.urandom(SALT_SIZE)
        # print('salt', salt)
        derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                                      dklen=IV_SIZE + KEY_SIZE)
        iv = derived[0:IV_SIZE]
        key = derived[IV_SIZE:]

        # falls dict or list dann konvertieren
        if isinstance(cleartext, dict) or isinstance(cleartext, list):
            # using encode() + dumps() to convert to bytes
            cleartext = json.dumps(cleartext).encode('utf-8')

        if compress:
            cleartext = zlib.compress(cleartext)

        elif checksum:
            # ic("cheksumme hinzufügen")
            cleartext += struct.pack("i", zlib.crc32(cleartext))

        encrypted = salt + AES.new(key, AES.MODE_CFB, iv).encrypt(cleartext)

        return encrypted

    def checksum_error(exception):
        print("CRC Error - Wrong encryption key?")

    def aes_decrypt(self, encrypted, password, checksum=True, compressed=True):
        IV_SIZE = 16  # 128 bit, fixed for the AES algorithm
        KEY_SIZE = 32  # 256 bit meaning AES-256, can also be 128 or 192 bits
        SALT_SIZE = 16  # This size is arbitrary

        salt = encrypted[0:SALT_SIZE]
        derived = hashlib.pbkdf2_hmac('sha256', password, salt, 100000,
                                      dklen=IV_SIZE + KEY_SIZE)
        iv = derived[0:IV_SIZE]
        key = derived[IV_SIZE:]

        # ic(password)
        clear_text = AES.new(key, AES.MODE_CFB, iv).decrypt(encrypted[SALT_SIZE:])

        if compressed:
            try:
                clear_text = zlib.decompress(clear_text)
            except:
                raise self.checksum_error("checksum mismatch")

        elif checksum:
            crc, clear_text = (clear_text[-4:], clear_text[:-4])
            if not crc == struct.pack("i", zlib.crc32(clear_text)):
                raise self.checksum_error("checksum mismatch")
                # print("Entschlüsselung fehlgeschlagen. Schlüssel falsch?")
                # return "", False

        # falls es ein dict war wieder in dict konvertieren.
        try:
            clear_text = json.loads(clear_text.decode('utf-8'))
        except:
            pass

        return clear_text

    def hybrdid_encryption(self, data, puplickeys, extra_password=False):
        """ encrypt data with aes encryption. the aes encrytion-key is encrypted with the public key.\\

        :param data: data to encrypt
        :param puplickeys: list of public keys.
        :return:
        """
        aes_key = binascii.hexlify(os.urandom(32))
        # ic(aes_key)

        encrypt_with_extra_password = (not extra_password == False)

        encrypted_data_dict = {}
        key_tubles = {}
        for pupkey in puplickeys:
            # print("pupkey")
            rsa_encrypted_aes_key = self.rsa_encrypt(aes_key, pupkey, True)
            pubkey_id = self.get_publickey_id(pupkey)
            key_tubles[pubkey_id] = rsa_encrypted_aes_key

        # if extra password then add an pseudo pupkey entry ID "password" .... and aes-enrypt the aes_key with the extra_password
        if encrypt_with_extra_password:
            aes_encrypted_aes_key = self.aes_encrypt(aes_key, extra_password.encode('utf-8'))
            key_tubles['password'] = aes_encrypted_aes_key

        # ic(key_tubles)

        encrypted_data_dict.update({"encrypted_key": key_tubles})

        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')

        encrypted = self.aes_encrypt(data, aes_key)
        encrypted_data_dict.update({"encrypted_data": encrypted})
        return encrypted_data_dict

    def hybrdid_decryption(self, enc_data, rsa_keypair, extra_password=False):
        """decrypts the AES key with the private key and uses the the aes key to decrypt the encrypted data

        :param enc_data: data with list of public_key_id and encrypted aes_key and the aes enrypted data_dict
        :param rsa_keypair: rsa_kypair with public and private key
        :return: a dict with data or False if decryption fails
        """
        private_key = rsa_keypair.exportKey("PEM")
        public_key = rsa_keypair.publickey().exportKey("PEM")
        public_key_id = self.get_publickey_id(public_key)

        aes_key = None
        try:
            if public_key_id in enc_data["encrypted_key"].keys():
                # ic("import per freundes ID")
                rsa_encrypted_key = enc_data["encrypted_key"][public_key_id]
                aes_key = self.rsa_decrypt(rsa_encrypted_key, private_key)
                # ic(aes_key)
            # if there is an extra password and the aes_encrypted_aes_key was found -> decrypt the aes key
            elif aes_key == None and not extra_password == False and "password" in enc_data["encrypted_key"].keys():
                # ic("import mit extra passwort:", extra_password)
                aes_encrypted_aes_key = enc_data["encrypted_key"]["password"]
                aes_key = self.aes_decrypt(aes_encrypted_aes_key, extra_password.encode('utf-8'))
                # ic(aes_key)

        except:
            # ic("friends file is corrupt")
            return False

        if aes_key == None:
            return False

        # decrypt aes encrypted data_dict with the aes key
        decrypted_data = self.aes_decrypt(enc_data["encrypted_data"], aes_key)
        return decrypted_data

    # liefert brutforce sicheren Hash / Key eines Strings
    def hash_string(self, plaintext, salt):
        plaintext = plaintext.encode()
        salt = salt.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(plaintext)).decode()


def Anderes():
    # byte Umwandlungen als Beispiel
    msg = b'Message for RSA signing'
    msgdecoded = msg.decode("utf-8")  # byte to string
    msgdecoded.encode("utf-8")  # string to byte

    user_dict = {'name': 'dinesh', 'code': 'dr-01'}

    user_encode_data = json.dumps(user_dict, indent=2).encode('utf-8')  # dict to byte, ohne indent=2 erhält newline /n
    print(user_encode_data)
    new = json.loads(user_encode_data.decode('utf-8'))  # byte to dict
    print(new['name'])
