import random

# Returns tuple of names and random League of Legends roles for each given name (with no chance of getting "Fill")
def lr(names):
    
    roles1 = ["Top", "Jungle", "Middle", "Bottom", "Support"]
    roles2 = ["Top", "Jungle", "Middle", "Bottom", "Support"]
    roles3 = ["Top", "Jungle", "Middle", "Bottom", "Support"]
    players = ""
    roles = ""
    max = 0
    primaries = {}
    secondaries = {}

    for i in names:
        num = random.randint(0, len(roles1) - 1)
        gone = roles1.pop(num)
        primaries[i] = gone
        
    for i in roles3:
        if (i in roles1):
            roles2.append(i)
            roles2.append(i)

    for i in names:
        num = random.randint(0, len(roles2) - 1)
        while (primaries[i] == roles2[num]):
            num = random.randint(0, len(roles2) - 1)
        secondaries[i] = roles2[num]
 
    for i in names:
        players = players + i + "\n"
        roles = roles + primaries[i] + " / " + secondaries[i] + "\n"

    return (players, roles)

# Returns tuple of names and random League of Legends roles for each given name
def lrf(names):
    
    roles1 = ["Top", "Jungle", "Middle", "Bottom", "Support", "Fill"]
    roles2 = ["Top", "Jungle", "Middle", "Bottom", "Support", "Fill"]
    roles3 = ["Top", "Jungle", "Middle", "Bottom", "Support", "Fill"]
    players = ""
    roles = ""
    primaries = {}
    secondaries = {}

    for i in names:
        num = random.randint(0, len(roles1) - 1)
        if (roles1[num] != "Fill"):
            gone = roles1.pop(num)
        else:
            gone = "Fill"
        primaries[i] = gone
        
    for i in roles3:
        if (i in roles1 and i != "Fill"):
            roles2.append(i)
            roles2.append(i)

    for i in names:
        if (primaries[i] != "Fill"):
            num = random.randint(0, len(roles2) - 1)
            while (primaries[i] == roles2[num]):
                num = random.randint(0, len(roles2) - 1)
            secondaries[i] = roles2[num]
 
    for i in names:
        players = players + i + "\n"
        if (i in secondaries.keys()):
            roles = roles + primaries[i] + " / " + secondaries[i] + "\n"
        else:
            roles = roles + primaries[i] + "\n"

    return (players, roles)

# Returns tuple of names and random Valorant roles for each given name
def vr(names):
    
    rolesList = ["Controller", "Duelist", "Initiator", "Sentinel"]
    players = ""
    roles = ""

    for i in names:
        num = random.randint(0, len(rolesList) - 1)
        players = players + i + "\n"
        roles = roles + rolesList[num] + "\n"

    return (players, roles)

# Returns tuple of names and random Valorant roles for each given name, while ensuring there's at most one duplicate role
def vrx(names):
    rolesList = ["Controller", "Duelist", "Initiator", "Sentinel"]
    used = []
    dupe = False
    players = ""
    roles = ""

    for i in names:
        num = random.randint(0, len(rolesList) - 1)
        if (dupe):
            while(rolesList[num] in used):
                num = random.randint(0, len(rolesList) - 1)
            used.append(rolesList[num])
            roleassigned = rolesList[num]
        else:
            if (rolesList[num] in used):
                dupe = True
            else:
                used.append(rolesList[num])
            roleassigned = rolesList[num]

        players = players + i + "\n"
        roles = roles + roleassigned + "\n"

    return (players, roles)

# Returns a random Valorant agent for the given role as a string
def va(role):

    controllers = ["Astra", "Brimstone", "Omen", "Viper"]
    duelists = ["Jett", "Neon", "Phoenix", "Raze", "Reyna", "Yoru"]
    initiators = ["Breach", "Fade", "KAY/O", "Skye", "Sova"]
    sentinels = ["Chamber", "Cypher", "Killjoy", "Sage"]
    controllerpics = ["https://static.wikia.nocookie.net/valorant/images/8/8a/Astra_artwork.png/revision/latest/scale-to-width-down/326?cb=20210302170140",
                    "https://static.wikia.nocookie.net/valorant/images/3/37/Brimstone_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020239",
                    "https://static.wikia.nocookie.net/valorant/images/0/06/Omen_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020233",
                    "https://static.wikia.nocookie.net/valorant/images/9/91/Viper_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020322"]
    duelistpics = ["https://static.wikia.nocookie.net/valorant/images/7/79/Jett_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020209",
                    "https://static.wikia.nocookie.net/valorant/images/a/ad/Neon_artwork.png/revision/latest/scale-to-width-down/326?cb=20220112155550",
                    "https://static.wikia.nocookie.net/valorant/images/f/fa/Phoenix_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020246",
                    "https://static.wikia.nocookie.net/valorant/images/c/c4/Raze_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020217",
                    "https://static.wikia.nocookie.net/valorant/images/4/41/Reyna_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020340",
                    "https://static.wikia.nocookie.net/valorant/images/1/1a/Yoru_artwork.png/revision/latest/scale-to-width-down/326?cb=20210112180407"]
    initiatorpics = ["https://static.wikia.nocookie.net/valorant/images/5/5c/Breach_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020225",
                    "https://static.wikia.nocookie.net/valorant/images/8/8a/Fade_artwork.png/revision/latest/scale-to-width-down/326?cb=20220425005211",
                    "https://static.wikia.nocookie.net/valorant/images/a/a9/KAYO_artwork.png/revision/latest/scale-to-width-down/326?cb=20210622163116",
                    "https://static.wikia.nocookie.net/valorant/images/d/d6/Skye_artwork.png/revision/latest/scale-to-width-down/326?cb=20201013182515",
                    "https://static.wikia.nocookie.net/valorant/images/6/61/Sova_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020314"]
    sentinelpics = ["https://static.wikia.nocookie.net/valorant/images/5/5d/Chamber_artwork.png/revision/latest/scale-to-width-down/326?cb=20211031124636",
                    "https://static.wikia.nocookie.net/valorant/images/b/bb/Cypher_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020329",
                    "https://static.wikia.nocookie.net/valorant/images/6/6b/Killjoy_artwork.png/revision/latest/scale-to-width-down/220?cb=20200729134445",
                    "https://static.wikia.nocookie.net/valorant/images/1/1e/Sage_artwork.png/revision/latest/scale-to-width-down/326?cb=20200602020306"]

    if (role == "any"):
        assignment = random.randint(0, 3)
        if (assignment == 0):
            num = random.randint(0, len(controllers) - 1)
            return (controllers[num], controllerpics[num])
        elif (assignment == 1):
            num = random.randint(0, len(duelists) - 1)
            return (duelists[num], duelistpics[num])
        elif (assignment == 2):
            num = random.randint(0, len(initiators) - 1)
            return (initiators[num], initiatorpics[num])
        else:
            num = random.randint(0, len(sentinels) - 1)
            return (sentinels[num], sentinelpics[num])

    if (role.lower() == "controller"):
        num = random.randint(0, len(controllers) - 1)
        return (controllers[num], controllerpics[num])
    elif (role.lower() == "duelist"):
        num = random.randint(0, len(duelists) - 1)
        return (duelists[num], duelistpics[num])
    elif (role.lower() == "initiator"):
        num = random.randint(0, len(initiators) - 1)
        return (initiators[num], initiatorpics[num])
    elif (role.lower() == "sentinel"):
        num = random.randint(0, len(sentinels) - 1)
        return (sentinels[num], sentinelpics[num])