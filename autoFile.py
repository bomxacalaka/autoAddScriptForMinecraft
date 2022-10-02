#Makes all files required to add a minecraft item
#It will take the folder where you would like to add a new item
#Then it will ask for the name and the rest will be the same
#It will then add the name into the necessary files

from csv import excel_tab
from logging import exception
import os
from random import Random, random
import shutil
import generateVariation

current_folder = os.path.dirname(os.path.abspath(__file__))

modName = input("Name of the file of the mod: ")

#check if file already exists
try:
    file = modName + ".txt"
    open(current_folder + file, 'r')

except FileNotFoundError:
    open(current_folder + file, 'a').close() # local file to save/load paths and preferences


# save profile(as a dict) to file
def saveProf(content):
    open(file, 'a').close()
    with open(file, 'w') as f: # save changes
        for i in content:
            f.write(i + '=' + content[i] + '\n')


# return content of file as dict
def openProf(): 
    a = {}
    l = []
    with open(file, 'r') as f: 
        l = f.read().splitlines()
        for i in l:
            a[i.split('=')[0]] = i.split('=')[1]
    return a

#modify file content
def changeProf(key, value):
    a = openProf()
    a[key] = value
    saveProf(a)


def changeProfDict(content):
    a = openProf()
    for i in content:
        a[i] = content[i]
    saveProf(a)

def dictToString(dict):
    return '+'.join([dict[i] for i in dict])
    

def registerItem(line, before, file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    f = open(file, 'w')
    for i in lines:
        if before in i:
            f.write('\n' + line + '\n\n')
        f.write(i)
    f.close()


def addJsonModel(newItemName, path):
    f = open(f'{path}{newItemName}.json', 'w')
    f.write('{\n\t"parent": "item/generated",\n\t"textures": {\n\t\t"layer0": "' + modName + ':item/' + newItemName + '"\n\t}\n}')
    f.close()


def addJsonEn(newItemName, path, inGameName):
    f = open(f'{path}en_us.json', 'r')
    lines = f.readlines()
    f.close()
    f = open(f'{path}en_us.json', 'w')
    for i in lines:
        if '}' in i:
            f.write(f',\t"item.{modName}.{newItemName}": "{inGameName}"\n')
        f.write(i)
    f.close()


def addPng(pngFileName):
    shutil.copyfile(pngSource + pngFileName + ".png", pngPath + item["name"].lower().replace(" ","_") + ".png")
    os.remove(pngSource + pngFileName + ".png")

#Get items in folder
def getItemsInFolder(folder):
    files = []
    for file in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file)):
            if ".png" in file and "+" in file:
                files.append(file)
    return files

#Get files in folder
def getPngsInFolder(folder):
    files = []
    for file in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file)):
            if ".png" in file:
                files.append(file)
    return files

#Get folders in folder
def getFoldersInFolder(folder):
    folders = []
    for file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file)):
            folders.append(file)
    return folders

# returns profile dict if it exists or creates it from user input
def main():
    try:
        a = openProf()
        if not a["before"]:
            raise Exception('No "before" found on dictionary')
        print("Profile loaded\n")
    except:
        print("No profile found, creating new one\n")
        a={}

        a["before"] = input("The word you wish your item be added before the line of the word is located? (e.g:IEventBus ) ")
        a["itemJavaClassPath"] = input("What is the path to your item java class? ")
        a["blockJavaClassPath"] = input("What is the path to your block java class? ")
        a["jsonEnPath"] = input("What is the path to your en_us.json? ")
        a["jsonModelPath"] = input("What is the path to your json model? ")
        a["pngPath"] = input("What is the path to your textures? ")
        a["pngSource"] = input("What is the path to your source png? ")
        print("Profile created and saved\n")

        changeProfDict(a)

    loadProfilePaths()

    # makes an item for each png in the source folder
    times = input("How many variations do you want to make? (e.g: 3) ") or "3"
    for i in getPngsInFolder(pngSource):
        if not "+" in i:
            for i2 in range(int(times)):
                generateVariation.makeRandomImage(pngSource + i)

    loadProfilePaths()

    interactiveOrFile = input("Get item attributes from file or interactive? (f/i) ") or "f"

    if interactiveOrFile == 'i':
        makeFiles()

    if interactiveOrFile == 'f':
        makePropertiesForItemsFromFiles()


