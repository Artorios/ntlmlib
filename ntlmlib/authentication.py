# (c) 2015, Ian Clegg <ian.clegg@sourcewarp.com>
#
# ntlmlib is licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__author__ = 'ian.clegg@sourcewarp.com'

from Crypto.Cipher import DES
from Crypto.Hash import MD5
from Crypto.Hash import MD4
from Crypto.Util import number
from Crypto.Cipher import ARC4
import hmac
import random
import struct
import calendar
import time
from messages import TargetInfo
from constants import NegotiateFlag


class PasswordAuthentication(object):
    """
    Initializes the PasswordAuthentication with the supplied domain, username and password
    """
    known_des_input = "KGS!@#$%"

    def __init__(self, domain, username, password, **kwargs):
        """
        Initializes the PasswordAuthentication with the supplied domain, username and password. Alternatively, if the
        password is not available, a set of password hashes can be supplied in the kwargs dictionary.
        Note: Unlike Unix password hashes, the LM and NTLM hashes are password-equivalents in the context of the
        response calculations; they must be protected as much as the passwords themselves.

        :param domain: The windows domain name
        :param user: The windows username
        :param password: The users password
        :param: kwargs: A optional dictionary which contains the external hashes where the password is not available
                        and/or overrides the default the Lan Manager Compatibility Level of 3
                challenge
                ansi_hash        - A pre-computed LM Hash of the password
                unicode_hash     - A pre-computed NTLM Hash of the password
                compatibility    - Lan Manager Compatibility Level to use
                                    On Windows Clients the level is set by an 'Administrator' in
                                    HKLM\SYSTEM\CurrentControlSet\Control\Lsa\LmCompatibilityLevel
                                    0 : Use LM and NTLM authentication, but never use NTLMv2 session security.
                                    1 : Use LM and NTLM authentication, but use NTLMv2 session security if possible
                                    2 : Use only NTLM authentication, but use NTLMv2 session security if possible
                                    3 : Use only NTLMv2 authentication, but use NTLMv2 session security if possible
                                    4 : Use only NTLMv2 authentication, but use NTLMv2 session security if possible
                                    5 : Use only NTLMv2 authentication, but use NTLMv2 session security if possible
                                    Note: Levels 3 to 5 are identical in terms of client behaviour, they only differ
                                    with respect to Domain Controller behaviour which is not applicable here

        NTLMv1 and NTLM2 Signing and Sealing is only available in Windows NT 4.0 SP4 and later
        """
        self._domain = domain
        self._username = username
        self._password = password
        self._challenge = kwargs.get('challenge', None)
        self._ansi_hash = kwargs.get('lm_hash', None)
        self._unicode_hash = kwargs.get('ntlm_hash', None)
        self._lm_compatibility = kwargs.get('compatibility', 3)

        # Initialise a random default 8 byte NTLM client challenge
        self._random = random.SystemRandom()
        self._client_challenge = number.long_to_bytes(self._random.getrandbits(8 * 8))
        self._client_key = number.long_to_bytes(self._random.getrandbits(16 * 8))

        # NTLM participants can include additional data in the TargetInfo (AV_PAIRS) to prevent MiTM and replay attacks
        # we include them by default, but allow the user to override this in case of compatibility issues.
        # MsvAvTimestamp is supported in Windows Vista / Windows 2008 and later
        # MsvChannelBindings is supported in Windows 7 and Windows 2008 R2 and later
        self._av_timestamp = kwargs.get('timestamp', True)
        self._av_channel_bindings = kwargs.get('channel_bindings', True)

        # If any external hashes have been supplied in kwargs, they must all be present
        if any(key in kwargs for key in ('challenge', 'lm_hash', 'ntlm_hash')):
            if not all(key in kwargs for key in ('challenge', 'lm_hash', 'ntlm_hash')):
                raise Exception("Please specify all hashes: challenge, lm_hash and ntlm_hash")
            elif self._password is not None:
                raise Exception("When using hashes, the password must be 'None'")
        elif self._password is None:
            raise Exception("Please specify a password or all hashes: challenge, lm_hash and ntlm_hash")


    def get_domain(self):
        """
        :return: The windows domain name
        """
        return self._domain

    def get_username(self):
        """
        :return: The windows username
        """
        return self._username

    def get_password(self):
        """
        :return: The password for the user if it is available
        """
        if self._unicode_hash is not None:
            raise Exception('The password is not available when initialised using hashes')
        return self._password

    def get_compatibility_level(self):
        """
        :return: The Lan Manager Compatibility Level
        """
        return self._lm_compatibility

    def get_lm_response(self, flags, challenge):
        """
        Computes the 24 byte LMHash password hash given the 8 byte server challenge.
        :param challenge: The 8-byte challenge message generated by the server
        :return: The 24 byte LMHash
        """
        # If lm compatibility level lower than 3, but the server negotiated NTLM2, generate an
        # NTLM2 response in preference to the weaker LMv1
        if flags & NegotiateFlag.NTLMSSP_NTLM2_KEY and self._lm_compatibility < 3:
            return self._client_challenge + '\x00' * 16

        if 0 <= self._lm_compatibility <= 1:
            return PasswordAuthentication.get_pre_ntlm_response(self._password, challenge)
        elif self._lm_compatibility == 2:
            return PasswordAuthentication.get_ntlmv1_response(self._password, challenge)
        elif 3 <= self._lm_compatibility <= 5:
            return PasswordAuthentication.get_lmv2_response(self._domain, self._username, self._password, challenge,
                                                            self._client_challenge)
        else:
            raise Exception('Unknown Lan Manager Compatibility Level')

    def get_ntlm_response(self, flags, challenge, target_info=None, channel_binding=None):
        """
        Computes the 24 byte NTLM challenge response given the 8 byte server challenge, along with the session key.
        If NTLMv2 is used, the TargetInfo structure must be supplied, the updated TargetInfo structure will be returned
        :param challenge: The 8-byte challenge message generated by the server
        :return: A tuple containing the 24 byte NTLM Hash, Session Key and TargetInfo
        """
        # If lm compatibility level is 3 or lower, but the server negotiated NTLM2, generate an
        # NTLM2 response in preference to the weaker NTLMv1.
        if flags & NegotiateFlag.NTLMSSP_NTLM2_KEY and self._lm_compatibility < 3:
            response, key = PasswordAuthentication.get_ntlm2_response(self._password, challenge, self._client_challenge)

        elif 0 <= self._lm_compatibility < 3:
            response, key = PasswordAuthentication.get_ntlmv1_response(self._password, challenge)
        elif 2 < self._lm_compatibility <= 5:
            # There is an issue around timestamps here. Are we supported to provide one, or get it
            # if there is one I think we must use it!
            timestamp = PasswordAuthentication._get_ntlm_timestamp()
            timestamp = target_info[TargetInfo.NTLMSSP_AV_TIME][1]

            # See [MS-NLMP] for pseudo code to set MsvAvTimestamp,
            if self._av_timestamp is True:
                if target_info is None:
                    target_info = TargetInfo()
                if target_info[TargetInfo.NTLMSSP_AV_TIME] is None:
                    target_info[TargetInfo.NTLMSSP_AV_TIME] = timestamp
                    # TODO: Windows Vista and later will also set the MIC field if _av_timestamp is valid

            # Calculating channel bindings is poorly documented. It is implemented in winrmlib, and needs to be
            # moved here
            if self._av_channel_bindings is True and channel_binding is not None:
                target_info[TargetInfo.NTLMSSP_AV_CHANNEL_BINDINGS] = channel_binding

            response, key, target_info = PasswordAuthentication.get_ntlmv2_response(self._domain, self._username,
                                                                                    self._password.encode('utf-16le'),
                                                                                    challenge, self._client_challenge,
                                                                                    timestamp, target_info)
        else:
            raise Exception('Unknown Lan Manager Compatibility Level')

        # If the we negotiated key exchange, generate a new new master key for the session, this is RC4-encrypted
        # with the previously selected session key. Even with key weakening the full 128bit master session key is
        # always sent to the server. This process is the same in across all NTLM versions.
        if flags & NegotiateFlag.NTLMSSP_KEY_EXCHANGE:
            cipher = ARC4.new(key)
            key = cipher.encrypt(self._client_key)

        return response, key, target_info

    def get_session_key(self):
        """
        Returns the user session key if a key has been negotiated this function cannot be used when
        using external hashes since the original password is required.
        :param challenge: The 8-byte challenge message generated by the server
        :return: The effective user session key, used for NTLM signing and sealing.
        """
        return self._client_key
        """
        random_key = number.long_to_bytes(self._random.getrandbits(16 * 8))
        cipher = ARC4.new(key)
        return cipher.encrypt(random_key)


        if flags & NegotiateFlag.NTLMSSP_NTLM2_KEY:
            # NTLM v2 Session Security
            pass
        else:
            # NTLM v1 Session Security
            pass
        """
        """
        if self._password is None:
            return
        md4 = MD4.new()
        md4.update(self._password)

        key_exchange = True
        if 0 <= self._lm_compatibility <= 2:
            md4.update(md4.digest())
            return md4.digest()
        elif 3 <= self._lm_compatibility <= 5:

                ntlmv2_hash = PasswordAuthentication.ntowfv2(self._domain, self._username, self._password)
                hmac_context = hmac.new(ntlmv2_hash)
                hmac_context.update(challenge)
                hmac_context.update(self._client_challenge)

                user_key = hmac.new(ntlmv2_hash)
                user_key.update(hmac_context.digest())
                return user_key.digest()
        else:
            raise Exception('Unknown Lan Manager Compatibility Level')
        """

    @staticmethod
    def _expand_des_key(key):
        """
        Expand the key from a 7-byte password key into a 8-byte DES key
        """
        key  = key[:7]
        key += '\x00' * (7 - len(key))
        s = chr(((ord(key[0]) >> 1) & 0x7f) << 1)
        s += chr(((ord(key[0]) & 0x01) << 6 | ((ord(key[1]) >> 2) & 0x3f)) << 1)
        s += chr(((ord(key[1]) & 0x03) << 5 | ((ord(key[2]) >> 3) & 0x1f)) << 1)
        s += chr(((ord(key[2]) & 0x07) << 4 | ((ord(key[3]) >> 4) & 0x0f)) << 1)
        s += chr(((ord(key[3]) & 0x0f) << 3 | ((ord(key[4]) >> 5) & 0x07)) << 1)
        s += chr(((ord(key[4]) & 0x1f) << 2 | ((ord(key[5]) >> 6) & 0x03)) << 1)
        s += chr(((ord(key[5]) & 0x3f) << 1 | ((ord(key[6]) >> 7) & 0x01)) << 1)
        s += chr((ord(key[6]) & 0x7f) << 1)
        return s

    @staticmethod
    def _encrypt_des_block(key, msg):
        cipher = DES.new(PasswordAuthentication._expand_des_key(key), DES.MODE_ECB)
        return cipher.encrypt(msg)

    @staticmethod
    def _get_ntlm_timestamp():
        # The NTLM timestamp is a 64-bit unsigned integer that contains the current system time, represented as the
        # number of 100 nanosecond ticks elapsed since midnight of January 1, 1601 (UTC).
        # We must calculate this value from the Unix Epoch (seconds since Thursday, 1 January 1970 UTC) by adding
        # 116444736000000000 to rebase to January 1, 1601 then multiply by 10000000 to convert to 100 nanoseconds.
        return struct.pack('<q', (116444736000000000 + calendar.timegm(time.gmtime()) * 10000000))

    @staticmethod
    def get_pre_ntlm_response(password, challenge):
        lm_hash = PasswordAuthentication.lmowfv1(password)
        response  = PasswordAuthentication._encrypt_des_block(lm_hash[:7], challenge)
        response += PasswordAuthentication._encrypt_des_block(lm_hash[7:14], challenge)
        response += PasswordAuthentication._encrypt_des_block(lm_hash[14:], challenge)
        return response

    @staticmethod
    def get_ntlmv1_response(password, challenge):
        """
        Generate the Unicode MD4 hash for the password associated with these credentials.
        """
        ntlm_hash = PasswordAuthentication.ntowfv1(password.encode('utf-16le'))
        response  = PasswordAuthentication._encrypt_des_block(ntlm_hash[:7], challenge)
        response += PasswordAuthentication._encrypt_des_block(ntlm_hash[7:14], challenge)
        response += PasswordAuthentication._encrypt_des_block(ntlm_hash[14:], challenge)

        # The NTLMv1 session key is simply the MD4 hash of the ntlm hash
        session_hash = MD4.new()
        session_hash.update(ntlm_hash)
        return response, session_hash.digest()

    @staticmethod
    def get_ntlm2_response(password, server_challenge, client_challenge):
        """
        Generate the Unicode MD4 hash for the password associated with these credentials.
        """
        md5 = MD5.new()
        md5.update(server_challenge + client_challenge)
        ntlm2_session_hash = md5.digest()[:8]
        ntlm_hash = PasswordAuthentication.ntowfv1(password.encode('utf-16le'))
        response  = PasswordAuthentication._encrypt_des_block(ntlm_hash[:7], ntlm2_session_hash)
        response += PasswordAuthentication._encrypt_des_block(ntlm_hash[7:14], ntlm2_session_hash)
        response += PasswordAuthentication._encrypt_des_block(ntlm_hash[14:], ntlm2_session_hash)

        # TODO
        key = ""
        return response, key

    @staticmethod
    def lmowfv1(password):
        if password is None:
            raise Exception("Password parameter is required")

        password = password.upper()
        lmhash  = PasswordAuthentication._encrypt_des_block(password[:7], PasswordAuthentication.known_des_input)
        lmhash += PasswordAuthentication._encrypt_des_block(password[7:14], PasswordAuthentication.known_des_input)
        return lmhash

    @staticmethod
    def ntowfv1(password):
        if password is None:
            raise Exception("Password parameter is required")

        md4 = MD4.new()
        md4.update(password)
        return md4.digest()

    @staticmethod
    def ntowfv2(domain, user, password):
        """
        NTOWFv2() Implementation
        [MS-NLMP] v20140502 NT LAN Manager (NTLM) Authentication Protocol
        3.3.2 NTLM v2 Authentication
        :param domain: The windows domain name
        :param user: The windows username
        :param password: The users password
        :return: Hash Data
        """
        if password is None:
            raise Exception("Password parameter is required")
        md4 = MD4.new()
        md4.update(password)
        hmac_context = hmac.new(md4.digest())
        hmac_context.update(user.upper().encode('utf-16le'))
        hmac_context.update(domain.encode('utf-16le'))
        return hmac_context.digest()

    @staticmethod
    def _compute_response(response_key, server_challenge, client_challenge):
        """
        ComputeResponse() has been refactored slightly to reduce its complexity and improve
        readability, the 'if' clause which switches between LMv2 and NTLMv2 computation has been
        removed. Users should not call this method directly, they should rely on get_lmv2_response
        and get_ntlmv2_response depending on the negotiated flags.

        [MS-NLMP] v20140502 NT LAN Manager (NTLM) Authentication Protocol
        3.3.2 NTLM v2 Authentication
        """
        hmac_context = hmac.new(response_key)
        hmac_context.update(server_challenge)
        hmac_context.update(client_challenge)
        return hmac_context.digest()

    @staticmethod
    def get_lmv2_response(domain, username, password, server_challenge, client_challenge):
        """
        Computes an appropriate LMv2 response based on the supplied arguments
        The algorithm is based on jCIFS. The response is 24 bytes, with the 16 bytes of hash
        concatenated with the 8 byte client client_challenge
        """
        ntlmv2_hash = PasswordAuthentication.ntowfv2(domain, username, password.encode('utf-16le'))
        hmac_context = hmac.new(ntlmv2_hash)
        hmac_context.update(server_challenge)
        hmac_context.update(client_challenge)
        return hmac_context.digest() + client_challenge

    @staticmethod
    def _get_lmv2_response(domain, user, password, server_challenge, client_challenge):
        """
        [MS-NLMP] v20140502 NT LAN Manager (NTLM) Authentication Protocol
        3.3.2 NTLM v2 Authentication

        Computes an appropriate LMv2 response
        """
        response_key = PasswordAuthentication.ntowfv2(domain, user, password)
        proof = PasswordAuthentication._compute_response(response_key, server_challenge, client_challenge)
        return str(proof) + client_challenge

    @staticmethod
    def get_ntlmv2_response(domain, user, password, server_challenge, client_challenge, timestamp, target_info):
        """
        [MS-NLMP] v20140502 NT LAN Manager (NTLM) Authentication Protocol
        3.3.2 NTLM v2 Authentication

        Computes an appropriate NTLMv2 response. The algorithm is based on jCIFS and the ComputeResponse()
        implementation the protocol documentation.
        Note: The MS ComputeResponse() implementation refers to a variable called ServerName, this is for
        historical reasons and is misleading. ServerName refers to the bytes that compose the AV_PAIRS
        structure called target_info. The reserved constants below are defined in the documentation

        :param response_key: The return value from NTOWF()
        :param server_challenge: The 8-byte challenge message generated by the server
        :param client_challenge: The 8-byte challenge message generated by the client
        :param timestamp: The 8-byte little-endian time in GMT
        :param target_info: The AttributeValuePairs structure to be returned to the server
        :return: NTLMv2 Response
        """
        lo_response_version = '\x01'
        hi_response_version = '\x01'
        reserved_dword = '\x00' * 4
        reserved_bytes = '\x00' * 6

        response_key = PasswordAuthentication.ntowfv2(domain, user, password)
        proof_material = lo_response_version
        proof_material += hi_response_version
        proof_material += reserved_bytes
        proof_material += timestamp
        proof_material += str(client_challenge)
        proof_material += reserved_dword
        proof_material += str(target_info)
        proof_material += reserved_dword
        proof = PasswordAuthentication._compute_response(response_key, server_challenge, proof_material)

        # The master session key derivation
        session_key = hmac.new(response_key)
        session_key.update(proof)
        session_master_key = session_key.digest()
        return str(proof) + proof_material, session_master_key, target_info



