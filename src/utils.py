def is_valid_move(board, x, y, player):
    # Détermine la couleur de l'adversaire
    opponent = 'W' if player == 'B' else 'B'

    # Vérifie si la case est déjà occupée
    if board[x][y] != '_':
        return False, []  # Le coup n'est pas valide, pas de cellules retournées

    # Liste des huit directions possibles (voisins)
    directions = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx != 0 or dy != 0]

    # Liste pour stocker les cellules à retourner
    flipped_cells = []

    # Parcours de chaque direction possible
    for dx, dy in directions:
        # Initialise une liste pour les cellules à retourner dans cette direction
        temp_flips = []
        # Déplacement initial à partir de la case de départ (x, y)
        nx, ny = x + dx, y + dy

        # Tant que les coordonnées sont à l'intérieur du plateau
        while 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] == opponent:
                # Ajoute les coordonnées de l'adversaire à la liste temporaire
                temp_flips.append((nx, ny))
            elif board[nx][ny] == player:
                if temp_flips:
                    # S'il y a des cellules adverses entre les cellules du joueur actuel,
                    # ajoute-les à la liste des cellules à retourner
                    flipped_cells.extend(temp_flips)
                break
            else:
                break  # La case est vide, donc le coup n'est pas valide
            # Met à jour les coordonnées pour passer à la case suivante dans la direction
            nx += dx
            ny += dy

    # Le coup est valide s'il y a des cellules à retourner
    return len(flipped_cells) > 0, flipped_cells

def has_valid_move(board, player):
    taille_grille = len(board)

    for row in range(taille_grille):
        for col in range(taille_grille):
            if is_valid_move(board, row, col, player)[0]:
                return True

    return False

def positions_jouables(board, player):
    positions = []
    for x in range(8):
        for y in range(8):
            if is_valid_move(board, x, y, player)[0]:
                positions.append((x, y))
    return positions

def make_move(board, x, y, player):
    is_valid, flipped_cells = is_valid_move(board, x, y, player)
    if is_valid:
        board[x][y] = player
        for fx, fy in flipped_cells:
            board[fx][fy] = player
    return is_valid