# -*- coding: utf-8 -*-
#   Copyright 2009-2021 Fumail Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
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
#
#
#
import logging

try:
    import chardet
    
    CHARDET_AVAILABLE = True
except ImportError:
    CHARDET_AVAILABLE = False


class ForceUStringError(TypeError):
    pass


def try_encoding(u_inputstring, encoding="utf-8"):
    """Try to encode a unicode string

    Args:
        u_inputstring (unicode/str):
        encoding (str): target encoding type

    Returns:
        byte-string
    """
    if u_inputstring is None:
        return None
    
    # make sure encoding is not None or empty
    if not encoding:
        encoding = "utf-8"
    
    logger = logging.getLogger("%s.stringencode.try_encoding" % __package__)
    try:
        return u_inputstring.encode(encoding, "strict")
    except UnicodeEncodeError as e:
        logger.error("Encoding error!")
        logger.exception(e)
        raise e


def try_decoding(b_inputstring, encodingGuess="utf-8", errors="strict"):
    """ Try to decode an encoded string

    This will raise exceptions if object can not be decoded. The calling
    routine has to handle the exception. For example, "force_uString" has
    to handle exceptions for sending non-encoded strings.

    Args:
        b_inputstring (str/bytes): input byte string
        encodingGuess (str): guess for encoding used, default assume unicode
        errors (str): error handling as in standard bytes.decode -> strict, ignore, replace

    Returns:
        unicode string

    """
    if b_inputstring is None:
        return None
    
    # make sure encoding is not None or empty
    if not encodingGuess:
        encodingGuess = "utf-8"
    
    logger = logging.getLogger("%s.stringencode.try_decoding" % __package__)
    u_outputstring = None
    try:
        u_outputstring = b_inputstring.decode(encodingGuess, errors=errors)
    except (UnicodeDecodeError, LookupError) as e:
        # if we get here we will also print either the chardet or trial&error decoding message anyway
        logger.debug("found non %s encoding or encoding not found (msg: %s), try to detect encoding"
                     % (str(e), encodingGuess))
        pass
    
    if u_outputstring is None:
        if CHARDET_AVAILABLE:
            encoding = chardet.detect(b_inputstring)['encoding']
            logger.info("chardet -> encoding estimated as %s" % encoding)
            try:
                u_outputstring = b_inputstring.decode(encoding, errors=errors)
            except (UnicodeDecodeError, LookupError):
                logger.info("encoding found by chardet (%s) does not work" % encoding)
        else:
            logger.debug("module chardet not available -> skip autodetect")
    
    if u_outputstring is None:
        trialerrorencoding = EncodingTrialError.test_all(b_inputstring, returnimmediately=True)
        logger.info("trial&error -> encoding estimated as one of (selecting first) %s" % trialerrorencoding)
        if trialerrorencoding:
            try:
                u_outputstring = b_inputstring.decode(trialerrorencoding[0], errors=errors)
            except (UnicodeDecodeError, LookupError):
                logger.info("encoding found by trial & error (%s) does not work" % trialerrorencoding)
    
    if u_outputstring is None:
        raise UnicodeDecodeError
    
    return u_outputstring


def force_uString(inputstring, encodingGuess="utf-8", errors="strict", convert_none=False):
    """Try to enforce a unicode string

    Args:
        inputstring (str, unicode, list): input string or list of strings to be checked
        encodingGuess (str): guess for encoding used, default assume unicode
        errors (str): error handling as in standard bytes.decode -> strict, ignore, replace
        convert_none (bool): convert None to empty string if True

    Raises:
        ForceUStringError: if input is not string/unicode/bytes (or list containing such elements)

    Returns: unicode string (or list with unicode strings)

    """
    if inputstring is None:
        return "" if convert_none else None
    elif isinstance(inputstring, list):
        return [force_uString(item, encodingGuess=encodingGuess, errors=errors) for item in inputstring]
    
    try:
        if isinstance(inputstring, str):
            return inputstring
        else:
            return try_decoding(inputstring, encodingGuess=encodingGuess, errors=errors)
    except (AttributeError, TypeError) as e:
        # Input might not be bytes but a number which is then
        # expected to be converted to unicode
        
        logger = logging.getLogger("fuglu.force_uString")
        if isinstance(inputstring, int):
            pass
        elif not isinstance(inputstring, (str, bytes)):
            logger.debug("object is not string/unicode/bytes/int but %s" % str(type(inputstring)))
        else:
            logger.debug("decoding failed using guess %s for object of type %s with message %s"
                         % (encodingGuess, str(type(inputstring)), str(e)))
        
        try:
            return str(inputstring)
        except (NameError, ValueError, TypeError, UnicodeEncodeError, UnicodeDecodeError) as e:
            logger.debug("Could not convert using 'str' -> error %s" % str(e))
            pass
        except Exception as e:
            logger.debug("Could not convert using 'str' -> error %s" % str(e))
            pass
        
        try:
            representation = str(repr(inputstring))
        except Exception as e:
            representation = "(%s)" % str(e)
        
        errormsg = "Could not transform input object of type %s with repr: %s" % \
                   (str(type(inputstring)), representation)
        
        logger.error(errormsg)
        raise ForceUStringError(errormsg)


