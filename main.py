import pygame
import assets
import levels
import random



# Define screen size
boardX = 10
boardY = 10
tilesize = 60
width = boardX * tilesize
height = boardY * tilesize
screen = pygame.display.set_mode((width, height))

class Battery:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def draw(self):
        screen.blit(assets.battery, (self.y*tilesize, self.x*tilesize))

class Light:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = 0
    
    def draw(self):
        if self.state==0:
            screen.blit(assets.bulb_off, (self.y*tilesize,self.x*tilesize))
        if self.state==1:
            screen.blit(assets.bulb_on, (self.y*tilesize,self.x*tilesize))

class Wire:
    def __init__(self, x:int, y:int, off:pygame.surface, on:pygame.surface, up=False,down=False,left=False,right=False) -> None:
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*tilesize,y*tilesize,tilesize,tilesize) #Hit box for mouse

        self.rot = 0
        self.state = 0

        self.off = off
        self.on = on

        self.up = up
        self.down = down
        self.left = left
        self.right = right

        for i in range(random.randint(0,3)):
            self.rotate()
    
    def draw(self,_screen):
        if self.state == 0:
            img = pygame.transform.rotate(self.off, self.rot*90)
        else:
            img = pygame.transform.rotate(self.on, self.rot*90)
        screen.blit(img,self.rect)
    
    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def rotate(self):
        self.up, self.left, self.down, self.right = self.left, self.down, self.right, self.up
        self.rot = (self.rot - 1) % 4
    
    #Only called on mouse up event
    def handle_click(self):
        if self.is_hovered():
            self.rotate()



def updateGrid(grid, batteries, lights):
    #Reset all wires
    for row in grid:
        for wire in row:
            if isinstance(wire, Wire):
                wire.state = 0

    #BFS all wires connected to batteries
    for i in batteries:
        queue = []
        queue.append([i.x,i.y])
        while queue:
            j = queue.pop(0)
            if grid[j[0]][j[1]].state == 1:
                continue
            grid[j[0]][j[1]].state = 1
            if grid[j[0]][j[1]].up:
                if j[0] > 0 and isinstance(grid[j[0]-1][j[1]], Wire) and grid[j[0]-1][j[1]].down:
                    queue.append((j[0]-1,j[1]))
            if grid[j[0]][j[1]].down:
                if j[0] < len(grid)-1 and isinstance(grid[j[0]+1][j[1]], Wire) and grid[j[0]+1][j[1]].up:
                    queue.append((j[0]+1,j[1]))
            if grid[j[0]][j[1]].left:
                if j[1] > 0 and isinstance(grid[j[0]][j[1]-1], Wire) and grid[j[0]][j[1]-1].right:
                    queue.append((j[0],j[1]-1))
            if grid[j[0]][j[1]].right:
                if j[1] < len(grid[0])-1 and isinstance(grid[j[0]][j[1]+1], Wire) and grid[j[0]][j[1]+1].left:
                    queue.append((j[0],j[1]+1))
    
    for i in lights:
        i.state = grid[i.x][i.y].state




def draw_text(text, size, x, y, color=assets.BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def generate_level():
    grid = [[Wire(-1,-1,assets.bulb_off,assets.bulb_on)]* 10 for _ in range(10)]
    batteries = []
    lights = []
    for i in range(10):
        for j in range(10):
            if levels.a[i][j] == 'P':
                grid[i][j] = Wire(j,i,assets.wire1_off,assets.wire1_on,up=True)
                batteries.append(Battery(i,j))
            if levels.a[i][j] == 'L':
                grid[i][j] = Wire(j,i,assets.wire1_off,assets.wire1_on,up=True)
                lights.append(Light(i,j))
            if levels.a[i][j] == 'b':
                grid[i][j] = Wire(j,i,assets.wire2b_off,assets.wire2b_on,up=True,right=True)
            if levels.a[i][j] == 'a':
                grid[i][j] = Wire(j,i,assets.wire2a_off,assets.wire2a_on,up=True,down=True)
            if levels.a[i][j] == 3:
                grid[i][j] = Wire(j,i,assets.wire3_off,assets.wire3_on,up=True,down=True,right=True)
            if levels.a[i][j] == 4:
                grid[i][j] = Wire(j,i,assets.wire4_off,assets.wire4_on,up=True,down=True,right=True,left=True)

    return grid, batteries, lights


def main():
    pygame.init()
    pygame.display.set_caption("Light BULBS!")

    grid, batteries, lights = generate_level()
    updateGrid(grid,batteries,lights)

    restart = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #Rotate wires on click
            if event.type == pygame.MOUSEBUTTONUP:
                for row in grid:
                    for button in row:
                        button.handle_click()
                updateGrid(grid,batteries,lights)
                click_detected = True
            
            #Restart game on R pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    running = False
                    restart = True

        # Draw game elements
        screen.fill(assets.BLACK)
        for row in grid:
            for button in row:
                button.draw(screen)
        for battery in batteries:
            battery.draw()
        for light in lights:
            light.draw()

        pygame.display.flip()
    
    return restart



while True:
    restart = main()
    if not restart:
        break
