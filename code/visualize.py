"""
Script utilitaire pour visualiser la triangulation de Delaunay sur les images.
Utile pour vérifier que les points et la triangulation sont corrects.

Utilisation :
    python visualize.py --img path/to/image.png --pts path/to/points.txt
    python visualize.py --img1 img1.png --img2 img2.png --pts1 pts1.txt --pts2 pts2.txt
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation

from morph import compute_triangulation
from utils import load_image, load_points, add_border_points


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


def main():
    parser = argparse.ArgumentParser(description="Visualisation de la triangulation")
    parser.add_argument("--img1", type=str, required=True, help="Image 1")
    parser.add_argument("--img2", type=str, required=True, help="Image 2")
    parser.add_argument("--pts1", type=str, required=True, help="Points de l'image 1")
    parser.add_argument("--pts2", type=str, required=True, help="Points de l'image 2")

    args = parser.parse_args()

    img1 = load_image(args.img1)
    img2 = load_image(args.img2)
    pts1 = load_points(args.pts1)
    pts2 = load_points(args.pts2)

    print(f"Image 1 : {img1.shape}")
    print(f"Image 2 : {img2.shape}")
    print(f"Points 1 : {pts1.shape[0]} points")
    print(f"Points 2 : {pts2.shape[0]} points")

    tri = visualize_triangulation(img1, img2, pts1, pts2)
    print(f"Triangulation : {len(tri.simplices)} triangles")


if __name__ == "__main__":
    main()
