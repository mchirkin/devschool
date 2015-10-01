"""
HeadHunter DEVSchool
Задача        : Точки
Автор решения : Чиркин М.В.
Дата          : 01.10.2015
"""


import math


class Point:
    """
    x         - координата точки по оси OX
    y         - координата точки по оси OY
    radius    - радиус точки (расстояние до ближайшей точки)
    neighbors - список соседей на расстоянии не более 2ух радиусов точки
    """

    def __init__(self, x, y,
                 radius=math.inf, neighbors=None):
        self.x = x
        self.y = y
        self.radius = radius
        if neighbors is None:
            self.neighbors = list()

    def distance_to_point(self, point):
        """
        Нахождение Евклидового расстояния от точки до точки
        """

        return math.sqrt((point.x - self.x)**2 + (point.y - self.y)**2)

    def get_coordinate(self, coordinate):
        """
        Получение заданной координаты точки
        """

        return [self.x, self.y]['y' == coordinate]


class Node:
    """
    center     - центральная точка узла KD-дерева
    sort_coord - координата, по которой сортируются точки
    left       - левое поддерево
    right      - правое поддерево
    """

    def __init__(self, center, sort_coord=None, left=None, right=None):
        self.center = center
        self.left = left
        self.right = right
        self.sort_coord = sort_coord


def sort_x(point):
    """
    Ключ для функции sorted() - cортировка по X-координате
    """

    return point.x


def sort_y(point):
    """
    Ключ для функции sorted() - cортировка по Y-координате
    """

    return point.y


def build_tree(points, coordinate):
    """
    Построение KD-дерева (k=2)
    """

    if len(points) == 0:
        return

    sorted_points = [sorted(points, key=sort_x), sorted(points, key=sort_y)]['y' == coordinate]

    middle = len(sorted_points)//2
    # Центральная точка узла дерева
    center = sorted_points[middle]
    # Точки левого поддерева
    left_points = sorted_points[0:middle]
    # Точки правого поддерева
    right_points = sorted_points[middle+1:]
    # Координата, по которой будут сортироваться
    # точки следующего уровня дерева
    next_coordinate = ['x', 'y']['x' == coordinate]

    node = Node(center, coordinate)
    node.left = build_tree(left_points, next_coordinate)
    node.right = build_tree(right_points, next_coordinate)

    return node


def search_nn(node, point, search_range=None):
    """
    Поиск ближайшего соседа и соседей в пределах search_range
    """

    # "Дальнее" поддерево, в котором не производился поиск
    far_tree = None
    # Расстояние от точки до узла
    dist = point.distance_to_point(node.center)
    point.radius = [point.radius, dist][dist < point.radius and point != node.center]

    sort_coord = node.sort_coord
    point_coord = point.get_coordinate(sort_coord)
    node_coord = node.center.get_coordinate(sort_coord)

    # Если координата точки меньше координаты центра узла,
    # то продолжаем поиск в левом поддереве, иначе - в правом
    if point_coord < node_coord:
        if node.left is not None:
            search_nn(node.left, point, search_range)
        if node.right is not None:
            far_tree = node.right
    else:
        if node.right is not None:
            search_nn(node.right, point, search_range)
        if node.left is not None:
            far_tree = node.left

    # Радиус окружности, в которой могут находиться соседи/сосед
    radius = [search_range, point.radius][search_range is None]

    # Если ищем не одного ближайшего соседа,
    # то проверяем точку узла на принадлежность области поиска
    if search_range is not None and dist <= search_range and point != node.center:
        point.neighbors.append(node.center)

    # Если область поиска пересекает "дальнее" поддерево,
    # то там могут быть точки-соседи
    if node_coord - point_coord <= radius and far_tree is not None:
        search_nn(far_tree, point, search_range)


points_number = int(input("Number of points: "))
points_list = list()

for i in range(1, points_number + 1):
    print("#", i, " Enter point's coordinates")
    x_coord = int(input("x = "))
    y_coord = int(input("y = "))
    points_list.append(Point(x_coord, y_coord))

# Строим KD-дерево и получаем его "корень"
root = build_tree(points_list, 'x')

for p in points_list:
    # Поиск ближайшего соседа,
    # расстояние до которого является радиусом точки
    search_nn(root, p)
    # Поиск соседей на расстоянии не более 2ух радиусов точки
    search_nn(root, p, p.radius*2)

    print("\nPoint:", (p.x, p.y))
    print("Radius:", p.radius)
    print("Number of neighbors:", len(p.neighbors))
