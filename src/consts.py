# Size definitions
CELL_SIZE = 40          # Must be greater than 4 to display properly
NB_CELLS = 16

# Window constants
WINDOW_SIZE = CELL_SIZE * NB_CELLS
WINDOW_GUI_HEIGHT = 150
WINDOW_TITLE = "Rasende Roboter"

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
DECISION_TIME = 60

# Pawn ids
RED_ID = 1
GREEN_ID = 2
BLUE_ID = 3
YELLOW_ID = 4

# Pawn colors mapping
PAWN_GOAL = 1
PAWN_COLORS = {
    RED_ID: RED,
    GREEN_ID: GREEN,
    BLUE_ID: BLUE,
    YELLOW_ID: YELLOW
}

# Pawn possible goal coordinates (for 0-15 square grid)
PAWN_GOAL_COORDS = {
    RED_ID: [(2,5),(2,14),(11,14),(14,1)],
    GREEN_ID: [(1,10),(5,4),(13,6),(14,13)],
    BLUE_ID: [(6,1),(6,13),(11,2),(12,9)],
    YELLOW_ID: [(1,3),(4,9),(10,7),(9,12)]
}
PAWN_NUMBER = 4

# Game states
STATE_INITIALIZING = 0
STATE_PLAYER_TURN = 1
STATE_PLAYER_END = 2
STATE_COMPUTER_CALCULATING = 3
STATE_COMPUTER_TURN = 4
STATE_RESULTS = 5
