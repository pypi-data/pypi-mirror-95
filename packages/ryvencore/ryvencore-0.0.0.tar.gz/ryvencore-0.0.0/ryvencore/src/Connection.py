from PySide2.QtCore import QObject, Signal

from .InfoMsgs import InfoMsgs


class Connection(QObject):
    """
    The base class for both types of abstract connections. All data is transmitted through a connection from an output
    port to some connected input port. The classes ExecConnection and DataConnection will be ready for reimplementation
    later, so users can add additional functionality to connections (like "weights").
    """

    def __init__(self, params):
        super().__init__()

        self.out, self.inp, self.flow = params

    def activate(self):
        pass



class ExecConnection(Connection):

    def activate(self):
        """Causes an update in the input port"""

        InfoMsgs.write('activating exec connection')
        self.inp.update()


class DataConnection(Connection):

    def get_val(self):
        """Gets the value of the output port"""

        InfoMsgs.write('getting value from data connection')
        return self.out.get_val()

    def activate(self, data=None):
        """Passes data to the input port and causes update"""

        InfoMsgs.write('activating data connection')
        self.inp.update(data)
