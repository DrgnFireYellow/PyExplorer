from yaml import load, Loader
import os

BIOMESFOLDER = os.path.join("data", "biomes")
biomes = {}


for biome in os.listdir(BIOMESFOLDER):
    with open(os.path.join(BIOMESFOLDER, biome)) as biomefile:
        biomedata = load(biomefile, Loader)
        biomes[os.path.splitext(biome)[0]] = biomedata

del biomedata
