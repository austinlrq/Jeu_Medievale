from src.models import Immigration, Soldat, Seigneur
from src.views.TYPE import TYPE
import random

# Référence globale pour le GameController
gc = None

def action_bots(game_controller):
    """
    Fonction principale pour exécuter les actions des bots à chaque tour.

    - Chaque bot choisit une catégorie (argent, ressources, guerre) en fonction de ses besoins.
    - Les actions spécifiques sont exécutées selon la catégorie choisie et les besoins du bot.

    :param game_controller: Instance du contrôleur principal du jeu.
    """
    global gc
    gc = game_controller

    # Création de la liste des bots (nobles et seigneurs sans suzerain)
    liste_bots = creer_liste_bots()
    
    # Calcul des moyennes d'argent et de ressources des bots
    moyenne_argent, moyenne_ressources = moyennes(liste_bots)

    for bot in liste_bots:
        if bot == gc.joueur:  # Ignorer le joueur principal
            continue
        if bot not in gc.seigneurs and bot not in gc.nobles:  # Vérifier que le bot est valide
            continue

        # Déterminer la catégorie à privilégier
        choix_categorie = choisir_categorie(bot, moyenne_argent, moyenne_ressources)

        # Exécuter l'action selon la catégorie choisie
        if choix_categorie == "argent":
            action_argent(bot)
        elif choix_categorie == "ressources":
            action_ressources(bot)
        elif choix_categorie == "guerre":
            action_guerre(bot, liste_bots)
    
def creer_liste_bots():
    """
    Crée une liste de tous les seigneurs et nobles libres.

    :return: Liste des bots valides.
    """
    liste = []
    for seigneur in gc.seigneurs:
        liste.append(seigneur)
    for noble in gc.nobles:
        if noble.seigneur is None:
            liste.append(noble)
    return liste

def moyennes(liste_bots):
    """
    Calcule les moyennes d'argent et de ressources des bots.

    :param liste_bots: Liste des bots.
    :return: Tuple contenant la moyenne d'argent et la moyenne de ressources.
    """
    moyenne_argent = sum(bot.argent for bot in liste_bots) / len(liste_bots)
    moyenne_ressources = sum(bot.ressources for bot in liste_bots) / len(liste_bots)
    return moyenne_argent, moyenne_ressources

def choisir_categorie(bot, moyenne_argent, moyenne_ressources):
    """
    Détermine la catégorie d'action à privilégier pour un bot.

    :param bot: Instance du bot.
    :param moyenne_argent: Moyenne d'argent des bots.
    :param moyenne_ressources: Moyenne de ressources des bots.
    :return: Catégorie choisie ("argent", "ressources", "guerre").
    """
    if bot.argent == 0 or moyenne_argent == 0:
        return "argent"
    if bot.ressources == 0 or moyenne_ressources == 0:
        return "ressources"

    # Probabilités pour chaque catégorie
    argent_chance = max(0, 100 - (bot.argent / moyenne_argent * 100))
    ressources_chance = max(0, 100 - (bot.ressources / moyenne_ressources * 100))
    guerre_chance = max(0, ((bot.argent / moyenne_argent + bot.ressources / moyenne_ressources) * 50) - 10)

    total = argent_chance + ressources_chance + guerre_chance
    choix = random.uniform(0, total)

    # Retourner la catégorie correspondant au choix
    if choix <= argent_chance:
        return "argent"
    elif choix <= argent_chance + ressources_chance:
        return "ressources"
    else:
        return "guerre"


def action_argent(bot):
    """
    Actions liées à l'argent pour un bot.

    :param bot: Instance du bot.
    """
    # Tenter d'acheter une case de type montagne
    liste_voisin = peut_acheter_case(bot, [TYPE.montagne, TYPE.montagneclair])
    if liste_voisin:
        random.shuffle(liste_voisin)
        voisin = liste_voisin[0]
        voisin.acheter(bot)
        bot.ajouter_case(voisin)
    else:
        # Vendre une partie des ressources pour augmenter l'argent
        total = int(bot.ressources * 0.2)
        bot.diminuer_ressources(total)
        bot.augmenter_argent(int(total * 0.8))
    return

def peut_acheter_case(bot, liste_cases):
    """
    Retourne une liste de cases pouvant être achetées par un bot.

    :param bot: Instance du bot.
    :param liste_cases: Types de cases recherchées.
    :return: Liste de cases achetables.
    """
    liste = []
    for case in bot.cases:
        voisins = gc.interface.map.get_voisins(case)
        for voisin in voisins:
            if voisin.proprietaire is None and voisin.type in liste_cases and voisin.prix <= bot.argent:
                liste.append(voisin)
    return liste

