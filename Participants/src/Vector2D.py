class Vector2D:
    def __init__(self, x, y) -> None:
        """
        Initializes the 2D vector
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    def __add__(self, other) -> 'Vector2D':
        """
        Adds two vectors
        :param other:
        :return:
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> 'Vector2D':
        """
        Subtracts two vectors
        :param other:
        :return:
        """
        return Vector2D(self.x - other.x, self.y - other.y)

    def __truediv__(self, other) -> 'Vector2D':
        """
        Divides two vectors
        :param other:
        :return:
        """
        return Vector2D(self.x / other, self.y / other)

    def __str__(self) -> str:
        """
        Returns the string representation of the vector
        :return:
        """
        return f"({self.x}, {self.y})"
