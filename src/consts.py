# Size definitions
CELL_SIZE = 20          # Must be greater than 4 to display properly
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

# Cell collisions masks
COL_LEFT = 1
COL_RIGHT = 2
COL_UP = 4
COL_DOWN = 8