def action_ressources(bot):
    """
    Actions liées aux ressources pour un bot.

    :param bot: Instance du bot.
    """
    # Probabilités d'actions
    acheter_case = 25
    recruter = 25
    acheter = 25
    x = random.randint(0, 100)
    action_prise = False

    if x < acheter_case and not action_prise:
        # Acheter des cases d'eau ou forêt
        liste_cases = peut_acheter_case(bot, [TYPE.eau, TYPE.eauclair, TYPE.foretclair, TYPE.foret])
        if liste_cases:
            random.shuffle(liste_cases)
            case = liste_cases[0]
            case.acheter(bot)
            bot.ajouter_case(case)
            action_prise = True

    if x < acheter_case + recruter and not action_prise:
        # Construire des habitats ou recruter des villageois
        if bot.capacite_habitants <= gc.obtenir_nombre_total_personnes(bot):
            liste_cases = peut_construire_case(bot)
            if liste_cases:
                random.shuffle(liste_cases)
                case = liste_cases[0]
                gc.construire(bot, case, "habitation")
                action_prise = True
        elif bot.argent >= 5:
            liste = ["paysan"]
            if bot.argent >= 10:
                liste.append("roturier")
            random.shuffle(liste)
            immigration = Immigration(bot)
            immigration.immigrer(liste[0])
            action_prise = True

    if x < acheter_case + recruter + acheter and not action_prise:
        # Acheter des ressources
        if bot.argent >= 2:
            total = int(bot.argent * 0.2)
            bot.augmenter_ressources(int(total * 1.2))
            bot.diminuer_argent(total)
            action_prise = True

    if not action_prise:
        # Percevoir l'impôt
        temp = []
        if isinstance(bot, Seigneur):
            for i in bot.vassaux:
                temp.append(i.village_noble)
        bot.percevoir_impot(temp)

def peut_construire_case(bot):
    """
    Retourne une liste de cases où un bot peut construire un bâtiment.

    :param bot: Instance du bot.
    :return: Liste de cases constructibles.
    """
    liste = []
    for case in bot.cases:
        if case.type == TYPE.plaine and case.batiment is None:
            liste.append(case)
    return liste

def action_guerre(bot, liste_bots):
    """
    Actions liées à la guerre pour un bot.

    :param bot: Instance du bot.
    :param liste_bots: Liste de tous les bots.
    """
    recruter = 25
    x = random.randint(0, 50)
    action_prise = False

    if x < recruter and not action_prise or len(bot.armee) < 2:
        # Construire un camp ou recruter des soldats
        if bot.capacite_soldats <= len(bot.armee):
            liste_cases = peut_construire_case(bot)
            if liste_cases:
                random.shuffle(liste_cases)
                case = liste_cases[0]
                gc.construire(bot, case, "camp")
                action_prise = True
        elif bot.argent >= 5:
            liste = ["infanterie"]
            if bot.argent >= 15:
                liste.append("cavalier")
            random.shuffle(liste)
            bot.recruter(Soldat(liste[0], 10, liste[0]))
            action_prise = True

    if not action_prise:
        # Prendre une case pour se rapprocher d'un ennemi
        liste = []
        for bot_defenseur in liste_bots:
            if bot_defenseur == bot:
                continue
            elif not liste:
                liste.append(bot_defenseur)
            elif bot_defenseur.seigneur == bot:
                continue
            elif bot.seigneur and len(bot_defenseur.seigneur.armee) < len(liste[0].armee):
                liste[0] = bot_defenseur.seigneur
            elif len(bot_defenseur.armee) < len(liste[0].armee):
                liste[0] = bot_defenseur

        if liste:
            coord1 = gc.interface.map.grid[bot.village_noble.y][bot.village_noble.x]
            coord2 = gc.interface.map.grid[liste[0].village_noble.y][liste[0].village_noble.x]
            chemin = gc.interface.map.chemin_le_plus_court(coord1, coord2)
            if chemin:
                i = 0
                while i < len(chemin):
                    if not chemin[i].proprietaire:
                        # Acheter la case si elle n'a pas de propriétaire
                        chemin[i].acheter(bot)
                        bot.ajouter_case(chemin[i])
                        return
                    elif chemin[i].proprietaire and chemin[i].proprietaire != bot:
                        # Déclencher une guerre si la case appartient à un autre bot
                        gc.guerre(bot, chemin[i].proprietaire)
                        return
                    i += 1
