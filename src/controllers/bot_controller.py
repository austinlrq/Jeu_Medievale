from src.models import Immigration, Soldat, Seigneur
from src import controllers
# importer TYPE
from src.views.TYPE import TYPE
import random

gc = None

def action_bots(game_controller):
        ["argent","ressources","guerre"]
        """
        il y a 3 categories possibles pour le bot: argent, ressources, guerre
        le bot va choisir une des categorie en fonction de ses besoins
        par exemple, plus il a de l'argent, moins il y a de chances qu'il choisisse cette categorie
        il faut une formule pour attribuer un pourcetage de chance pour chaque categorie d'etre choisie
        si il a besoin d'argent(en dessous de la moyenne des nobles/seigneurs):
                il peut acheter une case montage collé a une case qu'il a déjà
                vendre une partie de ses ressources
        si il a besoin de ressources(en dessous de la moyenne des nobles/seigneurs):
                prelever l'impot
                    si ses villageois ont des ressources
                acheter des cases eau ou montagnes
                si pas d'espace habitat:
                    il peut acheter un habitat
                sinon:
                    acheter des villageois
                il peut acheter des ressources
        si il a de l'argent et des ressources:
                si il n'a pas de camp/pas d'espace:
                    il peut acheter un camp
                sinon:
                    il peut acheter des soldats
                prendre des cases pour faire un chemin vers le noble seigneur qui a l'armee la plus faible
                attaquer un autre seigneur
        """
        global gc
        gc=game_controller
        #choisir une categorie
        liste_bots=creer_liste_bots()
        moyenne_argent, moyenne_ressources = moyennes(liste_bots)
        print(moyenne_argent, moyenne_ressources)
        for bot in liste_bots:
            if bot == gc.joueur:
                continue
            if bot not in gc.seigneurs and bot not in gc.nobles:
                continue
            choix_categorie = choisir_categorie(bot, moyenne_argent, moyenne_ressources)
            print(bot.nom, bot.argent, bot.ressources)
            print(choix_categorie)
            if choix_categorie=="argent":
                action_argent(bot, moyenne_argent)
            elif choix_categorie=="ressources":
                action_ressources(bot)
            elif choix_categorie == "guerre":
                action_guerre(bot, liste_bots)
            print("############################")
    
def creer_liste_bots():
    liste=[]
    for seigneur in gc.seigneurs:
        liste.append(seigneur)
    for noble in gc.nobles:
        if noble.seigneur==None:
            liste.append(noble)
    return liste

def moyennes(liste_bots):
    moyenne_argent=0
    moyenne_ressources=0
    for bot in liste_bots:
        moyenne_argent+=bot.argent
        moyenne_ressources+=bot.ressources
    moyenne_argent/=len(liste_bots)
    moyenne_ressources/=len(liste_bots)
    return moyenne_argent, moyenne_ressources

def choisir_categorie(bot, moyenne_argent, moyenne_ressources):
    if bot.argent == 0 or moyenne_argent == 0:
        return "argent"
    if bot.ressources == 0 or moyenne_ressources == 0:
        return "ressources"
    argent_chance = max(0, 100 - (bot.argent / moyenne_argent * 100))
    ressources_chance = max(0, 100 - (bot.ressources / moyenne_ressources * 100))
    guerre_chance = max(0, ((bot.argent / moyenne_argent + bot.ressources / moyenne_ressources) * 50)-10)
    print(argent_chance)
    print(ressources_chance)
    print(guerre_chance)
    total = argent_chance + ressources_chance + guerre_chance
    choix = random.uniform(0, total)

    if choix <= argent_chance:
        return "argent"
    elif choix <= argent_chance + ressources_chance:
        return "ressources"
    else:
        return "guerre"


def action_argent(bot, moyenne_argent):
    liste_voisin = peut_acheter_case(bot, [TYPE.montagne,TYPE.montagneclair])
    if liste_voisin:
        random.shuffle(liste_voisin)
        voisin = liste_voisin[0]
        voisin.acheter(bot)
        bot.ajouter_case(voisin)
        print("acheter case")
        return
    else:
        #vendre ressources pour revenir a peut pres a la moyenne
        total = int(bot.ressources*0.2)
        bot.diminuer_ressources(int(total))
        bot.augmenter_argent(int(total*0.8))

def peut_acheter_case(bot,liste_cases):
    liste = []
    for case in bot.cases:
        voisins = gc.interface.map.get_voisins(case)
        for voisin in voisins:
            if voisin.proprietaire==None:
                if voisin.type in liste_cases:
                    if voisin.prix<=bot.argent:
                        liste.append(voisin)
    return liste

