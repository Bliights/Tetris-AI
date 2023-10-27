gridWidth = 10
gridHeight = 20
cellSize = 20
screenWidth = gridWidth*cellSize
screenHeight = gridHeight*cellSize

fps = 25
maxFps =60
gravity = 10

shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 1], [0, 0, 1]],
]

colors = {"black": (0, 0, 0), 
          "white": (255, 255, 255),
          "blue": (0, 0, 255),
          "green": (0, 255, 0),
          "red": (255, 0, 0),
          "yellow": (255, 255, 0),
          "purple": (255, 0, 255),
          "cyan": (0, 255, 255)
          }