"""
        TODO: Implement Key Exchange for NTLMv1
    def KXKEY(flags, sessionBaseKey, lmChallengeResponse, serverChallenge, password, lmhash, nthash, use_ntlmv2 = USE_NTLMv2):
        if use_ntlmv2:
           return sessionBaseKey

        if flags & NTLMSSP_NTLM2_KEY:
           if flags & NTLMSSP_NTLM_KEY:
              keyExchangeKey = hmac_md5(sessionBaseKey, serverChallenge + lmChallengeResponse[:8])
           else:
              keyExchangeKey = sessionBaseKey
        elif flags & NTLMSSP_NTLM_KEY:
           if flags & NTLMSSP_LM_KEY:
              keyExchangeKey = __DES_block(LMOWFv1(password,lmhash)[:7], lmChallengeResponse[:8]) + __DES_block(LMOWFv1(password,lmhash)[7] + '\xBD\xBD\xBD\xBD\xBD\xBD', lmChallengeResponse[:8])
           elif flags & NTLMSSP_NOT_NT_KEY:
              keyExchangeKey = LMOWFv1(password,lmhash)[:8] + '\x00'*8
           else:
              keyExchangeKey = sessionBaseKey
        else:
           raise "Can't create a valid KXKEY!"

   return keyExchangeKey
"""