def voisins_cases(case):
    voisins=[]
    if case.col>0:
        voisins.append(gc.interface.map.grid[case.x-1][case.y])
    if case.col<gc.largeur-1:
        voisins.append(gc.carte[case.x+1][case.y])
    if case.row>0:
        voisins.append(gc.carte[case.x][case.y-1])
    if case.row<gc.hauteur-1:
        voisins.append(gc.carte[case.x][case.y+1])
    return voisins

def action_ressources(bot):
    impot = 25
    acheter_case = 25
    recruter = 25
    acheter = 25
    x = random.randint(0,100)
    action_prise = False
    if x<acheter_case and not action_prise:
        liste_cases = peut_acheter_case(bot, [TYPE.eau,TYPE.eauclair,TYPE.foretclair,TYPE.foret])
        if liste_cases:
            random.shuffle(liste_cases)
            case = liste_cases[0]
            case.acheter(bot)
            bot.ajouter_case(case)
            action_prise = True

    if x<acheter_case+recruter and not action_prise:
        if bot.capacite_habitants<=gc.obtenir_nombre_total_personnes(bot):
            liste_cases = peut_construire_case(bot)
            if liste_cases:
                random.shuffle(liste_cases)
                case = liste_cases[0]
                gc.construire(bot, case, "habitation")
                action_prise = True
        elif bot.argent>=5:
            liste = ["paysan"]
            if bot.argent>=10:
                liste.append("roturier")
            random.shuffle(liste)
            immigration = Immigration(bot)
            immigration.immigrer(liste[0])
            action_prise = True

    if x<acheter_case+recruter+acheter and not action_prise:
        if bot.argent>=2:
            total = int(bot.argent*0.2)
            bot.augmenter_ressources(int(total*1.2))
            bot.diminuer_argent(int(total))
            action_prise = True

    if not action_prise:
        temp=[]
        if isinstance(bot, Seigneur):
            for i in bot.vassaux:
                temp.append(i.village_noble)
        bot.percevoir_impot(temp)
        action_prise = True
    return

def peut_construire_case(bot):
    liste = []
    for case in bot.cases:
        if case.type == TYPE.plaine and case.batiment == None:
            liste.append(case)
    return liste

def action_guerre(bot, liste_bots):
    recruter = 25
    acheter_case = 25
    #guerre = 25
    x = random.randint(0,50)
    action_prise = False

    """if x<guerre and not action_prise:
        liste = []
        for bot_defenseur in liste_bots:
            if bot_defenseur!=bot:
                pass
        random.shuffle(liste)
        for bot_defenseur in liste:
            if gc.interface.map.territoires_adjacents(bot, bot_defenseur):
                gc.guerre(bot, bot_defenseur)
                action_prise = True
                return"""

    if x<recruter and not action_prise:
        if bot.capacite_soldats<=len(bot.armee):
            liste_cases = peut_construire_case(bot)
            if liste_cases:
                random.shuffle(liste_cases)
                case = liste_cases[0]
                gc.construire(bot, case, "camp")
                action_prise = True
        elif bot.argent>=5:
            liste = ["infanterie"]
            if bot.argent>=15:
                liste.append("cavalier")
            random.shuffle(liste)
            bot.recruter(Soldat(liste[0], 10, liste[0]))
            action_prise = True

    if not action_prise:
        #prendre une case pour se rapprocher du noble/seigneur le plus faible
        liste = []
        for bot_defenseur in liste_bots:
            if bot_defenseur==bot:
                continue
            elif liste==[]:
                liste.append(bot_defenseur)
            elif bot_defenseur.seigneur == bot:
                continue
            elif bot.seigneur:
                if len(bot_defenseur.seigneur.armee)<len(liste[0].armee):
                    liste[0]=bot_defenseur.seigneur
            elif len(bot_defenseur.armee)<len(liste[0].armee):
                liste[0]=bot_defenseur
        if liste:
            coord1 = gc.interface.map.grid[bot.village_noble.y][bot.village_noble.x]
            coord2 = gc.interface.map.grid[liste[0].village_noble.y][liste[0].village_noble.x]
            chemin = gc.interface.map.chemin_le_plus_court(coord1, coord2)
            if chemin:
                i=0
                while i<len(chemin):
                    if not chemin[i].proprietaire:
                        chemin[i].acheter(bot)
                        bot.ajouter_case(chemin[i])
                        action_prise = True
                        return
                    elif chemin[i].proprietaire and chemin[i].proprietaire!=bot:
                        #guerre
                        gc.guerre(bot, chemin[i].proprietaire)
                        return
                    i+=1
    return