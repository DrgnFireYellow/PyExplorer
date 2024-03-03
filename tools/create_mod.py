import os

mod_name = input("Enter the name of your mod: ")

os.mkdir(mod_name)
os.mkdir(os.path.join(mod_name, "data"))
os.mkdir(os.path.join(mod_name, "textures"))
os.mkdir(os.path.join(mod_name, "data", "tiles"))
os.mkdir(os.path.join(mod_name, "data", "biomes"))
os.mkdir(os.path.join(mod_name, "textures", "tiles"))
print("Mod created. You can add tiles and biomes using YAML files")
