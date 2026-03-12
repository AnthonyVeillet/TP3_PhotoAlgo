import numpy as np
from scipy.spatial import Delaunay
from scipy.interpolate import RectBivariateSpline
from matplotlib.path import Path


def compute_affine(src_tri, dst_tri):
    """
    Commentaire explicatif fait pas ChatGPT

    Calcule la matrice de transformation affine 2x3 qui transforme
    les points du triangle source vers le triangle destination.

    On résout : dst = T @ [src_x, src_y, 1]^T

    Paramètres
    ----------
    src_tri : ndarray (3, 2) — sommets du triangle source en (x, y)
    dst_tri : ndarray (3, 2) — sommets du triangle destination en (x, y)

    Retourne
    --------
    T : ndarray (2, 3) — matrice de transformation affine
    """
    # Matrice homo points source (3x3)
    # Chaque colonne [x, y, 1]^T
    src_h = np.array([
        [src_tri[0, 0], src_tri[1, 0], src_tri[2, 0]],
        [src_tri[0, 1], src_tri[1, 1], src_tri[2, 1]],
        [1.0, 1.0, 1.0]
    ])

    # Matrice des points destination (2x3)
    dst_m = np.array([
        [dst_tri[0, 0], dst_tri[1, 0], dst_tri[2, 0]],
        [dst_tri[0, 1], dst_tri[1, 1], dst_tri[2, 1]]
    ])

    # T = dst_m @ inv(src_h)
    T = dst_m @ np.linalg.inv(src_h)
    return T


def compute_triangulation(pts1, pts2):
    """
    Commentaire explicatif fait pas ChatGPT

    Calcule la triangulation de Delaunay sur la moyenne des deux ensembles
    de points. Cela minimise la déformation des triangles.

    Paramètres
    ----------
    pts1 : ndarray (N, 2) — points d'intérêt de l'image 1
    pts2 : ndarray (N, 2) — points d'intérêt de l'image 2

    Retourne
    --------
    tri : scipy.spatial.Delaunay — triangulation
    """
    avg_pts = (pts1 + pts2) / 2.0
    tri = Delaunay(avg_pts)
    return tri


def morph(img1, img2, img1_pts, img2_pts, tri, warp_frac, dissolve_frac):
    """
    Commentaire explicatif fait pas ChatGPT

    Produit une image intermédiaire (métamorphose) entre img1 et img2.

    Algorithme :
    1. Calcule les points intermédiaires : mid = (1-warp_frac)*pts1 + warp_frac*pts2
    2. Pour chaque triangle de la triangulation :
       a. Calcule les transformations affines inverses (mid → img1, mid → img2)
       b. Pour chaque pixel dans le triangle intermédiaire, retrouve les
          coordonnées correspondantes dans img1 et img2
       c. Interpole les couleurs avec RectBivariateSpline
       d. Mélange les couleurs selon dissolve_frac

    Paramètres
    ----------
    img1, img2 : ndarray (H, W, C) — images en float [0, 1]
    img1_pts, img2_pts : ndarray (N, 2) — points d'intérêt en (x, y)
    tri : scipy.spatial.Delaunay — triangulation (calculée une seule fois)
    warp_frac : float [0, 1] — contrôle la déformation de forme
        0 = forme de img1, 1 = forme de img2
    dissolve_frac : float [0, 1] — contrôle le fondu des couleurs
        0 = couleurs de img1, 1 = couleurs de img2

    Retourne
    --------
    morphed_img : ndarray (H, W, C) — image métamorphosée
    """
    h, w = img1.shape[:2]
    num_channels = img1.shape[2] if img1.ndim == 3 else 1

    # Points intermédiaires
    mid_pts = (1.0 - warp_frac) * img1_pts + warp_frac * img2_pts

    # Créer interpolateurs pour chaque canal de chaque image
    ys = np.arange(h)
    xs = np.arange(w)

    interp1 = []
    interp2 = []
    for c in range(num_channels):
        if img1.ndim == 3:
            interp1.append(RectBivariateSpline(ys, xs, img1[:, :, c]))
            interp2.append(RectBivariateSpline(ys, xs, img2[:, :, c]))
        else:
            interp1.append(RectBivariateSpline(ys, xs, img1))
            interp2.append(RectBivariateSpline(ys, xs, img2))

    # Image de sortie
    morphed_img = np.zeros_like(img1)

    # Pour chaque triangle de la triangulation
    for simplex in tri.simplices:
        # Sommets du triangle dans chaque espace de coordonnées
        mid_tri = mid_pts[simplex]       # (3, 2) — triangle intermédiaire
        img1_tri = img1_pts[simplex]     # (3, 2) — triangle dans img1
        img2_tri = img2_pts[simplex]     # (3, 2) — triangle dans img2

        # Boite autour triangle intermédiaire
        min_x = max(0, int(np.floor(mid_tri[:, 0].min())))
        max_x = min(w - 1, int(np.ceil(mid_tri[:, 0].max())))
        min_y = max(0, int(np.floor(mid_tri[:, 1].min())))
        max_y = min(h - 1, int(np.ceil(mid_tri[:, 1].max())))

        if min_x > max_x or min_y > max_y:
            continue

        # Grille de pixels dans la boîte entourante
        xx, yy = np.meshgrid(
            np.arange(min_x, max_x + 1),
            np.arange(min_y, max_y + 1)
        )
        bbox_points = np.column_stack([xx.ravel(), yy.ravel()])  # (M, 2) en (x, y)

        # Trouver pixels dans le triangle
        path = Path(mid_tri)
        mask = path.contains_points(bbox_points)

        if not np.any(mask):
            continue

        pixels_xy = bbox_points[mask]  # (K, 2) en (x, y)

        # Transfo affines inverses
        T1 = compute_affine(mid_tri, img1_tri)
        T2 = compute_affine(mid_tri, img2_tri)

        # Appliquer les transfo
        ones = np.ones((pixels_xy.shape[0], 1))
        pixels_h = np.hstack([pixels_xy, ones])  # (K, 3)

        src1_xy = (T1 @ pixels_h.T).T  # (K, 2) — coordonnées dans img1
        src2_xy = (T2 @ pixels_h.T).T  # (K, 2) — coordonnées dans img2

        # Indices des pixels de destination dans l'image de sortie
        dst_cols = pixels_xy[:, 0].astype(int)
        dst_rows = pixels_xy[:, 1].astype(int)

        # Interpoler et mélanger pour chaque canal
        for c in range(num_channels):
            # RectBivariateSpline.ev prend (y, x) = (row, col)
            vals1 = interp1[c].ev(src1_xy[:, 1], src1_xy[:, 0])
            vals2 = interp2[c].ev(src2_xy[:, 1], src2_xy[:, 0])

            # Fondu des couleurs
            blended = (1.0 - dissolve_frac) * vals1 + dissolve_frac * vals2

            if img1.ndim == 3:
                morphed_img[dst_rows, dst_cols, c] = blended
            else:
                morphed_img[dst_rows, dst_cols] = blended

    return np.clip(morphed_img, 0.0, 1.0)
