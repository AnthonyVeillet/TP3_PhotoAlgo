"""
Script utilitaire pour visualiser la triangulation de Delaunay sur les images.
Utile pour vérifier que les points et la triangulation sont corrects.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

from morph import compute_triangulation
from utils import load_image, load_points, add_border_points


# =============================================================================
# CHEMINS À MODIFIER SELON VOTRE CONFIGURATION
# =============================================================================
img1_path = "../data/dataInput/14_Lebel_Philippe.jpg"
img2_path = "../data/dataInput/54_Veillet_Anthony.jpg"
pts1_path = "../data/dataInput/14_Lebel_Philippe.txt"
pts2_path = "../data/dataInput/54_Veillet_Anthony.txt"


def visualize_single(img, pts, title="Image avec triangulation"):
    """Affiche une image avec ses points d'intérêt."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.imshow(img)
    ax.plot(pts[:, 0], pts[:, 1], 'r.', markersize=8)
    for i, (x, y) in enumerate(pts):
        ax.text(x + 3, y - 3, str(i + 1), fontsize=8, color='yellow')
    ax.set_title(title)
    plt.tight_layout()
    plt.show()


def visualize_triangulation(img1, img2, pts1, pts2):
    """
    Affiche les deux images avec la triangulation de Delaunay superposée.
    """
    # Ajouter les points de bordure
    pts1_full = add_border_points(pts1, img1.shape)
    pts2_full = add_border_points(pts2, img2.shape)

    # Calculer la triangulation sur la moyenne
    tri = compute_triangulation(pts1_full, pts2_full)

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    for ax, img, pts, title in [
        (axes[0], img1, pts1_full, "Image 1 + Triangulation"),
        (axes[1], img2, pts2_full, "Image 2 + Triangulation"),
    ]:
        ax.imshow(img)

        # Dessiner la triangulation
        mtri = Triangulation(pts[:, 0], pts[:, 1], tri.simplices)
        ax.triplot(mtri, 'g-', linewidth=0.8, alpha=0.7)
        ax.plot(pts[:, 0], pts[:, 1], 'r.', markersize=5)
        ax.set_title(title)

    plt.tight_layout()
    plt.show()

    return tri


# =============================================================================
# EXÉCUTION
# =============================================================================

img1 = load_image(img1_path)
img2 = load_image(img2_path)
pts1 = load_points(pts1_path)
pts2 = load_points(pts2_path)

print(f"Image 1 : {img1.shape}")
print(f"Image 2 : {img2.shape}")
print(f"Points 1 : {pts1.shape[0]} points")
print(f"Points 2 : {pts2.shape[0]} points")

tri = visualize_triangulation(img1, img2, pts1, pts2)
print(f"Triangulation : {len(tri.simplices)} triangles")