import logging
import socket

from generic_scpi_driver.session import Session

from .driver import _TTIPowerSupplyBase

logger = logging.getLogger()


class TCPSession(Session):
    def __init__(
        self, host, port=9221, timeout=1, buff_size=1024, baud_rate=None
    ) -> None:
        self._buff_size = buff_size
        self._sock = socket.create_connection((host, port), timeout=timeout)
        super().__init__()

    def write(self, s: str) -> None:
        logger.debug("Writing to TCP: %s", s)
        self._sock.send(s.encode())

    def query(self, s: str) -> str:
        self.write(s)
        r = self._sock.recv(self._buff_size).decode().strip()
        logger.debug("Received from TCP: %s", r)
        return r

    def close(self) -> None:
        self._sock.close()


class TTIPowerSupplyTCP(_TTIPowerSupplyBase):
    session_factory = TCPSession
