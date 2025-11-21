from flask import Flask, render_template, request
import os

# j'ai utilisé Flask pour combiner le HTML et Python (basically a framework)
app = Flask(__name__, template_folder='interface', static_folder='interface')


def parallel_prefix_sum(x):  # function thsb somme parallèle, prefix sum final, calcule prefixe

    n = len(x)
    if n == 0:
        return [], [], []  # ida user didn't type anything, return vide

    # -------------------------
    # Somme parallèle 
    # -------------------------
    arbre_somme = [x.copy()]  # on créer valeur arbre_somme w nhto fiha les valeurs initiales
    niveau_courant = x.copy()  # Niveau where we can add the pair values

    while len(niveau_courant) > 1:  # ida kan kayn aktr mn element wahd f niveau
        niveau_suivant = []  # on crée une liste pour le prochain niveau
        for i in range(0, len(niveau_courant), 2):  # parcours les elements 2 b 2
            if i + 1 < len(niveau_courant):
                # addition l 2 paire valeurs
                niveau_suivant.append(niveau_courant[i] + niveau_courant[i + 1])  # nzido niveau_courant[i] + niveau_courant[i + 1] w nzido niveau suivant
            else:
                # ida kan element impaire nkhloh kima rah
                niveau_suivant.append(niveau_courant[i])
        arbre_somme.append(niveau_suivant)  # On ajoute ce niveau à l'arbre
        niveau_courant = niveau_suivant  # On passe au niveau suivant
        # n3awdo htan yb9a element wahd w nhtoh w ytht f arbre_somme

    # -------------------------
    # # somme préfixe pour un élément Somme_prefixes[i]=x[1]+x[2]+....+x[n] 
    # -------------------------
    somme_prefixe = [0] * n #on cree un tableau vide de taille n win ha ytsocker les sommes prifixes de x , Exemple : si x = [-1, 3, 7, -5], alors somme_prefixe = [0, 0, 0, 0] au départ.
    somme_prefixe[0] = x[0]  #awl element fel somme_prefixes howa awl element fel x ,x[0] = -1 donc somme_prefixe[0] = -1 
    for i in range(1, n): #parcours l kaml indice w nbdaw mel 1 (li hwa deuxieme element)
        #calcule sequencielle,exemple x = [-1, 3, 7, -5] , -1,(-1+3)=2,(2+7)=9,..... somme_prefixe = [-1, 2, 9, 4] 
        somme_prefixe[i] = somme_prefixe[i - 1] + x[i] 
        #mtali ha nkhrjo f tableau complet des sommes préfixes

    # -------------------------
    #  calcule prefixe (tree bel3ks)
    # -------------------------
    arbre_recon = [somme_prefixe.copy()]  # arbre_recon nfsha somme_prefixe 
    niveau_courant = somme_prefixe.copy() #une copie pour construire l’arbre sans écraser les données originales (somme_prefixe)
    while len(niveau_courant) > 1: #ida kan niveau_courant kan fih aktr mn element wahd
        niveau_suivant = [] #ndiro tableau vide lel prochaine niveau d'arbre
        for i in range(0, len(niveau_courant), 2): #parcourt les éléments du niveau courant par paires , 
             #Exemple : si niveau_courant = [-1, 2, 9, 4] , i = 0 => première paire : -1 et 2 , i = 2 => deuxième paire : 9 et 4
            if i + 1 < len(niveau_courant): #ida kayn paire complete (meanah i+1 existe) mtln i=0 w i=0+!=1 
                # alors on ajoute l'enfant droit, exemple : aendna nv_cr=[a,b,c,d] paires:[a,b] et [c,d] niveau_suiv=[b,d]
                niveau_suivant.append(niveau_courant[i + 1])
            else:#ida mknsh paire mtln 3 valeurs , [a,b,c] [a,b][c] niv_suiv=[b,c]
                niveau_suivant.append(niveau_courant[i])
        arbre_recon.append(niveau_suivant) #liste fiha kml les niveaux (kol khatra nzido niveau li lginah) twli arbre fiha kaml levels
        niveau_courant = niveau_suivant #n3gbo lel niveau suivant htan nlhgo lel racine
        #exemple : Niveau 0 : [ -1, 2, 9, 4, 7, 24, 32, 53 ]<= niveau_courant / Niveau 1 : [ 2, 9, 24, 53 ] <= niveau_suivant ki ndiro niveau_courant = niveau_suivant
        #ha twli niveau_courant = [ 2, 9, 24, 53 ] w nkmlo nhsbo 




    return somme_prefixe, arbre_somme, arbre_recon #somme_prefixe=resultat finale , 
        #arbre_somme=comment les sommations parallèles ont été faites example : 
          #Niveau 0 : [-1, 3, 7, -5, 3, 17, 8, 21]
          #Niveau 1 : [2, 2, 20, 29]
          #Niveau 2 : [4, 49]
          #Niveau 3 : [53]
        #rbre_recon:comment on reconstruit les résultats à partir des préfixes 
          #Niveau 0 : [-1, 2, 9, 4, 7, 24, 32, 53]
          #Niveau 1 : [2, 9, 24, 53]
          #Niveau 2 : [9, 53]
          #Niveau 3 : [53]
   


# Quand l'utilisateur entre des nombres et clique sur "Envoyer",
# on calcule le prefix-sum et on affiche les résultats.

@app.route("/", methods=["GET", "POST"])
def index():
    input_numbers = ""
    somme_prefixe = []
    arbre_somme = []
    arbre_recon = []

    if request.method == "POST":
        input_numbers = request.form.get("numbers", "")
        try:
            numbers = [int(num.strip()) for num in input_numbers.split(",")]
            somme_prefixe, arbre_somme, arbre_recon = parallel_prefix_sum(numbers)
        except ValueError:
            somme_prefixe = arbre_somme = arbre_recon = ["Erreur : entrez des nombres séparés par des virgules"]

    return render_template("index.html",
                           input_numbers=input_numbers,
                           S=somme_prefixe,
                           up_tree=arbre_somme,
                           down_tree=arbre_recon)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
