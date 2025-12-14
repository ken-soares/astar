## Liste des choses à retravailler et/ou à implémenter

- faire une fonction win condition qui permet de dire si le joueur a reussi
- faire le lien IA-joueur avec un tour par tour
- faire un systeme de points avec plusieurs manches eventuellement
- designer une map où il est toujours possible de gagner
- definir une liste de coordonnées valables pour le goal afin que le jeu soit gagnable

- La fonction ```create_grid``` ne récupère pas dynamiquement la taille de la grille. Celle-ci est pour l'instant définie dans le fichier ```consts.py``` ==> Inutile si chargée depuis le fichier.
- Déplacer le fichier ```board.txt```. Peut-être dans un dossier ```Resources``` ?
- Système de "safefail" si la fenêtre de jeu ne s'est pas lancée
- Gérer les joueurs ==> Il faudra sans doute changer le système de ```value```/```goal``` pour les cellules de la grille.