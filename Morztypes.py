import math


def can_be_used_as_vector(value) -> bool:
    """
    Returns whether value can be used as a value when instancing Vector2&3
    """

    return isinstance(value, (int, float, Vector2, Vector3, list, tuple, set))


class Vector2:
    """
    Two floats in one variable\n
    Has x and y
    """

    def __init__(self, x=None, y=None):
        self.x = 0
        self.y = 0

        if x is None:
            if y is None:
                self.x = 0
                self.y = 0
            else:
                self.x = y
                self.y = y
        else:
            if y is None:
                self.x = x
                self.y = x
            else:
                self.x = x
                self.y = y

        if isinstance(x, (list, tuple, set)):
            self.x = x[0]
            self.y = x[1]

        if isinstance(x, (Vector2, Vector3)):
            self.x = x.x
            self.y = x.y

    def unwrap(self, to_tuple=False):
        """
        :param to_tuple: Does the result need to be tuple
        :return: List (or tuple) of x and y of this Vector2
        """
        return [self.x, self.y] if not to_tuple else (self.x, self.y)

    @property
    def normalized(self):
        """
        :return: This Vector2 divided by its length
        """
        return self / len(self)

    @property
    def length(self):
        """
        :return: Lenght of this Vector2
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def lerped_to(self, v2, t):
        """
        Shorthand for Vector2(second_vector2) * t + this_vector2 * (1 - t)
        :param v2: Second Vector2 to lerp to
        :param t: Progress of lerping. 0 returns this Vector2, and 1 returns second Vector2
        :return:
        """
        return Vector2(v2) * t + self * (1 - t)

    @property
    def area(self):
        """
        :return: Area of this vector2, x multiplied by y
        """
        return self.x * self.y

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __sub__(self, other):
        return Vector2(self.x - Vector2(other).x, self.y - Vector2(other).y)

    def __mul__(self, other):
        return Vector2(self.x * Vector2(other).x, self.y * Vector2(other).y)

    def __add__(self, other):
        return Vector2(self.x + Vector2(other).x, self.y + Vector2(other).y)

    def __truediv__(self, other):
        return Vector2(self.x / Vector2(other).x, self.y / Vector2(other).y)

    def __floordiv__(self, other):
        return Vector2(self.x // Vector2(other).x, self.y // Vector2(other).y)

    def __mod__(self, other):
        return Vector2(self.x % Vector2(other).x, self.y % Vector2(other).y)

    def __pow__(self, power, modulo=None):
        return Vector2(self.x ** Vector2(power).x, self.y ** Vector2(power).y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Vector3:
    """
    Three floats in one variable\n
    Has x, y and z
    """

    def __init__(self, x=None, y=None, z=None):
        self.x = 0
        self.y = 0
        self.z = 0

        if x is None:
            if y is None:
                if z is None:
                    self.x = 0
                    self.y = 0
                    self.z = 0
                else:
                    self.x = z
                    self.y = z
                    self.z = z
            else:
                if z is None:
                    self.x = y
                    self.y = y
                    self.z = y
                else:
                    self.x = 0
                    self.y = y
                    self.z = z
        else:
            if y is None:
                if z is None:
                    self.x = x
                    self.y = x
                    self.z = x
                else:
                    self.x = x
                    self.y = 0
                    self.z = z
            else:
                if z is None:
                    self.x = x
                    self.y = y
                    self.z = 0
                else:
                    self.x = x
                    self.y = y
                    self.z = z

        if isinstance(x, (list, tuple, set)):
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]

        if isinstance(x, Vector2):
            self.x = x.x
            self.y = x.y

        if isinstance(x, Vector3):
            self.x = x.x
            self.y = x.y
            self.z = x.z

    def unwrap(self, to_tuple=False):
        """
        :param to_tuple: Does the result need to be tuple
        :return: List (or tuple) of x, y and z of this Vector3
        """
        return [self.x, self.y, self.z] if not to_tuple else (self.x, self.y, self.z)

    @property
    def normalized(self):
        """
        :return: This Vector3 divided by its length
        """
        return self / len(self)

    @property
    def length(self):
        """
        :return: Length of this Vector3
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def lerped_to(self, v3, t):
        """
        Shorthand for Vector3(second_vector3) * t + this_vector3 * (1 - t)
        :param v2: Second Vector3 to lerp to
        :param t: Progress of lerping. 0 returns this Vector3, and 1 returns second Vector3
        :return:
        """
        return Vector3(v3) * t + self * (1 - t)

    @property
    def volume(self):
        """
        :return: Volume of this Vector3, x * y * z
        """
        return self.x * self.y * self.z

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vector3(self.x + Vector3(other).x, self.y + Vector3(other).y, self.z + Vector3(other).z)

    def __sub__(self, other):
        return Vector3(self.x - Vector3(other).x, self.y - Vector3(other).y, self.z - Vector3(other).z)

    def __mul__(self, other):
        return Vector3(self.x * Vector3(other).x, self.y * Vector3(other).y, self.z * Vector3(other).z)

    def __truediv__(self, other):
        return Vector3(self.x / Vector3(other).x, self.y / Vector3(other).y, self.z / Vector3(other).z)

    def __floordiv__(self, other):
        return Vector3(self.x // Vector3(other).x, self.y // Vector3(other).y, self.z // Vector3(other).z)

    def __mod__(self, other):
        return Vector3(self.x % Vector3(other).x, self.y % Vector3(other).y, self.z % Vector3(other).z)

    def __pow__(self, power, modulo=None):
        return Vector3(self.x ** Vector3(power).x, self.y ** Vector3(power).y, self.z ** Vector3(power).z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


class Particle:
    t_circle = 0
    t_square = 1

    def __init__(self, type_, pos, speed, accel, size, size_decrease, color):
        self.pos = pos
        self.size = size
        self.type = type_
        self.speed = Vector2(speed)
        self.accel = Vector2(accel)
        self.size_decrease = size_decrease
        self.color = color

    def tick(self):
        self.size -= self.size_decrease
        self.speed += self.accel
        self.pos += self.speed

    def pack_for_draw(self, dis, out_library="pygame"):
        if out_library.lower() == "pygame":
            if self.type == self.t_circle:
                return [dis, self.color.unwrap(), self.pos.unwrap(), self.size / 2]
            elif self.type == self.t_square:
                return [dis, self.color.unwrap(), (self.pos - self.size / 2).unwrap() + (self.size * 2).unwrap()]
        else:
            quit(f"Library {out_library.lower()} is not supported by Morztypes! Right now the only supproted library is pygame.")