def force_bString(inputstring, encoding="utf-8", checkEncoding=False):
    """Try to enforce a string of bytes

    Args:
        inputstring (unicode, str, list): string or list of strings
        encoding (str): encoding type in case of encoding needed
        checkEncoding (bool): if input string is encoded, check type

    Returns: encoded byte string (or list with endcoded strings)

    """
    if inputstring is None:
        return None
    elif isinstance(inputstring, list):
        return [force_bString(item) for item in inputstring]
    
    try:
        if isinstance(inputstring, bytes):
            # string is already a byte string
            # since basic string type is unicode
            b_outString = inputstring
        else:
            # encode
            b_outString = try_encoding(inputstring, encoding)
    except (AttributeError, ValueError):
        # we end up here if the input is not a unicode/string
        # just try to first create a string and then encode it
        inputstring = force_uString(inputstring)
        b_outString = try_encoding(inputstring, encoding)
    
    if checkEncoding:
        # re-encode to make sure it matches input encoding
        return try_encoding(try_decoding(b_outString, encodingGuess=encoding), encoding=encoding)
    else:
        return b_outString


def force_bfromc(chars_iteratable):
    """Python 2 like bytes from char for Python 3

    Implemented to have the same char-byte conversion in Python 3 as in Python 2
    for special applications. In general it is recommended to use the real
    str.encode() function for Python3

    Args:
        chars_iteratable (str or bytes): char-string to be byte-encoded

    Returns:
        bytes: a byte-string

    """
    if isinstance(chars_iteratable, bytes):
        return chars_iteratable
    elif isinstance(chars_iteratable, str):
        return bytes([ord(x) for x in chars_iteratable])
    else:
        raise AttributeError


def force_cfromb(bytes_iteratable):
    """Python 2 like chars from bytes for Python 3

    Implemented to have the same byte-char conversion in Python 3 as in Python 2
    for special applications. In general it is recommended to use the real
    bytes.decode() function for Python3

    Args:
        bytes_iteratable (): byte-string

    Returns:
        str: chr - string

    """
    if isinstance(bytes_iteratable, str):
        return bytes_iteratable
    elif isinstance(bytes_iteratable, int):
        return chr(bytes_iteratable)
    elif isinstance(bytes_iteratable, bytes):
        return "".join([chr(x) for x in bytes_iteratable])
    elif isinstance(bytes_iteratable, list):
        return [force_cfromb(b) for b in bytes_iteratable]
    else:
        raise AttributeError("Type: %s is not str and not bytes" % (type(bytes_iteratable)))


class EncodingTrialError(object):
    # list of Py-3.7 encodings
    all_encodings_list = ['utf-8', 'ascii', 'big5', 'big5hkscs', 'cp037',
                          'cp273', 'cp424', 'cp437', 'cp500',
                          'cp720', 'cp737', 'cp775', 'cp850',
                          'cp852', 'cp855', 'cp856', 'cp857',
                          'cp858', 'cp860', 'cp861', 'cp862',
                          'cp863', 'cp864', 'cp865', 'cp866',
                          'cp869', 'cp874', 'cp875', 'cp932',
                          'cp949', 'cp950', 'cp1006', 'cp1026',
                          'cp1125', 'cp1140', 'cp1250', 'cp1251',
                          'cp1252', 'cp1253', 'cp1254', 'cp1255',
                          'cp1256', 'cp1257', 'cp1258', 'cp65001',
                          'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
                          'euc_kr', 'gb2312', 'gbk', 'gb18030',
                          'hz', 'iso2022_jp', 'iso2022_jp_1', 'iso2022_jp_2',
                          'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr',
                          'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4',
                          'iso8859_5', 'iso8859_6', 'iso8859_7', 'iso8859_8',
                          'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13',
                          'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab',
                          'koi8_r', 'koi8_t', 'koi8_u', 'kz1048',
                          'mac_cyrillic', 'mac_greek', 'mac_iceland', 'mac_latin2',
                          'mac_roman', 'mac_turkish', 'ptcp154', 'shift_jis',
                          'shift_jis_2004', 'shift_jisx0213', 'utf_32', 'utf_32_be',
                          'utf_32_le', 'utf_16', 'utf_16_be', 'utf_16_le',
                          'utf_7', 'utf_8_sig']
    
    @staticmethod
    def test_all(bytestring, returnimmediately=False):
        """
        Test all known codecs if they can be used to decode an encoded string.
        A codec can be used if it it possible to decode the string without exception.
        Then after reencoding the string it should be the same as the original string.

        Args:
            bytestring (str, bytes): the encoded string
            returnimmediately (bool): if true function returns after the first working encoding found

        Returns:
            list(str) : list containing all encodings which passed the test

        """
        assert isinstance(bytestring, bytes)
        
        positive = []
        for enc in EncodingTrialError.all_encodings_list:
            try:
                # encode and decode
                test_decoded = bytestring.decode(enc, "strict")
                test_reencoded = test_decoded.encode(enc, "strict")
                
                if not (isinstance(test_decoded, str) and isinstance(test_reencoded, bytes)):
                    raise TypeError()
                
                if bytestring == test_reencoded:
                    positive.append(enc)
            except Exception:
                pass
        
        return positive
