import pygame
from utils import Block,Agent,create_matrix,ban_blocks,Point
# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid App by mosTafa Arshadi")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL = (46, 46, 46)
TARGET = (173, 35, 35)
START_POINT = (35, 173, 76)
GRAY = (128, 128, 128)
WAY = (235,235,42)

# Set the grid size and cell size
grid_size = 30
cell_size = int(550/grid_size)

# Initialize grid
grid = [[WHITE for _ in range(grid_size)] for _ in range(grid_size)]

error = ""
# Boolean variables to keep track of active modes
WALL_mode_active = False
TARGET_mode_active = False
START_POINT_mode_active = False
white_mode_active = False

current_color = WHITE
# Function to draw the grid
def draw_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            pygame.draw.rect(screen, grid[row][col], (col * cell_size, row * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, GRAY, (col * cell_size, row * cell_size, cell_size, cell_size),1)

def is_clicked(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
        return True
    return False

def draw_button_with_text(x, y, width, height, text):
    pygame.draw.rect(screen, GRAY, (x, y, width, height))
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    
    font = pygame.font.Font(None, 32)
    text_render = font.render(text, True, BLACK)
    text_rect = text_render.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_render, text_rect)

def clear_way():
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == WAY:
                grid[i][j] = WHITE
RUN_LOC = (screen_width - 100 ,10,100,50)
IS_DRAWING = False
# Game loop
running = True
while running:
    # Clear the screen
    screen.fill(BLACK)

    # Process events
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYUP and event.unicode == "1":
            WALL_mode_active = True
            TARGET_mode_active = False
            START_POINT_mode_active = False
            current_color = WALL
            white_mode_active =False


        elif event.type == pygame.KEYUP and event.unicode == "2":
            TARGET_mode_active = True
            WALL_mode_active = False
            START_POINT_mode_active =False
            current_color = TARGET
            white_mode_active =False


        elif event.type == pygame.KEYUP and event.unicode == "3":
            START_POINT_mode_active = True
            TARGET_mode_active =False
            WALL_mode_active=False
            white_mode_active =False
            current_color = START_POINT

        elif event.type == pygame.KEYUP and event.unicode == "4":
            START_POINT_mode_active = False
            TARGET_mode_active =False
            WALL_mode_active=False
            white_mode_active = True
            current_color = WHITE

        elif event.type == pygame.KEYUP and event.unicode == "5":
            grid = [[WHITE for _ in range(grid_size)] for _ in range(grid_size)]
            error = ""
        
        elif event.type == pygame.KEYUP and event.unicode == "6":
            clear_way()
            
            error = ""
            
        elif event.type == pygame.KEYUP and event.unicode == "7":
            for i in range(grid_size):
                    for j in range(grid_size):
                        if grid[i][j] == WALL:
                            grid[i][j] = WHITE
                           

        elif event.type == pygame.MOUSEBUTTONUP:
            IS_DRAWING = False

        elif event.type == pygame.MOUSEMOTION and IS_DRAWING:
            if WALL_mode_active :
                # WALL mode: Clicking on any box makes it WALL

                x, y = pygame.mouse.get_pos()
                if x >= 0 and x <= grid_size * cell_size and y >= 0 and y <= grid_size * cell_size:
                    col = x // cell_size
                    row = y // cell_size
                    grid[row][col] = WALL
            
            elif white_mode_active:
                # TARGET mode: Only one box can be TARGET at a time
                x, y = pygame.mouse.get_pos()
                if x >= 0 and x <= grid_size * cell_size and y >= 0 and y <= grid_size * cell_size:
                    col = x // cell_size
                    row = y // cell_size
                    grid[row][col] = WHITE

        elif event.type == pygame.MOUSEBUTTONDOWN:
            IS_DRAWING = True
            if(is_clicked(*RUN_LOC)):
                clear_way()
                error = ""
                lst = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
                start_point = None
                target = None
                to_ban = []
                create_matrix(grid_size,grid_size)
                for i in range(grid_size):
                    for j in range(grid_size):
                        if grid[i][j] == TARGET:
                            lst[i][j] = 1
                            target = Block.get_block(Point(i,j))
                        elif grid[i][j] == WALL:
                            lst[i][j] = 2
                            to_ban.append(Point(i,j))
                        elif grid[i][j] == START_POINT:
                            lst[i][j] = 3
                            start_point = Block.get_block(Point(i,j))

                        elif grid[i][j] == WHITE:
                            lst[i][j] = 0
                ban_blocks(to_ban)
                attemts = 0
                done = False
                while 1:
                    if attemts == 3:break
                    player = Agent(start_point)
                    paths = (player.start_moving(target))
                    found = False
                    try:
                        while not found: 
                            prev = paths[target]
                            if prev == player.start_block:
                                break
                            target = prev
                            grid[target.x][target.y] = WAY
                        done = True
                        break
                    except Exception as ex:
                        print(ex)
                        attemts+=1
                        continue
                if not done:
                    
                    error = "No way"

                
                            
                
            

            

            elif TARGET_mode_active:
                # TARGET mode: Only one box can be TARGET at a time
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if x >= 0 and x <= grid_size * cell_size and y >= 0 and y <= grid_size * cell_size:
                        clear_way()

                        col = x // cell_size
                        row = y // cell_size
                        for r in range(grid_size):
                            for c in range(grid_size):
                                if grid[r][c] == TARGET:
                                    grid[r][c] = WHITE
                        
                        grid[row][col] = TARGET
            
            

            elif START_POINT_mode_active:
                # START_POINT mode: Only one box can be START_POINT at a time
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    if x >= 0 and x <= grid_size * cell_size and y >= 0 and y <= grid_size * cell_size:
                        clear_way()

                        col = x // cell_size
                        row = y // cell_size
                        for r in range(grid_size):
                            for c in range(grid_size):
                                if grid[r][c] == START_POINT:
                                    grid[r][c] = WHITE
                        grid[row][col] = START_POINT


    # Draw the grid
    draw_grid()

    # Draw buttons
    pygame.draw.circle(screen, GRAY, (30, screen_height - 30),28)
    pygame.draw.circle(screen, current_color, (30, screen_height - 30),25)
    draw_button_with_text(*RUN_LOC,"RUN")
    if len(error) > 0:
        draw_button_with_text(screen_width-100,50,100,50,error)
    draw_button_with_text(screen_width-200,100,200,50,"1 = WALL")
    draw_button_with_text(screen_width-200,150,200,50,"2 = TARGET")
    draw_button_with_text(screen_width-200,200,200,50,"3 = START_POINT")
    draw_button_with_text(screen_width-200,250,200,50,"4 = white")
    draw_button_with_text(screen_width-200,300,200,50,"5 = clear board")
    draw_button_with_text(screen_width-200,350,200,50,"6 = clear ways")
    draw_button_with_text(screen_width-200,400,200,50,"7 = clear walls")
    draw_button_with_text(screen_width//2 ,screen_height-50,200,50,"mosTafa Arshadi")
    

    # Update the display
    pygame.display.update()

# Quit Pygame
pygame.quit()