import collections
import microbit
import random


Point = collections.namedtuple('Point', ['x', 'y'])


class GameOfLife:
    def __init__(self, data):
        self.size = Point(x=len(data[0]), y=len(data))
        self.pos = Point(0, 0)
        self.data = data

    def neighbours(self, point):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                x = (point.x + dx) % self.size.x
                y = (point.y + dy) % self.size.y
                yield Point(x, y)

    def neighbour_counts(self):
        nc = [[0 for x in range(self.size.x)] for y in range(self.size.y)]
        for x in range(self.size.x):
            for y in range(self.size.y):
                if self.data[y][x]:
                    for n in self.neighbours(Point(x, y)):
                        nc[n.y][n.x] += 1
        return nc

    def step(self):
        neighbour_counts = self.neighbour_counts()
        newgen = [[0 for x in range(self.size.x)] for y in range(self.size.y)]
        for x in range(self.size.x):
            for y in range(self.size.y):
                count = neighbour_counts[y][x]
                current_value = self.data[y][x]
                if count == 3 or (count == 2 and current_value):
                    newgen[y][x] = 1
        self.data = newgen

    def gen_image(self):
        img_data = []
        for dy in range(5):
            for dx in range(5):
                x = (self.pos.x + dx) % self.size.x
                y = (self.pos.y + dy) % self.size.y
                img_data.append('9' if self.data[y][x] else '0')
            img_data.append(':')
        return microbit.Image(''.join(img_data[:-1]))

    def move(self, dx, dy):
        x = (self.pos.x + dx) % self.size.x
        y = (self.pos.y + dy) % self.size.y
        self.pos = Point(x, y)

    def is_alive(self):
        return any(any(p for p in row) for row in self.data)


SIZE = 10
CLOCK = 250

while __name__ == '__main__':
    game = GameOfLife([[random.randint(0, 1) for x in range(SIZE)]
                       for y in range(SIZE)])
    time = 0
    step = 500

    while True:
        microbit.sleep(CLOCK)
        time += CLOCK
        acc_x = max(-2, min(2, microbit.accelerometer.get_x() // 500))
        acc_y = max(-2, min(2, microbit.accelerometer.get_y() // 500))
        game.move(acc_x, acc_y)
        if time >= step:
            game.step()
            time %= step
        microbit.display.show(game.gen_image())
        if microbit.button_a.was_pressed() or not game.is_alive():
            break
