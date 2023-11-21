from .driver import _TTIPowerSupplyBase


class TTIPowerSupply(_TTIPowerSupplyBase):
    """
    Driver for a TTI QL355P power supply. Communicates over RS232 with an exclusive VISA lock.
    """

    _tol = 1e-5

    def __init__(self, *args, **kwargs):
        # kwargs["wait_after_connect"] = 1
        kwargs["baud_rate"] = 19200
        kwargs["read_termination"] = "\r\n"
        kwargs["write_termination"] = "\r\n"

        super().__init__(*args, **kwargs)
