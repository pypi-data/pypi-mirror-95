import socket
import random
import logging

from email.header import Header

from fuglu.shared import Suspect
from fuglu.stringencode import force_uString


class HealthCheckSuspect(Suspect):
    def __init__(self, *args, **kwargs):
        # try to initialise original suspect but don't fail on any error
        try:
            super().__init__(*args, **kwargs)
        except Exception as e:
            pass


def _connect(host, port, timeout):
    """Socket connect for healch checks"""

    logger = logging.getLogger("fuglu.check._connect")

    ipvers = socket.AF_INET
    if ':' in host:
        ipvers = socket.AF_INET6
    s = socket.socket(ipvers, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect((host, port),)
    sockfile = s.makefile('rwb')
    banner = str(sockfile.readline())
    logger.debug(f"Banner: {banner}")
    return s, sockfile


def check_fuglu_netcat(host: str = '127.0.0.1', port: int = 10125, timeout: int = 5) -> int:
    """Connect to fuglu and run healthcheck on SMTP connector"""

    logger = logging.getLogger("fuglu.check.check_fuglu_netcat")

    try:
        logger.debug("Open connection")
        s, sockfile = _connect(host, port, timeout)

        # --                        -- #
        # - prepend header for FUGLU - #
        # --                        -- #

        # start marker
        prepend_identifier = str(random.randint(1, 999))
        add_headers = [("X-DATA-PREPEND-START", prepend_identifier)]
        add_headers.append(("X-HEALTHCHECK", "true"))
        add_headers.append(("X-DATA-PREPEND-END", prepend_identifier))

        headerlines = b""
        for key, value in add_headers:
            # convert inputs if needed
            u_key = str(key)
            u_value = str(value)

            try:
                hdr = Header(u_value, header_name=u_key, continuation_ws=' ')
            except (UnicodeDecodeError, UnicodeEncodeError):
                b_value = u_value.encode()
                hdr = Header(b_value, charset='utf-8', header_name=u_key, continuation_ws=' ')

            hdrline = "%s: %s\r\n" % (u_key, hdr.encode())

            if headerlines:
                headerlines += hdrline.encode()
            else:
                headerlines = hdrline.encode()

        logger.debug("Send headerlines...")
        sockfile.write(headerlines)
        sockfile.flush()
        logger.debug("Sent, now disable writing to socket")
        try:
            s.shutdown(socket.SHUT_WR)
        except (OSError, socket.error):
            pass
        logger.debug("Wait for response and parse...")
        reply = force_uString(sockfile.read()).strip()
        logger.info(f"Got reply: {reply}")
        if reply == "DUNNO: healthcheck":
            return 0
    except Exception as e:
        logger.error(str(e))

    return 1


def check_fuglu_smtp(host: str = '127.0.0.1', port: int = 10125, timeout: int = 5) -> int:
    """Connect to fuglu and run healthcheck on SMTP connector"""

    logger = logging.getLogger("fuglu.check.check_fuglu_smtp")

    try:
        logger.debug("Open connection")
        s, sockfile = _connect(host, port, timeout)

        logger.debug("Send healthcheck...")
        sockfile.write(b"HCHK\r\n")
        sockfile.flush()

        logger.debug("Sent, now disable writing to socket")
        try:
            s.shutdown(socket.SHUT_WR)
        except (OSError, socket.error):
            pass

        logger.debug("Wait for response and parse...")
        reply = force_uString(sockfile.read()).strip()
        logger.debug(f"Got reply: {reply}")
        if reply == "250 healthcheck":
            return 0
    except Exception as e:
        logger.error(str(e))

    return 1
