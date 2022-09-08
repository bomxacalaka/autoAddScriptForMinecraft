#Makes all files required to add a minecraft item
#It will take the folder where you would like to add a new item
#Then it will ask for the name and the rest will be the same
#It will then add the name into the necessary files

import os
from random import Random, random



file = "profile1.0.txt" # local file to save/load paths and preferences


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


# returns profile dict if it exists or creates it from user input
def setup():
    try:
        a = openProf()
        print("Profile loaded\n")
    except:
        print("No profile found, creating new one\n")
        a={}
        a["before"] = input("The word you wish your item be added before the line the word is located? (e.g: ) ")
        a["javaClassPath"] = input("What is the path to your java class? ")
        a["jsonEnPath"] = input("What is the path to your en_us.json? ")
        a["jsonModelPath"] = input("What is the path to your json model? ")
        a["pngPath"] = input("What is the path to your textures? ")
        print("Profile created and saved\n")
        changeProf(a)


def getInputs(newItemName): #Gets all the inputs for the files such as the type, tier, attack damage, attack speed, etc

    questions = {"type": "What is the type of the item? (sword, pickaxe, etc) ",
     "tier": "What is the tier of the item? (wood, stone, etc) ",
    "attackDamage": "What is the attack damage of the item? ",
    "attackSpeed": "What is the attack speed of the item? ",
     "durability": "What is the durability of the item? ",
      "miningSpeed": "What is the mining speed of the item? ",
       "enchantability": "What is the enchantability of the item? ",
        "rarity": "What is the rarity of the item? (common, uncommon, etc) ",
         "repairMaterial": "What is the repair material of the item? (ingotIron, etc) ",
          "isFood": "Is the item food? (y/n) ",
           "foodPoints": "How many food points does the item give? ",
            "saturation": "How much saturation does the item give? ",
             "effect": "Does the item give an effect? (y/n) ",
              "effectName": "What is the effect name? (speed, etc) ",
               "effectDuration": "How long does the effect last? ",
                "effectAmplifier": "What is the effect amplifier? ",
                 "effectProbability": "What is the effect probability? ",
                  "effectIsAmbient": "Is the effect ambient? (y/n) ",
                   "effectShowParticles": "Does the effect show particles? (y/n) ",
                   "effectShowIcon": "Does the effect show icon? (y/n) ",
                    "effectIsInstant": "Is the effect instant? (y/n) ",
                     "effectIsPotion": "Is the effect a potion? (y/n) ",
                      "effectIsBeneficial": "Is the effect beneficial? (y/n) ",
                       "effectIsCurativeItem": "Is the effect a curative item? (y/n) ",
                        "effectIsBeneficial": "Is the effect beneficial? (y/n) ",
                         "effectIsCurativeItem": "Is the effect a curative item? (y/n) ",
                          "effectIsBeneficial": "Is the effect beneficial? (y/n) ",
                           "effectIsCurativeItem": "Is the effect a curative item? (y/n) ",
                            "effectIsBeneficial": "Is the effect beneficial? (y/n) ",
                             "effectIsCurativeItem": "Is the effect a curative item? (y/n) ",
                              "effectIsBeneficial": "Is the"}

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


def addBlock():  # ADDED BY COPILOT, STILL NEEDS WORK AND TESTING
    newItemName = "new_block"
    typeOfItem = "Block"
    tab = "CreativeModeTab.TAB_BUILDING_BLOCKS"

    tab = input("Enter the tab you want to add it to(Black for default): \ne.g:\nCreativeModeTab.TAB_BUILDING_BLOCKS \n") or tab
    newItemName = input(f"Enter the name of the new item(Blank for {newItemName}): ").replace(' ', '_') or newItemName

    return f"""    public static final RegistryObject<Block> {newItemName.upper()} = BLOCKS.register("{newItemName}",\n() -> 
        new {typeOfItem}(Block.Properties.of(Material.STONE).strength(5.0F, 6.0F)));"""


def getJavaLineForItem(item):
    """    public static final RegistryObject<Item> ZIRCON  = ITEMS.register("zircon",
            () -> new Item(new Item.Properties().tab(ModCreativeModeTab.TUTORIAL_TAB)));"""

    """    public static final RegistryObject<Item> DAGGER = ITEMS.register("dagger",
            () -> new SwordItem(ModTiers.ZIRCON, 10, 5F, (new Item.Properties()).
                    tab(ModCreativeModeTab.TUTORIAL_TAB).fireResistant().
                    food(new FoodProperties.Builder().nutrition(3).alwaysEat().saturationMod(8f).build())));"""

    """    public static final RegistryObject<Item> GOLDEN_PICKAXE_20K = ITEMS.register("20kgoldpick",
            () -> new PickaxeItem(Tiers.GOLD, 1, -2.8F, (new Item.Properties()).tab(ModCreativeModeTab.TUTORIAL_TAB)));"""

    """{ITEM NAME}_{ITEM TYPE}_{LEVEL}_{USES}_{SPEED}_{ATTACK DAMAGE BONUS}_
        {ENCHANTMENT VALUE}_{TAG}_{REPAIR INGREDIENT}_{ATTACK DAMAGE}_{SPEED}_
        {PROPERTIES}"""


    properties = []
    if item["properties"]:
        for prop in item["properties"]:
            properties.append(f'.{prop}')

    return f"""    public static final ForgeTier {item["item name"].upper()} = new ForgeTier({item["level"]}, {item["uses"]}, {item["speed"]}f,
        {item["attack damage bonus"]}f, {item["enchantment value"]}, BlockTags.{item["tag"]},
        () -> Ingredient.of(ZIRCON.get()));

        public static final RegistryObject<Item> {item["item name"].upper()}  = {item["item type"]}.register("{item["item name"].lower()}",
        () -> new {item["item name"].upper()}(new Item.Properties(){properties}));"""

    


before = 'register'
javaClassPath = 'C:/Users/jorge/Documents/makingModLearning/forgeproject1.19.2/src/main/java/net/jorge/modlearning/item/temp.java'
jsonEnPath = 'C:/Users/jorge/Documents/makingModLearning/forgeproject1.19.2/src/main/resources/assets/modlearning/lang/'
jsonModelPath = 'C:/Users/jorge/Documents/makingModLearning/forgeproject1.19.2/src/main/resources/assets/modlearning/models/item/'
pngPath = 'C:/Users/jorge/Documents/makingModLearning/forgeproject1.19.2/src/main/resources/assets/modlearning/textures/item/'

allPngFiles = getFilesInFolder(pngPath)
allJsonModelsFiles = getFilesInFolder(jsonModelPath)
allJsonEnFiles = getFilesInFolder(jsonEnPath)


def addNewItem():
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


if __name__ == "__main__":
    setup()

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

