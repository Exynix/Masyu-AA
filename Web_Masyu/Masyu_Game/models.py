from django.db import models

# Create your models here.
class Circle(models.Model):
    BLACK = 'B'
    WHITE = 'W'
    CIRCLE_COLORS = [
        (BLACK, 'Black'),
        (WHITE, 'White'),
    ]

    color = models.CharField(max_length=1, choices=CIRCLE_COLORS)
    x = models.IntegerField()
    y = models.IntegerField()

    def __str__(self):
        return f"{self.get_color_display()} Circle at ({self.x}, {self.y})"


class GameBoard(models.Model):
    size = models.IntegerField()
    circles = models.ManyToManyField(Circle)

    def __str__(self):
        return f"GameBoard {self.id} ({self.size}x{self.size})"

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            size = int(lines[0].strip())
            game_board = cls.objects.create(size=size)
            for line in lines[1:]:
                row, col, circle_type = map(int, line.strip().split(','))
                color = Circle.WHITE if circle_type == 1 else Circle.BLACK
                circle = Circle.objects.create(x=row, y=col, color=color)
                game_board.circles.add(circle)
                print(f"Added {color} circle at ({row}, {col})")
            return game_board