def loadProfilePaths():
    global before, itemJavaClassPath, blockJavaClassPath, jsonEnPath, jsonModelPath, pngPath, allPngFiles, allJsonModelsFiles, allJsonEnFiles, pngOut, pngSource
    a = openProf()
    before = a["before"]
    itemJavaClassPath = a["itemJavaClassPath"]
    blockJavaClassPath = a["blockJavaClassPath"]
    jsonEnPath = a["jsonEnPath"]
    jsonModelPath = a["jsonModelPath"]
    pngPath = a["pngPath"]
    pngSource = a["pngSource"]
    
    pngOut = getItemsInFolder(pngPath)
    allJsonModelsFiles = getItemsInFolder(jsonModelPath)
    allJsonEnFiles = getItemsInFolder(jsonEnPath)
    allPngFiles = getItemsInFolder(pngSource)


def pngFileNameToDict(name):
    global item
    item = {}
    pngFile = name.replace(".png", "").split("+")
    if len(pngFile) < 2:
        for i in range(12):
            pngFile.append("")

    if pngFile[0] == "Item":
        item["type"] = pngFile[0] or "Item"
        item["name"] = pngFile[1] or "name"
        item["register"] = pngFile[2] or "ITEMS"
        item["properties"] = pngFile[3] or "tab(CreativeModeTab.TAB_MISC)'stacksTo(64)"

    elif pngFile[0] == "SwordItem" or pngFile[0] == "PickaxeItem":
        item["type"] = pngFile[0] or "swordItem"
        item["name"] = pngFile[1] or "sword name"
        item["register"] = pngFile[2] or "ITEMS"
        item["level"] = pngFile[3] or "0"
        item["uses"] = pngFile[4] or "0"
        item["attack"] = pngFile[5] or "0"
        item["speed"] = pngFile[6] or "0"
        item["attack damage bonus"] = pngFile[7] or "0"
        item["attack speed bonus"] = pngFile[8] or "0"
        item["enchantment value"] = pngFile[9] or "0"
        item["tag"] = pngFile[10] or "NEEDS_IRON_TOOL"
        item["repair ingredient"] = pngFile[11] or "Items.STICK"
        item["properties"] = pngFile[12] or "tab(CreativeModeTab.TAB_COMBAT)"
        # PickaxeItem+pickaxename+ITEMS+0+0+0+0+0+0+0+NEEDS_IRON_TOOL+Items.STICK+tab(CreativeModeTab.TAB_TOOLS)'stacksTo(64)
            
    elif pngFile[0] == "Block":
        item["type"] = pngFile[0] or "Block"
        item["name"] = pngFile[1] or "block name"
        item["register"] = pngFile[2] or "registerBlock"
        item["material"] = pngFile[3] or "Material.STONE"
        item["properties"] = pngFile[4] or "strength(1f).requiresCorrectToolForDrops().sound(SoundType.STONE)"
        item["block tab"] = pngFile[5] or "CreativeModeTab.TAB_BUILDING_BLOCKS"


def dictToItemProperties(item):

    if item["type"] == "Item":
        return f"""public static final RegistryObject<Item> {item["name"].upper().replace(" ","_")} = {item["register"]}.register("{item["name"].lower().replace(" ","_")}", 
        () -> new {item["type"].replace(" ","_")}(new Item.Properties().{item["properties"]}));"""

    elif item["type"] == "SwordItem" or item["type"] == "PickaxeItem":
        return f"""    public static final ForgeTier {item["name"].upper().replace(" ","_")}_TIER = new ForgeTier({item["level"]}, {item["uses"]}, {item["speed"]}f,
            {item["attack damage bonus"]}f, {item["enchantment value"]}, BlockTags.{item["tag"]},
            () -> Ingredient.of({item["repair ingredient"]}));

            public static final RegistryObject<Item> {item["name"].upper().replace(" ","_")}  = {item["register"]}.register("{item["name"].lower().replace(" ","_")}",
            () -> new {item["type"]}({item["name"].upper().replace(" ","_")}_TIER, {item["attack"]}, {item["speed"]}f, 
            (new Item.Properties().{item["properties"]})));"""
            
    elif item["type"] == "Block":
        return f"""public static final RegistryObject<Block> {item["name"].upper().replace(" ","_")} = {item["register"]}("{item["name"].lower().replace(" ","_")}",
            () -> new {item["type"]}(BlockBehaviour.Properties.of({item["material"]}).
            {item["properties"]}), {item["block tab"]});"""


