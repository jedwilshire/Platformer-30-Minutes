import pygame
""" Constants """
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

FPS = 60  # frames per second
TILE_ROWS = 24
TILE_COLS = 32
TILE_SIZE = 25
WIDTH = TILE_COLS * TILE_SIZE # 800
HEIGHT = TILE_ROWS * TILE_SIZE # 600
MAX_FALL = 15
GRAVITY = 1
SPEED = 4
JUMP = 12

class Game:
    def __init__(self):
        self.sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.playing = True
        self.map = Map('level1.txt')
        self.player = Player(self, (5 * TILE_SIZE, 23 * TILE_SIZE))
    
    def update_game(self):
        self.sprites.update()
    
    def update_screen(self):
        self.screen.blit(self.map.image, (0, 0))
        self.sprites.draw(self.screen)
        pygame.display.flip()
        
    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                
    def gameloop(self):
        while self.playing:
            self.clock.tick(FPS)
            self.update_events()
            self.update_game()
            self.update_screen()
    

class Map:
    def __init__(self, level):
        self.tiles = []
        with open(level, 'r') as f:
            for line in f:
                self.tiles.append(line.strip())
        self.make_image()
    
    def collide_wall(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        return self.tiles[y][x] == 'X'
    
    def make_image(self):
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(WHITE)
        self.block = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.block.fill(BLACK)
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == 'X':
                    self.image.blit(self.block, (x * TILE_SIZE, y * TILE_SIZE))

class CollideSprite(pygame.sprite.Sprite):
    def __init__(self, game, rect, pos):
        super().__init__()
        self.rect = rect
        self.rect.midbottom = pos
        self.game = game
        self.game.sprites.add(self)
        self.map = self.game.map
    
    def move(self, dx = 0, dy = 0):
        if dx > 0:
            for i in range(dx):
                self.rect.x += 1
                if self.map.collide_wall(self.rect.midright):
                    self.rect.x -= 1
                    return True
        if dx < 0:
            for i in range(abs(dx)):
                self.rect.x -= 1
                if self.map.collide_wall(self.rect.midleft):
                    self.rect.x += 1
                    return True    
        if dy > 0:
            for i in range(dy):
                self.rect.y += 1
                if self.map.collide_wall(self.rect.midbottom):
                    self.rect.y -= 1
                    return True
        
        if dy < 0:
            for i in range(abs(dy)):
                self.rect.y -= 1
                if self.map.collide_wall(self.rect.midtop):
                    self.rect.y += 1
                    return True

        return False
    
class GravitySprite(CollideSprite):
    def __init__(self, game, rect, pos):
        super().__init__(game, rect, pos)
        self.dx = 0
        self.dy = 0
        self.on_ground = False
        
    def update(self):
        self.on_ground = False
        self.dy = min(MAX_FALL, self.dy + GRAVITY)
        if self.move(dy = self.dy):
            if self.dy > 0: # falling
                self.on_ground = True
            self.dy = 0
            
        if self.move(dx = self.dx):
            self.dx = 0
            
class Player(GravitySprite):
    def __init__(self, game, pos):
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        super().__init__(game, self.rect, pos)
    
    def update(self):
        self.dx = 0
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.dx = -SPEED
        if keys[pygame.K_RIGHT]:
            self.dx = SPEED
        if keys[pygame.K_UP] and self.on_ground:
            self.dy = -JUMP
        super().update()
        


        
        


def main():
    pygame.init()
    app = Game()
    app.gameloop()
    pygame.quit()

if __name__ == '__main__':
    main() 