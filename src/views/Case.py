from ..views.Type import TYPE

class Case:
    def __init__(self, x=0, y=0, type=TYPE.plaine, proprio=None, lhabitant=None) -> None:
        self._x = x
        self._y = y
        self._type = type
        self._proprio = proprio
        self._lhabitant = lhabitant

    # Getter pour x
    @property
    def x(self):
        return self._x

    # Setter pour x
    @x.setter
    def x(self, value):
        self._x = value

    # Getter pour y
    @property
    def y(self):
        return self._y

    # Setter pour y
    @y.setter
    def y(self, value):
        self._y = value

    # Getter pour type
    @property
    def type(self):
        return self._type

    # Setter pour type
    @type.setter
    def type(self, value):
        self._type = value

    # Getter pour proprio
    @property
    def proprio(self):
        return self._proprio

    # Setter pour proprio
    @proprio.setter
    def proprio(self, value):
        self._proprio = value

    # Getter pour lhabitant
    @property
    def lhabitant(self):
        return self._lhabitant

    # Setter pour lhabitant
    @lhabitant.setter
    def lhabitant(self, value):
        self._lhabitant = value