def dictToPngFileName(dict):
    return '+'.join([dict[i] for i in dict]) + ".png"


def getJavaLineForItemFromItem(pngItem):
    pngFile = pngItem.replace(".png", "").split("+")
    for i in range(12):
        pngFile.append("")
    item={}
    if pngFile[0] == "Item":
        item["type"] = pngFile[0] or "Item"
        item["name"] = pngFile[1] or "name"
        item["register"] = pngFile[2] or "ITEMS"
        item["properties"] = pngFile[3] or "tab(CreativeModeTab.TAB_MISC)'stacksTo(64)"
        return f"""public static final RegistryObject<Item> {item["name"].upper().replace(" ","_")} = {item["register"]}.register("{item["name"]}", 
        () -> new {item["type"].replace(" ","_")}(new Item.Properties().{item["properties"]}));"""

    elif pngFile[0] == "SwordItem" or pngFile[0] == "PickaxeItem":
        item["type"] = pngFile[0] or "swordItem"
        item["name"] = pngFile[1] or "sword name"
        item["register"] = pngFile[2] or "ITEMS"
        item["level"] = pngFile[3] or "0"
        item["uses"] = pngFile[4] or "0"
        item["attack"] = pngFile[5] or "0"
        item["speed"] = pngFile[6] or "0"
        item["attack damage bonus"] = pngFile[7] or "0"
        item["attack speed bonus"] = pngFile[8] or "0"
        item["enchantment value"] = pngFile[9] or "0"
        item["tag"] = pngFile[10] or "NEEDS_IRON_TOOL"
        item["repair ingredient"] = pngFile[11] or "Items.STICK"
        item["properties"] = pngFile[12] or "tab(CreativeModeTab.TAB_COMBAT)'stacksTo(64)"

        return f"""    public static final ForgeTier {item["name"].upper().replace(" ","_")}_TIER = new ForgeTier({item["level"]}, {item["uses"]}, {item["speed"]}f,
            {item["attack damage bonus"]}f, {item["enchantment value"]}, BlockTags.{item["tag"]},
            () -> Ingredient.of({item["repair ingredient"]}));

            public static final RegistryObject<Item> {item["name"].upper().replace(" ","_")}  = {item["register"]}.register("{item["name"].lower().replace(" ","_")}",
            () -> new {item["type"]}({item["name"].upper().replace(" ","_")}_TIER, {item["attack"]}, {item["speed"]}f, 
            (new Item.Properties().{item["properties"]})));"""
            
    elif pngFile[0] == "Block":
        item["type"] = pngFile[0] or "Block"
        item["name"] = pngFile[1] or "block name"
        item["register"] = pngFile[2] or "registerBlock"
        item["material"] = pngFile[3] or "Material.STONE"
        item["properties"] = pngFile[4] or "strength(1f).requiresCorrectToolForDrops().sound(SoundType.STONE)"
        item["block tab"] = pngFile[5] or "CreativeModeTab.TAB_BUILDING_BLOCKS"


        return f"""public static final RegistryObject<Block> {item["name"].upper().replace(" ","_")} = {item["register"]}("{item["name"].lower().replace(" ","_")}",
            () -> new {item["type"]}(BlockBehaviour.Properties.of({item["material"]}).
            {item["properties"]}), {item["block tab"]});"""


