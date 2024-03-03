from yaml import load, Loader
import os

BIOMESFOLDER = os.path.join("data", "biomes")
biomes = {}


for biome in os.listdir(BIOMESFOLDER):
    with open(os.path.join(BIOMESFOLDER, biome)) as biomefile:
        biomedata = load(biomefile, Loader)
        biomes[os.path.splitext(biome)[0]] = biomedata

for mod in os.listdir("mods"):
    if os.path.isdir(os.path.join("mods", mod)):
        moddedbiomesfolder = os.path.join("mods", mod, BIOMESFOLDER)
        for biome in os.listdir(moddedbiomesfolder):
            with open(os.path.join(moddedbiomesfolder, biome)) as biomefile:
                biomedata = load(biomefile, Loader)
                biomes[os.path.splitext(biome)[0]] = biomedata
del biomedata
