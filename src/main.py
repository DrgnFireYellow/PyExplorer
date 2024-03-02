import pygame
import tiles
import biomes
import os
import math
import random

pygame.init()
print(f"Loaded {len(tiles.tiles)} tiles")


screeninfo = pygame.display.Info()
clock = pygame.time.Clock()

font = pygame.font.Font(pygame.font.get_default_font(), 10)

window = pygame.display.set_mode((screeninfo.current_w, screeninfo.current_h))
pygame.display.set_caption("PyExplorer")

solids = []

player_right = pygame.image.load(os.path.join("textures", "player", "right.png"))
player_right = pygame.transform.scale(
    player_right, (tiles.TILESIZE, tiles.TILESIZE * 2)
)

player_left = pygame.transform.flip(player_right, True, False)

player_x = 0
player_y = 0

WALK_SPEED = 3

def load_map(map):
    global solids
    solids = []
    for ycoord, y in enumerate(map):
        for xcoord, x in enumerate(y):
            window.blit(
                tiles.tiles[x],
                (
                    xcoord * tiles.TILESIZE - player_x,
                    ycoord * tiles.TILESIZE - player_y,
                ),
            )
            if x:
                solids.append(
                    pygame.Rect(
                        xcoord * tiles.TILESIZE - player_x,
                        ycoord * tiles.TILESIZE - player_y - 2,
                        tiles.TILESIZE,
                        tiles.TILESIZE,
                    )
                )


direction = 1

biome = "plains"

map = []

for i in range(5):
    map.append([0] * 64)

map.append([biomes.biomes[biome]["surface"]] * 64)
map.append([biomes.biomes[biome]["middle"]] * 64)

if biomes.biomes[biome]["trees"]["enabled"]:
    tree = False
    for i in range(63):
        if random.randint(0, 3) == 3 and not tree:
            map[4][i] = biomes.biomes[biome]["trees"]["log"]
            map[3][i] = biomes.biomes[biome]["trees"]["log"]
            map[2][i] = biomes.biomes[biome]["trees"]["leaves"]
            map[1][i] = biomes.biomes[biome]["trees"]["leaves"]
            map[2][i + 1] = biomes.biomes[biome]["trees"]["leaves"]
            map[2][i - 1] = biomes.biomes[biome]["trees"]["leaves"]
            tree = True
        else:
            tree = False

for i in range(10):
    map.append([biomes.biomes[biome]["bottom"]] * 64)

jump_remaining = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_location = pygame.mouse.get_pos()
            player_tile = (
                round(player_x / tiles.TILESIZE),
                round(player_y / tiles.TILESIZE),
            )
            mouse_tile = (
                math.floor(mouse_location[0] / tiles.TILESIZE) + player_tile[0],
                math.floor(mouse_location[1] / tiles.TILESIZE) + player_tile[1],
            )
            if event.button == 3 and map[mouse_tile[1]][mouse_tile[0]] == 0:
                map[mouse_tile[1]][mouse_tile[0]] = 1
            elif event.button == 1:
                map[mouse_tile[1]][mouse_tile[0]] = 0

    old_player_x = player_x
    old_player_y = player_y
    grounded = False

    keys = pygame.key.get_pressed()

    window.fill(pygame.Color("skyblue"))
    load_map(map)
    player_y += 4

    if keys[pygame.K_RIGHT]:
        player_x += WALK_SPEED
        direction = 1

    if keys[pygame.K_LEFT]:
        player_x -= WALK_SPEED
        direction = -1

    player_rect = pygame.Rect(
        window.get_width() / 2, 0, tiles.TILESIZE, tiles.TILESIZE * 2
    )

    for solid in solids:
        if solid.colliderect(player_rect):
            if player_rect.midtop[1] < solid.midtop[1]:
                grounded = True
                player_y = old_player_y
            if (
                player_rect.midright[0] < solid.midright[0]
                and player_rect.midtop[1] + tiles.TILESIZE * 1.5 > solid.midtop[1]
            ):
                player_x -= WALK_SPEED
            if (
                player_rect.midright[0] > solid.midright[0]
                and player_rect.midtop[1] + tiles.TILESIZE * 1.5 > solid.midtop[1]
            ):
                player_x += WALK_SPEED

    if keys[pygame.K_UP] and grounded:
        jump_remaining = tiles.TILESIZE * 2

    if jump_remaining:
        player_y -= 16
        jump_remaining -= 16

    if direction == 1:
        window.blit(player_right, (window.get_width() / 2, 0))
    elif direction == -1:
        window.blit(player_left, (window.get_width() / 2, 0))
    window.blit(
        font.render(f"FPS: {clock.get_fps()}", False, pygame.Color("white")), (0, 0)
    )
    window.blit(
        font.render(f"Position: {player_x}, {player_y}", False, pygame.Color("white")),
        (0, 10),
    )
    pygame.display.update()
    clock.tick(60)
