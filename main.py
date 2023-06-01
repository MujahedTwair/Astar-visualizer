import pygame 
from queue import PriorityQueue

WIDTH = 600               #For display screen (as a square)

WIN = pygame.display.set_mode((WIDTH,WIDTH))  #create the screen
pygame.display.set_caption("maze using A* path finding") #give it caption

#Declare colors :
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Cell:
    def __init__(self,row,col,width, total_rows) :
        self.row = row
        self.col = col
        self.x = col*width   #like fixed position
        self.y = row*width
        self.color = WHITE   #initial value
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_blocked(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def is_reset(self):
        return self.color == WHITE
    
    def make_start(self):
        self.color = ORANGE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN        

    def make_blocked(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self,win): 
        pygame.draw.rect(win, self.color , (self.x , self.y, self.width, self.width))            

    def update_neighbors(self, grid):
        # self.neighbors =[]
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1), # Up, Down, Left, Right
            (-1, -1), (-1, 1), (1, -1), (1, 1) # Diagonal directions
        ]
        for d_row, d_col in directions:
            new_row, new_col = self.row + d_row, self.col + d_col
            if 0 <= new_row < self.total_rows and 0 <= new_col < self.total_rows:
                neighbor = grid[new_row][new_col]
                if not neighbor.is_blocked():
                    self.neighbors.append(neighbor)

                


    
def h(p1, p2): #heuristic function
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2) 


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()

    draw()    
    current.make_start()
       



def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

 #   g_score = {cell: float("inf") for row in grid for cell in row}
 #   f_score = {cell: float("inf") for row in grid for cell in row}

    g_score ={}
    f_score={}
    for row in grid:
        for cell in row:
            g_score[cell] = float("inf")
            f_score[cell] = float("inf")

    g_score[start] = 0        
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} #because the priority queue doesn't have any thing to tell us if a cell is in the queue or not(can remove from proiorityQ,but cant check if an item in priorityQ)
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] #get the third elemnt of tuple -that have the high priority- (minimum f_score) (Return The Cell) and remove from queue
        open_set_hash.remove(current)

        if current == end:
#            print(g_score[current],count) #count = number of expanded nodes, g-score : the cost
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + move_cost(current, neighbor)

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos() , end.get_pos())
                if neighbor not in open_set_hash:
                    count +=1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()


        if current != start:
            current.make_closed()

        pygame.time.delay(10)
        draw()    

    cont=0
    for row in grid:
        for cell in row:
            if(cell.is_closed()):
                cont +=1
    print("red closed : ",cont)            
    return False

def move_cost(current, neighbor):
    if current.row == neighbor.row or current.col == neighbor.col:
        return 10
    else:
        return 14


def make_grid(rows, width): #dataStructure list to save all nodes
    grid = []
    gap = width // rows #Integer division def , gap = width of each cube(cell)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell =  Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid        
    
#draw gray lines between cells
def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win , GREY , (0, i * gap), (width , i * gap)) #draw horizintal lines

        pygame.draw.line(win , GREY , (i * gap, 0), (i * gap , width)) #draw vertical lines


def draw(win, grid, rows, width):
    
    win.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid_lines(win, rows, width)
    
    pygame.display.update()
#   pygame.time.delay(50)

#function to take a mouse position and veiw what cube(cell) clicked on
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x,y = pos

    row = y // gap
    col = x // gap

    return row,col

def main(win, width):
    ROWS = 25
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


            if pygame.mouse.get_pressed()[0]: #press on the left mouse button
                pos = pygame.mouse.get_pos()  #the position of the pi game mouse coordinates xy
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                if not start and cell != end and not cell.is_blocked(): #or : if not start and cell.is_reset()
                    start = cell
                    start.make_start()

                elif not end and cell != start and not cell.is_blocked(): #or : elif not end and cell.is_reset()
                    end = cell
                    end.make_end()

                elif cell != end and cell != start:
                    cell.make_blocked() 

            elif pygame.mouse.get_pressed()[2]: #press on the rifht mouse  
                pos = pygame.mouse.get_pos()  #the position of the pi game mouse coordinates xy
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    

main(WIN , WIDTH)
