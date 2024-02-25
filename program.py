from folium import*

def fichierVersTableau(nomFichier):
    """
    Construit un tableau à partir du fichier des proriétés
    Le chemin du fichier est passé en paramètre
    """
    fichier = open(nomFichier,"r",encoding="ISO-8859-1")                        # ouvre le fichier
    entete = fichier.readline().split(";")                                      # sépare les valeurs de la première ligne en fonction des points-virgules
    valeursLigne = []                                                           # variable qui contiendra les tuples colonne:valeur de chaque ligne
    for ligne in fichier:                                                       # pour chaque ligne du fichier
        valeurs = ligne.split(";")                                              # sépare les valeurs de la ligne en fonction des points-virgules
        index = 0
        valeurColonne = {}                                                      # variable qui contiendra le tuple colonne:valeur
        for colonne in entete:                                                  # pour chaque colonne
            valeurColonne[colonne] = valeurs[index]                             # associe le nom de la colonne à la valeur de la ligne
            index=index+1
        valeursLigne.append(valeurColonne)                                      # ajoute le tuple colonne:valeur à la liste des lignes
    fichier.close()                                                             # ferme le fichier
    return valeursLigne

def couleurAnnee(annee):
    """
    Retourne une couleur en fonction de l'année
    L'année est passée en paramètre
    La couleur par défaut est gris si l'année n'est pas gérée
    """
    couleur = "grey"
    if annee == "2013":
        couleur = "red"
    elif annee == "2014":
        couleur = "green"
    elif annee == "2015":
        couleur = "blue"
    elif annee == "2016":
        couleur = "purple"
    elif annee == "2017":
        couleur = "yellow"
    return couleur

def nbPropDepartement(tableau, departement):
    """
    Compte le nombre de propriétés dans un département
    Le tableau des proriétés et le département sont passés en paramètres
    """
    nbProp=0
    for ligne in tableau:
        if ligne["Département"] == departement:
            nbProp=nbProp+1
    return nbProp

def genererCarte(tableau):
    """
    Génère le fichier HTML contenant la carte des propriétés
    Le tableau des proriétés est passé en paramètre
    """
    carte = Map(location=[46.746780,5.907690],zoom_start=5.75)                                                                  # créer une nouvelle carte
    for ligne in tableau:                                                                                                       # pour chaque element du tableau
        if (ligne["Geom\n"] is not None and ligne["Geom\n"] != "" and ligne["Geom\n"] != "\n"):                                 # si la valeur n'est pas nulle, vide, ou juste un retour à la ligne
            coord = ligne["Geom\n"][:-2].split(",")                                                                             # retire le \n à la fin puis sépare les valeurs en fonction des virgules
            coordFloat = [float(coord[0]),float(coord[1])]                                                                      # les coordonnées doivent être converties en float avant de pouvoir les ajouter à la carte
            tooltip = ligne["Commune"] + " (" + ligne["Département"] + ")"                                                      # tooltip contenant le nom de la commune avec entre parenthèses le département
            desc = "<b>Date de signature</b> : " + ligne["Date_signature"]                                						# description contenant la date de signature de l'acte de vente
            couleur = couleurAnnee(ligne["Année_cession"])                                                                      # récupère le bonne couleur en fonction de l'année
            nbProp = nbPropDepartement(tableau, ligne["Département"])                                                           # compte le nombre de propriétés dans le département
            print("Ajout du point " + tooltip + " aux coordonnées " + coord[0] + "," + coord[1])
            CircleMarker(coordFloat, popup=desc, tooltip=tooltip, radius=0.1*nbProp, color=couleur, fill=True).add_to(carte)    # ajoute le point à la carte, la grosseur du cercle (radius) dépend du nombre de propriétés du département
    print("Ecriture du fichier...")
    carte.save("carte.html")                                                                                             		# sauve la carte dans un fichier HTML
    print("Terminé")

tableau = fichierVersTableau("cessions-immobilieres.csv")
genererCarte(tableau)