import math as _math
import typing as _typing


class Description(_typing.NamedTuple):
    x: _typing.Any = 0
    y: _typing.Any = 0
    z: _typing.Any = 0
    def tare_x(self):
        cls = type(self)
        return cls(0, self.y - self.x, self.z - self.x)
    def tare_y(self):
        cls = type(self)
        return cls(self.x - self.y, 0, self.z - self.y)
    def tare_z(self):
        cls = type(self)
        return cls(self.x - self.z, self.y - self.z, 0)
    def projected_abscissa(self):
        return (self.y - self.x) * (.75 ** .5)
    def projected_ordinate(self):
        return (self.x * -.5) + (self.y * -.5) + self.z
    def projected_radius(self):
        return ((self.projected_abscissa() ** 2) + (self.projected_ordinate() ** 2)) ** .5
    def projected_angle(self):
        try:
            ratio = self.projected_abscissa() / self.projected_radius()
        except ZeroDivisionError:
            return float('nan')
        if self.projected_ordinate() < 0:
            return -_math.acos(ratio)
        else:
            return _math.acos(ratio)
    def __bool__(self):
        return all(self)
    def __float__(self):
        if bool(self):
            return float('nan')
        else:
            return 0.
    def __int__(self):
        return int(float(self))
    
class Vector:
    def tare_x(self):
        return Description(0, self._y, self._z)
    def tare_y(self):
        return self.tare_x().tare_y()
    def tare_z(self):
        return self.tare_x().tare_z()
    def projected_abscissa(self):
        return self.tare_x().projected_abscissa()
    def projected_ordinate(self):
        return self.tare_x().projected_ordinate()
    def projected_angle(self):
        return self.tare_x().projected_angle()
    def projected_radius(self):
        return self.tare_x().projected_radius()
    def rotate(self, amount):
        cls = type(self)
        items = self._rotate(amount)[:3]
        return cls(*items)
    def _rotate(self, amount):
        cls = type(self)
        if type(amount) is not int:
            raise TypeError
        v = self
        if amount % 2:
            v = -v
            amount -= 3
        items = tuple(v.tare_x()) * 2
        amount %= 6
        if amount == 0:
            return items[0:]
        if amount == 2:
            return items[1:]
        if amount == 4:
            return items[2:]
        raise NotImplementedError
    def _dot(self, other):
        return (
            (self._y * other._y)
            + (self._z * other._z)
            + (-.5 * self._y * other._z)
            + (-.5 * self._z * other._y)
        )
    def _list(self):
        return [
            self.tare_x(),
            self.tare_y(),
            self.tare_z(),
        ]
    def __init__(self, *args, **kwargs):
        v = Description(*args, **kwargs)
        self._y = v[1] - v[0]
        self._z = v[2] - v[0]
    def __iter__(self):
        for a in self._list():
            yield a
    def __getitem__(self, key):
        if type(key) is int:
            return self._list()[key]
        if type(key) is slice:
            return (a for a in self._list())
        raise TypeError
    def __add__(self, other):
        cls = type(self)
        if type(other) is not cls:
            raise TypeError
        return cls(0, self._y + other._y, self._z + other._z)
    def __neg__(self):
        cls = type(self)
        return cls(0, -self._y, -self._z)
    def __sub__(self, other):
        return self + (-other)
    def __mul__(self, other):
        cls = type(self)
        if type(other) is cls:
            return self._dot(other)
        else:
            return cls(0, self._y * other, self._z * other)
    def __rmul__(self, other):
        cls = type(self)
        if type(other) is cls:
            raise NotImplementedError
        else:
            return cls(0, other * self._y, other * self._z)
    def __div__(self, other):
        cls = type(self)
        return cls(0, self._y / other, self._z / other)
    def __pow__(self, other):
        if type(other) is not int:
            raise TypeError
        if other < 0:
            raise ValueError
        ans = 1
        for i in range(other):
            ans *= self
        return ans
    def __hash__(self):
        return (self._y, self._z).__hash__()
    def __eq__(self, other):
        cls = type(self)
        if type(other) is not cls:
            return False
        return (self._y == other._y) and (self._z == other._z)
    def __str__(self):
        cls = type(self)
        return f"{cls.__name__}(projected_abscissa={self.projected_abscissa()}, projected_ordinate={self.projected_ordinate()})"
    def __repr__(self):
        return str(self)
    def __bool__(self):
        return self._y or self._z
    def __float__(self):
        if bool(self):
            return float('nan')
        else:
            return 0.
    def __int__(self):
        return int(float(self))
        
