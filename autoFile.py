#Makes all files required to add a minecraft item
#It will take the folder where you would like to add a new item
#Then it will ask for the name and the rest will be the same
#It will then add the name into the necessary files

import os
from random import Random, random

#root path
path = 'C:/Users/USER/Documents/makingModLearning/forgeproject1.19.2/src/main'
#item java class path
itemClassPath = 'C:/Users/USER/Documents/makingModLearning/forgeproject1.19.2/src/main/java/net/USER/modlearning/item'


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
    f.write('{\n\t"parent": "item/generated",\n\t"textures": {\n\t\t"layer0": "modlearning:item/' + newItemName + '"\n\t}\n}')
    f.close()


def addJsonEn(newItemName, path):
    f = open(f'{path}en_us.json', 'r')
    lines = f.readlines()
    f.close()
    f = open(f'{path}en_us.json', 'w')
    for i in lines:
        if '}' in i:
            f.write(f',\t"item.modlearning.{newItemName}": "{input(f"In game item name(blank for {newItemName})" or newItemName)}"\n')
        f.write(i)
    f.close()


#Get files in folder
def getFilesInFolder(folder):
    files = []
    for file in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, file)):
            files.append(file)
    return files


#Get folders in folder
def getFoldersInFolder(folder):
    folders = []
    for file in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, file)):
            folders.append(file)
    return folders


a = getFilesInFolder(itemClassPath)
if False:
    for a1 in a:
        if a1 == "ModItems.java":
            a = a1
    print(a)
    jva = open(itemClassPath + '/' + a, 'r')
    newFile = open(itemClassPath + '/' + 'temp.java', 'w')
    l = jva.readlines()

    i2 = 0
    for i in l:
        if 'ModItems' in i:
            print("found it")
            print(i)
            i = 'public class temp {\n'
            
        newFile.write(i)
        i2 += 1

    newFile.close()
    jva.close()

def getInputs(newItemName): #Gets all the inputs for the files such as the type, tier, attack damage, attack speed, etc

    print(f'Adding ---> {newItemName} <--- to the mod')
    itemOrPickOrSwordItem = input("Type of item(Blank for 1)? (item(1), pickaxe(2), SwordItem(3)): ") or "1"

    if itemOrPickOrSwordItem == "Item" or itemOrPickOrSwordItem == "1":
        typeOfItem = "Item"
        tab = "CreativeModeTab.TAB_MISC"

        tab = input("Enter the tab you want to add it to(Black for default): \ne.g:\nItemGroup.TAB_MISC \n") or tab
        newItemName = input(f"Enter the name of the new item(Blank for {newItemName}): ").replace(' ', '_') or newItemName

        return f"""    public static final RegistryObject<Item> {newItemName.upper()} = ITEMS.register("{newItemName}",() -> 
        new {typeOfItem}(new Item.Properties().tab({tab})));"""

    if itemOrPickOrSwordItem == "PickaxeItem" or itemOrPickOrSwordItem == "2":
        typeOfItem = "PickaxeItem"
        tierOfItem = "Tiers.IRON"
        attackDmg = "3"
        attackSpeed = "2"
        tab = "CreativeModeTab.TAB_TOOLS"

        tab = input("Enter the tab you want to add it to(Black for default): \ne.g:\nCreativeModeTab.TAB_TOOLS \n") or tab
        tierOfItem = input("Enter the tier of item(Blank for default): \n e.g:\nTiers.IRON\n") or tierOfItem
        attackDmg = input("Enter the attack damage of item(Blank for default): \ne.g:\n3\n") or attackDmg
        attackSpeed = input("Enter the attack speed of item(Blank for default): \ne.g:\n2\n") or attackSpeed + "F"
        newItemName = input(f"Enter the name of the new item(Blank for {newItemName}): ").replace(' ', '_') or newItemName

        return f"""    public static final RegistryObject<Item> {newItemName.upper()} = ITEMS.register("{newItemName}",\n() -> 
        new {typeOfItem}({tierOfItem}, {attackDmg}, {attackSpeed}, (new Item.Properties()).tab({tab})));"""

    if itemOrPickOrSwordItem == "SwordItem" or itemOrPickOrSwordItem == "3":
        typeOfItem = "SwordItem"
        tierOfItem = "Tiers.IRON"
        attackDmg = "3"
        attackSpeed = "2"
        tab = "CreativeModeTab.TAB_COMBAT"

        tab = input("Enter the tab you want to add it to(Black for default): \ne.g:\nCreativeModeTab.TAB_COMBAT \n") or tab
        tierOfItem = input("Enter the tier of item(Blank for default): \ne.g:\nTiers.IRON\n") or tierOfItem
        attackDmg = input("Enter the attack damage of item(Blank for default): \ne.g:\n3\n") or attackDmg
        attackSpeed = input("Enter the attack speed of item(Blank for default): \ne.g:\n2\n") or attackSpeed + "F"
        newItemName = input(f"Enter the name of the new item(Blank for {newItemName}): ").replace(' ', '_') or newItemName

        return f"""    public static final RegistryObject<Item> {newItemName.upper()} = ITEMS.register("{newItemName}",\n() -> 
        new {typeOfItem}({tierOfItem}, {attackDmg}, {attackSpeed}, (new Item.Properties()).tab({tab})));"""


before = 'IEventBus '
javaClassPath = 'C:/Users/USER/Documents/makingModLearning/forgeproject1.19.2/src/main/java/net/USER/modlearning/item/temp.java'
jsonEnPath = 'C:/Users/USER/Documents/makingModLearning/forgeproject1.19.2/src/main/resources/assets/modlearning/lang/'
jsonModelPath = 'C:/Users/USER/Documents/makingModLearning/forgeproject1.19.2/src/main/resources/assets/modlearning/models/item/'
pngPath = 'C:/Users/USER/Documents/makingModLearning/forgeproject1.19.2/src/main/resources/assets/modlearning/textures/item/'

allPngFiles = getFilesInFolder(pngPath)
allJsonModelsFiles = getFilesInFolder(jsonModelPath)
allJsonEnFiles = getFilesInFolder(jsonEnPath)


for allPngFile in allPngFiles:
    jsonEnFile = ''.join(allJsonModelsFiles)
    pngFile = allPngFile.replace('.png', '')
    if not pngFile in jsonEnFile:
        line = getInputs(pngFile)
        registerItem(line, before, javaClassPath)
        print(f'Added {pngFile} to {javaClassPath}')
        addJsonModel(pngFile, jsonModelPath)
        print(f'Added {pngFile} to {jsonModelPath}')
        addJsonEn(pngFile, jsonEnPath)
        print(f'Added {pngFile} to {jsonEnPath}')
        print(f'Added {pngFile} to the mod')
    else:
        print(f'{allPngFile} already in the mod')



"""
TO DO:
- add a way to save profiles so you can add multiple items at once or at least faster
- add more options for the items so you can customize them further
- add a way to add blocks

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

"""

