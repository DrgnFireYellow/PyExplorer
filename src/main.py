import pygame
import tiles
import biomes
import os
import math
import random

pygame.init()
print(f"Loaded {len(tiles.tiles)} tiles")
print(f"Loaded {len(biomes.biomes)} biomes")

screeninfo = pygame.display.Info()
clock = pygame.time.Clock()

font = pygame.font.Font(pygame.font.get_default_font(), 10)
hotbarfont = pygame.font.Font(pygame.font.get_default_font(), int(tiles.TILESIZE / 2))

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

inventory = {}

for tile in tiles.tiles:
    if tile != 0:
        inventory[tile] = 0

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


hotbar_slots = {}
selected_hotbar_slot = 1


def display_hotbar():
    displayx = 0
    for tile in tiles.tiles:
        if tile and inventory[tile] > 0:
            tileicon = tiles.tiles[tile].copy()
            if tile == selected_hotbar_slot:
                pygame.draw.rect(
                    tileicon, "white", (0, 0, tiles.TILESIZE, tiles.TILESIZE), 4
                )
            window.blit(tileicon, (displayx, 0))
            window.blit(
                hotbarfont.render(str(inventory[tile]), False, "white"), (displayx, 0)
            )
            hotbar_slots[tile] = pygame.Rect(
                displayx, 0, tiles.TILESIZE, tiles.TILESIZE
            )
            displayx += tiles.TILESIZE + 8
        else:
            try:
                del hotbar_slots[tile]
            except KeyError:
                pass


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

map.append([6] * 64)

jump_remaining = 0

playing = False
playbutton = pygame.image.load(os.path.join("textures", "ui", "playbutton.png"))
playbuttonrect = pygame.Rect(
    (window.get_width() - playbutton.get_width()) // 2,
    (window.get_height() - playbutton.get_height()) // 2,
    playbutton.get_width(),
    playbutton.get_height(),
)

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
            if playing:
                try:
                    if event.button == 3 and map[mouse_tile[1]][mouse_tile[0]] == 0:
                        if inventory[selected_hotbar_slot] > 0:
                            map[mouse_tile[1]][mouse_tile[0]] = selected_hotbar_slot
                            inventory[selected_hotbar_slot] -= 1
                    elif event.button == 1:
                        hotbar_clicked = False
                        for slot in hotbar_slots:
                            if hotbar_slots[slot].collidepoint(mouse_location):
                                hotbar_clicked = True
                                selected_hotbar_slot = slot
                        if (
                            not hotbar_clicked
                            and map[mouse_tile[1]][mouse_tile[0]] != 6
                        ):
                            inventory[map[mouse_tile[1]][mouse_tile[0]]] += 1
                            map[mouse_tile[1]][mouse_tile[0]] = 0
                except (IndexError, KeyError):
                    pass
            else:
                if event.button == 1:
                    if playbuttonrect.collidepoint(mouse_location):
                        playing = True
    if playing:
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
        display_hotbar()
        window.blit(
            font.render(f"FPS: {clock.get_fps()}", False, pygame.Color("white")), (0, 0)
        )
        window.blit(
            font.render(
                f"Position: {player_x}, {player_y}", False, pygame.Color("white")
            ),
            (0, 10),
        )
    else:
        window.fill("chartreuse3")
        window.blit(
            playbutton,
            (
                (window.get_width() - playbutton.get_width()) // 2,
                (window.get_height() - playbutton.get_height()) // 2,
            ),
        )
    pygame.display.update()
    clock.tick(60)
