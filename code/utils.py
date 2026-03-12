import numpy as np
from skimage import io
from pathlib import Path


def load_points(filepath):
    """
    Commentaire explicatif fait pas ChatGPT

    Charge les points d'intérêt depuis un fichier texte.
    Le format attendu est celui de selectpoints.py : \tx\ty par ligne.
    Les coordonnées sont en (x, y), i.e. (colonne, ligne).
    """
    points = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                x, y = float(parts[0]), float(parts[1])
                points.append([x, y])
    return np.array(points, dtype=np.float64)


def load_image(filepath):
    """
    Commentaire explicatif fait pas ChatGPT

    Charge une image et la convertit en float64 dans [0, 1].
    """
    img = io.imread(str(filepath))
    # Si l'image a un canal alpha (RGBA), ne garder que RGB
    if img.ndim == 3 and img.shape[2] == 4:
        img = img[:, :, :3]
    if img.dtype == np.uint8:
        img = img.astype(np.float64) / 255.0
    return img


def add_border_points(points, img_shape):
    """
    Commentaire explicatif fait pas ChatGPT

    Ajoute des points en bordure de l'image pour gérer l'arrière-plan.
    On ajoute les 4 coins + des points intermédiaires sur les bords
    pour une meilleure couverture de l'image entière.

    Paramètres
    ----------
    points : ndarray (N, 2) — points d'intérêt existants en (x, y)
    img_shape : tuple (H, W, ...) — dimensions de l'image

    Retourne
    --------
    ndarray (N+M, 2) — points augmentés avec les points de bordure
    """
    h, w = img_shape[:2]
    max_x = w - 1
    max_y = h - 1

    border_pts = [
        # 4 coins
        [0, 0], [max_x, 0], [0, max_y], [max_x, max_y],
        # Milieux des bords
        [max_x / 2, 0], [max_x / 2, max_y],
        [0, max_y / 2], [max_x, max_y / 2],
        # Quarts des bords (pour une couverture plus dense)
        [max_x / 4, 0], [3 * max_x / 4, 0],
        [max_x / 4, max_y], [3 * max_x / 4, max_y],
        [0, max_y / 4], [0, 3 * max_y / 4],
        [max_x, max_y / 4], [max_x, 3 * max_y / 4],
    ]

    border_pts = np.array(border_pts, dtype=np.float64)
    return np.vstack([points, border_pts])


def save_image(img, filepath):
    """
    Commentaire explicatif fait pas ChatGPT

    Sauvegarde une image float [0, 1] en fichier PNG (uint8).
    """
    img_uint8 = np.clip(img * 255, 0, 255).astype(np.uint8)
    io.imsave(str(filepath), img_uint8)
