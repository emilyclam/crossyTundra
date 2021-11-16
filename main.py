"""
X basic setup
X animate user (grid system)
X have the screen constantly be moving down (screen scroll-er)
X setup an event that creates lanes of water (same size as grid) (that also move)
    X @ clock 30 and scroll_speed 2, the screen moves down at ~66.7px/sec (1000/30 * 2)
    - later: in the period of plain snow, display directions?
    X Water object... attr: y, direction+speed (+/-), list of Ice
    X Ice object... attr: width, x, inherit y, direction, and speed from water
    X I used a function to screen scroll everything
X if user is on an ice block, the user-x is influenced by it (velocity is the same)
    X use collisions to check if user is standing on a block
    X if user collides with water, but not block, then they drown (if more than half of user is off... use center-x)
X once objects leave the screen, delete them
X if player.bottom hits bottom of screen, restart game

NEXT:
- snow for breaks
- home/directions screen
- end screen
- coins! + coin tracker...
- visuals!!!
  - player: image?
  - water: have a cool gradient?
  - ice: bobbing effect?
- sound effects!



WHAT I LEARNED
- the reason you should keep functions simple:
if a function does two things: 1) return T/F 2) moves a user accordingly, you can only ever call that function once!
because if you move it more than that, it'll move user at a rate 2x or nx more than it's supposed to!
it's a nightmare to try to debug!
It's okay for a function to just be 3 lines long! if there is more going on than what can fit inside the
function title, then you should probably split it up into more functions...
I learned what the debugging function does; it's super helpful...

- learn more about sprites and groups... how to loop through groups like i looped through lane_list?
-


FIX
- some ice blocks in a lane will just not move
- or blocks in the same lane will move at different velocities
    - every time you step on a lane print out the velocity of the lane and each block
    - or make a function han does it so i can easily run it when i'm debugging
"""

import pygame
import sys
import random
import water


# moves and draws player and lanes
# in the future if i add more objects (coins?? snow for breather?? scenery things/things in the water?) i
# might give them their own function and then put it all into one big function?
def scroll_screen():
    clean_screen()

    # scrolls and draws all the lanes and ice
    for lane in lane_list:
        lane.rect.y += scroll_speed
        pygame.draw.rect(screen, water_color, lane.rect)
        lane.ice_list.update(lane.rect.y)
        lane.ice_list.draw(screen)

    # scrolls and draws user
    player.rect.y += scroll_speed
    pygame.draw.rect(screen, player_color, player.rect)


# checks if user is standing on a water lane
def on_lane():
    for lane in lane_list:
        if lane.rect.bottom >= player.rect.centery >= lane.rect.top:
            return lane
    return False


# returns the lane that user is on
def on_ice():
    if not on_lane():
        return False
    elif on_lane():
        for lane in lane_list:
            this_ice = pygame.sprite.spritecollide(player, lane.ice_list, False)  # holds ice player is standing on or F
            if this_ice and this_ice[0].rect.left <= player.rect.centerx <= this_ice[0].rect.right:
                # print(this_ice[0].rect.left, player.rect.centerx, this_ice[0].rect.right)
                # print(this_ice[0].rect.left, player.rect.centerx, this_ice[0].rect.right)
                return lane
        # user isn't standing on any of the lanes
        return False


def player_motion():
    if on_ice():
        this_lane = on_ice()
        player.rect.x += this_lane.velocity
        player.rect.y = this_lane.rect.y


# checks if the player has drowned or left the screen --> T/F
def player_alive():
    if not on_ice() and on_lane():
        print("you drowned")
        return False
    if not 0 < player.rect.centerx < SCREEN_WIDTH:
        print("you left the screen x")
        return False
    #if not 0 < player.rect.centery < SCREEN_HEIGHT:
     #   return False
    # idk maybe the end screen will be different
    return True


# deletes lane obj (+ice) if they scroll past the screen and return the cleaned lane_list
def clean_screen():
    new_lane_list = [lane for lane in lane_list if lane.rect.y < SCREEN_HEIGHT+50]
    return new_lane_list


# for debugging: checks that the velocity of the blocks match the vel of their lane
def check_velocity():
    this_lane = on_lane()
    print(this_lane.velocity)
    for ice in this_lane.temp_list:
        print(ice.velocity)


# i only did this so player can be a sprite...
class Player(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        self.size = size
        self.rect = pygame.Rect(SCREEN_WIDTH/2 - grid/2, SCREEN_HEIGHT/2, size, size)


# setup
pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Tundra")

# game variables
bg_color = (184, 217, 216)
grid = 40  # each grid-square is 30x30
scroll_speed = 2
all_sprites = pygame.sprite.Group()
game_state = "active"  # active or dead

# player
PLAYER_SIZE = grid * 1/2
player_color = (255, 255, 255)
player = Player(PLAYER_SIZE)
all_sprites.add(player)

# water
water_color = (41, 179, 174)
SPAWNWATER = pygame.USEREVENT
pygame.time.set_timer(SPAWNWATER, int(1000*4/5))  # 2//3 * 1000
MAX_VELOCITY = 7
lane_list = []


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.rect.top -= grid
            if event.key == pygame.K_s:
                player.rect.bottom += grid
            if event.key == pygame.K_d:
                player.rect.right += grid
            if event.key == pygame.K_a:
                player.rect.left -= grid
        if event.type == SPAWNWATER:
            vel = random.randint(-MAX_VELOCITY*10, MAX_VELOCITY*10)/10
            new_lane = water.WaterLane(-grid, vel)
            lane_list.append(new_lane)
    if game_state == "active":
        if not player_alive():
            game_state = "dead"

        # visuals
        screen.fill(bg_color)
        scroll_screen()
        player_motion()
        lane_list = clean_screen()

    pygame.display.update()
    clock.tick(25)
