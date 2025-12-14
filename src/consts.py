# Size definitions
CELL_SIZE = 40          # Must be greater than 4 to display properly
NB_CELLS = 16

# Window constants
WINDOW_SIZE = CELL_SIZE * NB_CELLS
WINDOW_TITLE = "A*"

# Color definitions
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
FUCHSIA = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

COLOR_NAME_MAP = {
    BLACK: "Black",
    RED: "Red",
    GREEN: "Green",
    BLUE: "Blue",
    YELLOW: "Yellow",
    FUCHSIA: "Fuchsia",
    CYAN: "Cyan",
    WHITE: "White"
}

# Cell collisions masks
COL_LEFT = 1
COL_RIGHT = 2
COL_UP = 4
COL_DOWN = 8

# Player moves
MOVE_UP = 1
MOVE_DOWN = 2
MOVE_LEFT = 3
MOVE_RIGHT = 4

# Player decision time (in seconds)
DECISION_TIME = 30

# Pawn colors mapping
PAWN_GOAL = 1
PAWN_COLORS = {
    1: GREEN,
    2: BLUE,
    3: FUCHSIA
}
PAWN_NUMBER = 3
PAWN_SIZE = CELL_SIZE // 2.5