import time
import pygame
import sys
import othello_game
import menu

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu Othello")

# Couleurs
vert = (42, 81, 45)
blanc = (255, 255, 255)
bleu_clair = (161, 212, 164)  # Couleur bleu clair
noir = (0, 0, 0)

# Police de texte
police = pygame.font.Font(None, 36)

# Titre du jeu
titre_police = pygame.font.Font(None, 72)
titre = titre_police.render("Othello", True, noir)
titre_rect = titre.get_rect()
titre_rect.center = (largeur // 2, 50)

def afficher_grille(board):
    fenetre.fill(vert)
    fenetre.blit(titre, titre_rect)  # Affichage du titre en haut

    taille_grille = len(board)
    taille_case = 50

    # Calcul des coordonnées pour centrer le tableau de jeu
    x_debut = (largeur - (taille_grille * taille_case)) // 2
    y_debut = (hauteur - (taille_grille * taille_case)) // 2

    for row in range(taille_grille):
        for col in range(taille_grille):
            x = x_debut + col * taille_case
            y = y_debut + row * taille_case

            # Dessiner un rectangle autour de chaque case
            pygame.draw.rect(fenetre, bleu_clair, (x, y, taille_case, taille_case), 1)

            # Dessiner les pions
            if board[row][col] == 'B':
                pygame.draw.circle(fenetre, noir, (x + taille_case // 2, y + taille_case // 2), taille_case // 2 - 5)
            elif board[row][col] == 'W':
                pygame.draw.circle(fenetre, blanc, (x + taille_case // 2, y + taille_case // 2), taille_case // 2 - 5)

def afficher_info(tour, pions_noirs, pions_blancs, player_turn):
    # Affichage du décompte des tours
    tour_texte = police.render(f"Tour : {tour}", True, noir)
    tour_texte_rect = tour_texte.get_rect()
    tour_texte_rect.topright = (largeur - 20, 20)
    fenetre.blit(tour_texte, tour_texte_rect)

    # Affichage du nombre de pions noirs et blancs
    pions_noirs_texte = police.render(f"Noirs : {pions_noirs}", True, noir)
    pions_noirs_texte_rect = pions_noirs_texte.get_rect()
    pions_noirs_texte_rect.topright = (largeur - 20, 60)
    fenetre.blit(pions_noirs_texte, pions_noirs_texte_rect)

    pions_blancs_texte = police.render(f"Blancs : {pions_blancs}", True, noir)
    pions_blancs_texte_rect = pions_blancs_texte.get_rect()
    pions_blancs_texte_rect.topright = (largeur - 20, 100)
    fenetre.blit(pions_blancs_texte, pions_blancs_texte_rect)
    
    # Affichage du joueur actuel
    joueur_texte = police.render(f"Joueur : {player_turn}", True, noir)
    joueur_texte_rect = joueur_texte.get_rect()
    joueur_texte_rect.topright = (largeur - 20, 140)
    fenetre.blit(joueur_texte, joueur_texte_rect)

    # Bouton "Retour" sous la grille de jeu
    pygame.draw.rect(fenetre, bleu_clair, (largeur - 100, hauteur - 60, 80, 40))
    retour_texte = police.render("Retour", True, noir)
    retour_texte_rect = retour_texte.get_rect()
    retour_texte_rect.center = (largeur - 60, hauteur - 40)
    fenetre.blit(retour_texte, retour_texte_rect)   
 
def afficher_bouton_rejouer():
    # Bouton "Rejouer" sous la grille de jeu
    pygame.draw.rect(fenetre, bleu_clair, (largeur - 100, hauteur - 60, 80, 40))
    retour_texte = police.render("Rejouer", True, noir)
    retour_texte_rect = retour_texte.get_rect()
    retour_texte_rect.center = (largeur - 60, hauteur - 40)
    fenetre.blit(retour_texte, retour_texte_rect)
 
def afficher_victoire(player):
    # Créez un rectangle pour afficher le message de victoire
    victoire_rect = pygame.Rect(0, hauteur - 100, largeur, 50)
    
    # Remplissez le rectangle avec une couleur de fond
    pygame.draw.rect(fenetre, vert, victoire_rect)
    
    # Utilisez la police de texte pour afficher le message de victoire
    if player == 'Egalité':
        victoire_texte = police.render("Egalité !", True, noir)
    else:
        victoire_texte = police.render(f"Bravo, le joueur {player} a gagné !", True, noir)
    victoire_texte_rect = victoire_texte.get_rect()
    victoire_texte_rect.center = victoire_rect.center
    
    # Affichez le texte de victoire dans le rectangle
    fenetre.blit(victoire_texte, victoire_texte_rect)

def jeuPvP():
    board = othello_game.init_board()
    player_turn = 'B'  # Commencez avec les Noirs
    
    taille_grille = len(board)
    taille_case = 50
    
    x_debut = (largeur - (taille_grille * taille_case)) // 2
    y_debut = (hauteur - (taille_grille * taille_case)) // 2
    
    tour = 0  # Initialisez le décompte des tours
    pions_noirs = 2  # Initialisez le nombre de pions noirs
    pions_blancs = 2  # Initialisez le nombre de pions blancs

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Obtenez les coordonnées du clic de souris
                x, y = pygame.mouse.get_pos()
                
                if largeur - 100 <= x <= largeur - 20 and hauteur - 60 <= y <= hauteur - 20:
                    menu.main()  # Appeler menu.main() lorsque le bouton "Retour" est cliqué
        
                # Convertissez les coordonnées de la souris en coordonnées de case
                x_case = (x - x_debut) // taille_case
                y_case = (y - y_debut) // taille_case

                # Vérifiez si le coup est valide
                is_valid, _ = othello_game.is_valid_move(board, y_case, x_case, player_turn)

                if is_valid:
                    # Mettez à jour le plateau avec le coup
                    othello_game.make_move(board, y_case, x_case, player_turn)
                    
                    # Mettez à jour le décompte des tours
                    tour += 1
                    
                    # Mettez à jour le nombre de pions de chaque couleur
                    pions_noirs = sum(row.count('B') for row in board)
                    pions_blancs = sum(row.count('W') for row in board)
                    
                    # Passez au tour suivant
                    player_turn = 'W' if player_turn == 'B' else 'B'
        
        
        # Affichez le plateau mis à jour et les informations
        afficher_grille(board)
        afficher_info(tour, pions_noirs, pions_blancs, player_turn)
        pygame.display.flip()

        # Vérifiez si la partie est terminée   
        if not othello_game.has_valid_move(board, 'B') and not othello_game.has_valid_move(board, 'W'):
            print("Fin de la partie car plus de coups possibles")
            if pions_noirs > pions_blancs:
                afficher_victoire('Noir')
            elif pions_blancs > pions_noirs:
                afficher_victoire('Blanc')
            else:
                afficher_victoire('Égalité')
            pygame.display.flip()
            pygame.time.delay(5000)  # Pause de 3 secondes pour afficher le résultat
            # return  # Sortez de la boucle de jeu
        elif not othello_game.has_valid_move(board, 'B') and player_turn == 'B':
            print("changement de joueur de B à W")
            player_turn = 'W'
        elif not othello_game.has_valid_move(board, 'W') and player_turn == 'W':
            player_turn = 'B'
            print("changement de joueur de W à B")

# def jeuPvAI():
#     board = othello_game.init_board()
#     player_turn = 'B'  # Commencez avec les Noirs
    
#     taille_grille = len(board)
#     taille_case = 50
    
#     x_debut = (largeur - (taille_grille * taille_case)) // 2
#     y_debut = (hauteur - (taille_grille * taille_case)) // 2
    
#     tour = 0  # Initialisez le décompte des tours
#     pions_noirs = 2  # Initialisez le nombre de pions noirs
#     pions_blancs = 2  # Initialisez le nombre de pions blancs

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
            
#             if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 # Obtenez les coordonnées du clic de souris
#                 x, y = pygame.mouse.get_pos()
                
#                 # Convertissez les coordonnées de la souris en coordonnées de case
#                 x_case = (x - x_debut) // taille_case
#                 y_case = (y - y_debut) // taille_case
                
#                 if largeur - 100 <= x <= largeur - 20 and hauteur - 60 <= y <= hauteur - 20:
#                     menu.main()  # Appeler menu.main() lorsque le bouton "Retour" est cliqué

#                 # Vérifiez si le coup est valide
#                 is_valid, _ = othello_game.is_valid_move(board, y_case, x_case, player_turn)

#                 if is_valid:
#                     # Mettez à jour le plateau avec le coup
#                     othello_game.make_move(board, y_case, x_case, player_turn)
#                     afficher_grille(board)
#                     afficher_info(tour, pions_noirs, pions_blancs, player_turn)
#                     pygame.display.flip()
#                     # Mettez à jour le décompte des tours
#                     tour += 1
                    
#                     # Mettez à jour le nombre de pions de chaque couleur
#                     pions_noirs = sum(row.count('B') for row in board)
#                     pions_blancs = sum(row.count('W') for row in board)
                    
#                     # Vérification de la fin du jeu
#                     if all(cell != ' ' for row in board for cell in row):
#                         w_score = sum(cell == 'W' for row in board for cell in row)
#                         b_score = sum(cell == 'B' for row in board for cell in row)
#                         print(f"Final scores - W: {w_score}, B: {b_score}")
#                         if w_score > b_score:
#                             print("Human wins!")
#                         elif b_score > w_score:
#                             print("AI wins!")
#                         else:
#                             print("It's a tie!")
#                         break
                    
#                     # Passez au tour suivant
#                     if player_turn == 'W' and othello_game.has_valid_move(board, 'B'):
#                         player_turn = 'B'
#                     elif player_turn == 'B' and othello_game.has_valid_move(board, 'W'):
#                         player_turn = 'W'
#                     elif player_turn == 'W' and not othello_game.has_valid_move(board, 'B'):
#                         if not othello_game.has_valid_move(board, 'W') : 
#                             print("Fin de la partie car plus de coups possibles")
#                             if pions_noirs > pions_blancs:
#                                 afficher_victoire('Noir')
#                             elif pions_blancs > pions_noirs:
#                                 afficher_victoire('Blanc')
#                             else:
#                                 afficher_victoire('Égalité')
#                             pygame.display.flip()
#                             pygame.time.delay(5000)  # Pause de 3 secondes pour afficher le résultat
#                         else : 
#                             player_turn = 'W'
#                     elif player_turn == 'B' and not othello_game.has_valid_move(board, 'W'):
#                         if not othello_game.has_valid_move(board, 'B') : 
#                             print("Fin de la partie car plus de coups possibles")
#                             if pions_noirs > pions_blancs:
#                                 afficher_victoire('Noir')
#                             elif pions_blancs > pions_noirs:
#                                 afficher_victoire('Blanc')
#                             else:
#                                 afficher_victoire('Égalité')
#                             pygame.display.flip()
#                             pygame.time.delay(5000)  # Pause de 3 secondes pour afficher le résultat
#                         else : 
#                             player_turn = 'B'
                    
                    
                            
#         # Si c'est au tour de l'IA (les Noirs dans ce cas)
#         if player_turn == 'B':
#             # Simulation de l'IA en utilisant l'algorithme min-max avec mémoire
#             timeout = time.time() + 2  # 2 secondes de time-out pour l'IA
#             _, (x, y) = othello_game.minmax_with_memory(board, 3, True, 'B', timeout)
#             if x is None and y is None:
#                 print("AI timeout. Human wins!")
#                 break
            
#             # Mettez à jour le plateau avec le coup de l'IA
#             othello_game.make_move(board, x, y, player_turn)
            
#             # Mettez à jour le décompte des tours
#             tour += 1
            
#             # Mettez à jour le nombre de pions de chaque couleur
#             pions_noirs = sum(row.count('B') for row in board)
#             pions_blancs = sum(row.count('W') for row in board)
            
#             # Vérification de la fin du jeu
#             # if all(cell != ' ' for row in board for cell in row):
#             #     w_score = sum(cell == 'W' for row in board for cell in row)
#             #     b_score = sum(cell == 'B' for row in board for cell in row)
#             #     print(f"Final scores - W: {w_score}, B: {b_score}")
#             #     if w_score > b_score:
#             #         print("Human wins!")
#             #     elif b_score > w_score:
#             #         print("AI wins!")
#             #     else:
#             #         print("It's a tie!")
#             #     break
#             if not othello_game.has_valid_move(board, 'B') and not othello_game.has_valid_move(board, 'W'):
#                 print("Fin de la partie car plus de coups possibles")
#                 if pions_noirs > pions_blancs:
#                     afficher_victoire('Noir')
#                 elif pions_blancs > pions_noirs:
#                     afficher_victoire('Blanc')
#                 else:
#                     afficher_victoire('Égalité')
#                 pygame.display.flip()
#                 pygame.time.delay(5000)  # Pause de 5 secondes pour afficher le résultat
#                 break
#             elif not othello_game.has_valid_move(board, 'B') and player_turn == 'B':
#                 print("changement de joueur de B à W")
#                 player_turn = 'W'
#             elif not othello_game.has_valid_move(board, 'W') and player_turn == 'W':
#                 player_turn = 'B'
#                 print("changement de joueur de W à B")
            
#             # Passez au tour suivant (joueur humain)
#             player_turn = 'W'
        
#         # Affichez le plateau mis à jour et les informations
#         afficher_grille(board)
#         afficher_info(tour, pions_noirs, pions_blancs, player_turn)
#         pygame.display.flip()

def jeuPvAI():
    board = othello_game.init_board()
    player_turn = 'B'  # Commencez avec les Noirs

    # Initialisation de la grille et d'autres paramètres
    taille_grille = len(board)
    taille_case = 50
    x_debut = (largeur - (taille_grille * taille_case)) // 2
    y_debut = (hauteur - (taille_grille * taille_case)) // 2
    tour = 0  # Initialisez le décompte des tours
    pions_noirs = 2  # Initialisez le nombre de pions noirs
    pions_blancs = 2  # Initialisez le nombre de pions blancs

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_case = (x - x_debut) // taille_case
                y_case = (y - y_debut) // taille_case
                
                if largeur - 100 <= x <= largeur - 20 and hauteur - 60 <= y <= hauteur - 20:
                    menu.main()  # Appeler menu.main() lorsque le bouton "Retour" est cliqué

                is_valid, _ = othello_game.is_valid_move(board, y_case, x_case, player_turn)

                if is_valid:
                    othello_game.make_move(board, y_case, x_case, player_turn)
                    tour += 1
                    pions_noirs = sum(row.count('B') for row in board)
                    pions_blancs = sum(row.count('W') for row in board)
                    afficher_grille(board)
                    afficher_info(tour, pions_noirs, pions_blancs, player_turn)
                    pygame.display.flip()
                    pygame.time.delay(500)  # Pause de 1 seconde pour afficher le résultat
                    
                    if all(cell != ' ' for row in board for cell in row) or (not othello_game.has_valid_move(board, 'B') and not othello_game.has_valid_move(board, 'W')):
                        print("Fin de la partie car plus de coups possibles")
                        if pions_noirs > pions_blancs:
                            afficher_victoire('Noir')
                        elif pions_blancs > pions_noirs:
                            afficher_victoire('Blanc')
                        else:
                            afficher_victoire('Égalité')
                        pygame.display.flip()
                        # pygame.time.delay(5000)  # Pause de 5 secondes pour afficher le résultat
                        break  # Fin de la partie
                    elif player_turn == 'W' and othello_game.has_valid_move(board, 'B'):
                        player_turn = 'B'
                    elif player_turn == 'B' and othello_game.has_valid_move(board, 'W'):
                        print("On passe le tour du jouer Noir")
                        player_turn = 'W'

        if player_turn == 'B':
            timeout = time.time() + 2  # 2 secondes de time-out pour l'IA
            _, (x, y) = othello_game.minmax_with_memory(board, 3, True, 'B', timeout)
            if x is None and y is None:
                print("AI timeout. Human wins!")
                break

            othello_game.make_move(board, x, y, player_turn)
            tour += 1
            pions_noirs = sum(row.count('B') for row in board)
            pions_blancs = sum(row.count('W') for row in board)
            if player_turn == 'W' and othello_game.has_valid_move(board, 'B'):
                player_turn = 'B'
            elif player_turn == 'B' and othello_game.has_valid_move(board, 'W'):
                print("On passe le tour du jouer Blanc")
                player_turn = 'W'

        afficher_grille(board)
        afficher_info(tour, pions_noirs, pions_blancs, player_turn)
        pygame.display.flip()


if __name__ == "__main__":
    jeuPvAI()
