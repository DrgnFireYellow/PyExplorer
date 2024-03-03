import os
import pygame
from yaml import load, Loader


TILESFOLDER = os.path.join("data", "tiles")
TEXTUREFOLDER = os.path.join("textures", "tiles")
TILESIZE = 64

tiles = {}
for tile in os.listdir(TILESFOLDER):
    with open(os.path.join(TILESFOLDER, tile)) as tiledatafile:
        tiledata = load(tiledatafile, Loader)
        tiles[tiledata["id"]] = pygame.image.load(
            os.path.join(TEXTUREFOLDER, tiledata["texture"])
        )
        tiles[tiledata["id"]] = pygame.transform.scale(
            tiles[tiledata["id"]], (TILESIZE, TILESIZE)
        )

for mod in os.listdir("mods"):
    if os.path.isdir(os.path.join("mods", mod)):
        moddedtilesfolder = os.path.join("mods", mod, TILESFOLDER)
        moddedtexturefolder = os.path.join("mods", mod, TEXTUREFOLDER)
        for tile in os.listdir(moddedtilesfolder):
            with open(os.path.join(moddedtilesfolder, tile)) as tiledatafile:
                tiledata = load(tiledatafile, Loader)
                tiles[tiledata["id"]] = pygame.image.load(
                    os.path.join(moddedtexturefolder, tiledata["texture"])
                )
                tiles[tiledata["id"]] = pygame.transform.scale(
                    tiles[tiledata["id"]], (TILESIZE, TILESIZE)
                )

tiles[0] = pygame.Surface((TILESIZE, TILESIZE))
tiles[0].fill(pygame.Color("skyblue"))

del tiledata
