"""
Define a basic simulation device which simulates the VISA response of a real device
"""

TOLERANCE = "5"  # 5 decimal places


class SimTTIPowerSupply:
    _current = None
    _voltage = None
    range = None

    def __init__(self):
        self._reset()

    def _reset(self):
        self._current = 0
        self._voltage = 0
        self.range = 0

    def close(self):
        pass

    def write(self, cmd):
        args = cmd.split(" ")
        if args[0] == "i1":
            self._set_current(float(args[1]))
        elif args[0] == "v1":
            self._set_voltage(float(args[1]))
        elif args[0] == "range1":
            self._set_range(args[1])
        elif args[0] == "reset":
            self._reset()

    def query(self, cmd):
        if cmd == "i1?":
            return ("i1 {:." + TOLERANCE + "f}").format(self._current)
        elif cmd == "v1?":
            return ("v1 {:." + TOLERANCE + "f}").format(self._voltage)
        elif cmd == "range1?":
            return "{}".format(self._get_range())

    def flush(self):
        pass

    def _set_range(self, range):
        range_num = int(range)
        if range_num not in [0, 1, 2]:
            return
        self.range = range_num

    def _get_range(self):
        return str(self.range)

    def _set_current(self, current):
        if (
            (self.range == 2 and current > 0.5)
            or (self.range == 1 and current > 3)
            or (self.range == 0 and current > 5)
        ):
            return

        self._current = current

    def _set_voltage(self, voltage):
        if (
            (self.range == 2 and voltage > 35)
            or (self.range == 1 and voltage > 35)
            or (self.range == 0 and voltage > 15)
        ):
            return

        self._voltage = voltage