def dictItemPropertiesFromInput(item = {}):

    item["type"] = input("Blank for default\nType of item(e.g: Item, SwordItem, PickaxeItem, Block): ") or "Item"

    print("-----Item Attributes Making-----")

    if item["type"] == "Item":
        item["name"] = input("Name of item(In game name): ") or "item name"
        item["register"] = input("Register of item(e.g ITEM): ") or "ITEMS"
        item["properties"] = input("Properties of item(e.g: tab(CreativeModeTab.TAB_MISC).stacksTo(64)): ") or "tab(CreativeModeTab.TAB_MISC).stacksTo(64)"
        # changeProfDict({attributeName : dictToString(item)})
        return item
    
    elif item["type"] == "SwordItem" or item["type"] == "PickaxeItem":
        item["name"] = input("Name of item(In game name): ") or "item name"
        item["register"] = input("Register of item(e.g ITEM): ") or "ITEMS"
        item["level"] = input("Level of item(e.g: 1): ") or "1"
        item["uses"] = input("Uses of item(e.g: 1): ") or "1"
        item["attack"] = input("Attack of item(e.g: 1): ") or "1"
        item["speed"] = input("Speed of item(e.g: 1): ") or "1"
        item["attack damage bonus"] = input("Attack damage bonus of item(e.g: 1): ") or "1"
        item["attack speed bonus"] = input("Attack speed bonus of item(e.g: 1): ") or "1"
        item["enchantment value"] = input("Enchantment value of item(e.g: 1): ") or "1"
        item["tag"] = input("Tag of item(e.g: NEEDS_IRON_TOOL): ") or "NEEDS_IRON_TOOL"
        item["repair ingredient"] = input("Repair ingredient of item(e.g: Items.DIAMOND): ") or "Items.DIAMOND"
        item["properties"] = input("Properties of item(e.g: tab(CreativeModeTab.TAB_MISC).stacksTo(64)): ") or "tab(CreativeModeTab.TAB_MISC).stacksTo(64)"
        # changeProfDict({attributeName : dictToString(item)})
        return item

    elif item["type"] == "Block":
        item["name"] = input("Name of item(In game name): ") or "item name"
        item["register"] = input("Register of item(e.g registerBlock): ") or "registerBlock"
        item["material"] = input("Material of item(e.g: Material.STONE): ") or "Material.STONE"
        item["properties"] = input("Properties of item(e.g: strength(1f).requiresCorrectToolForDrops().sound(SoundType.STONE)): ") or "strength(1f).requiresCorrectToolForDrops().sound(SoundType.STONE)"
        item["block tab"] = input("Block tab of item(e.g: CreativeModeTab.TAB_MISC): ") or "CreativeModeTab.TAB_MISC"
        # changeProfDict({attributeName : dictToString(item)})
        return item


def makePropertiesForItemsFromFiles():
    for allPngFile in allPngFiles:
            jsonEnFile = ''.join(allJsonModelsFiles)
            pngFile = allPngFile.replace('.png', '')
            pngFileNameToDict(pngFile)
            inGameName = item["name"]
            gameName = item["name"].lower().replace(" ","_")
            if not pngFile in jsonEnFile:
                line = dictToItemProperties(item)
                registerItem(line, before, itemJavaClassPath)
                addJsonModel(gameName, jsonModelPath)
                addJsonEn(gameName, jsonEnPath, inGameName)
                addPng(pngFile)
                print(f'Added {inGameName} to the mod')
            else:
                print(f'{allPngFile} already in the mod')
    if not allPngFiles:
        print("No files found")


def makeFiles():
    item = dictItemPropertiesFromInput()
    name = item["name"].replace(' ', '_')
    inGameName = item["name"]
    for i in item:
        print(i)
    line = dictToItemProperties(item)
    registerItem(line, before, itemJavaClassPath)
    print(f'Java line added to {itemJavaClassPath}')
    addJsonModel(name, jsonModelPath)
    print(f'JsonModel file added to {jsonModelPath}')
    inGameName = input(f"In game item name(blank for {item['name']}): ") or item["name"]
    addJsonEn(name, jsonEnPath, inGameName)
    print(f'JsonEN line added to {jsonEnPath}')
    print(f'Added {item["name"]} to the mod')


if __name__ == "__main__":
    main()


"""
TO DO:
- add a way to save profiles so you can add multiple items at once or at least faster **DONE**
- add more options for the items so you can customize them further **DONE**
- add a way to add blocks **ADDED BUT NOT TESTED**

VERY FAR AWAY TO DO LIST:
add the ability to add armor
add the ability to add food
add the ability to add entities
add the ability to add biomes
add the ability to add dimensions
add the ability to add structures
add the ability to add recipes
add the ability to add advancements
add the ability to add loot tables
add the ability to add sounds
add the ability to add particles
add the ability to add enchantments
add the ability to add potions
add the ability to add villager trades
add the ability to add custom world generation

ADDED BY BOREDOM:
random texture generator
"""

