"""
Script principal pour générer une séquence de métamorphose entre deux images.

Utilisation :
    python generate_sequence.py --img1 path/to/img1.png --img2 path/to/img2.png \
                                --pts1 path/to/pts1.txt --pts2 path/to/pts2.txt \
                                --output_dir path/to/output \
                                --num_frames 100 --fps 25
"""

import argparse
import numpy as np
from pathlib import Path
import subprocess

from morph import morph, compute_triangulation
from utils import load_image, load_points, add_border_points, save_image


def generate_frames(img1, img2, pts1, pts2, tri, num_frames, output_dir):
    """
    Génère les trames de la métamorphose et les sauvegarde en PNG.

    Le warp_frac et dissolve_frac varient linéairement de 0 à 1 sur
    l'ensemble des trames. L'astuce suggérée dans l'énoncé (augmenter
    warp_frac avant dissolve_frac) est implémentée avec un décalage :
    warp_frac avance légèrement plus vite au début.

    Paramètres
    ----------
    img1, img2 : ndarray (H, W, C) — images source et cible
    pts1, pts2 : ndarray (N, 2) — points d'intérêt correspondants
    tri : Delaunay — triangulation pré-calculée
    num_frames : int — nombre total de trames
    output_dir : Path — dossier où sauvegarder les trames
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for i in range(num_frames):
        t = i / (num_frames - 1)  # t varie de 0 à 1

        # Stratégie : warp_frac mène légèrement devant dissolve_frac
        # Cela permet d'aligner les formes avant de fondre les couleurs
        warp_frac = np.clip(t * 1.2, 0, 1)
        dissolve_frac = np.clip(t * 1.2 - 0.2, 0, 1)

        # Alternative simple : les deux linéaires (décommenter si désiré)
        # warp_frac = t
        # dissolve_frac = t

        print(f"Trame {i+1}/{num_frames} — warp={warp_frac:.3f}, dissolve={dissolve_frac:.3f}")

        morphed = morph(img1, img2, pts1, pts2, tri, warp_frac, dissolve_frac)

        filename = output_dir / f"frame_{i+1:05d}.png"
        save_image(morphed, filename)

    print(f"Toutes les trames sauvegardées dans {output_dir}")


def create_video(frames_dir, output_video, fps=25):
    """
    Crée un fichier vidéo MP4 à partir des trames PNG avec ffmpeg.

    Paramètres
    ----------
    frames_dir : Path — dossier contenant les trames frame_00001.png, ...
    output_video : Path — chemin du fichier vidéo de sortie
    fps : int — images par seconde
    """
    frames_pattern = str(Path(frames_dir) / "frame_%05d.png")
    output_video = str(output_video)

    cmd = [
        "ffmpeg", "-y",
        "-i", frames_pattern,
        "-c:v", "libx264",
        "-vf", f"fps={fps},format=yuv420p",
        output_video
    ]

    print(f"Création de la vidéo : {output_video}")
    subprocess.run(cmd, check=True)
    print("Vidéo créée avec succès.")


def main():
    parser = argparse.ArgumentParser(description="Génération de séquence de métamorphose")
    parser.add_argument("--img1", type=str, required=True,
                        help="Chemin de l'image source (personne N-1)")
    parser.add_argument("--img2", type=str, required=True,
                        help="Chemin de l'image cible (votre photo)")
    parser.add_argument("--pts1", type=str, required=True,
                        help="Chemin du fichier de points de l'image source")
    parser.add_argument("--pts2", type=str, required=True,
                        help="Chemin du fichier de points de l'image cible")
    parser.add_argument("--output_dir", type=str, default="output/frames",
                        help="Dossier pour les trames générées")
    parser.add_argument("--video_output", type=str, default="output/morphing.mp4",
                        help="Chemin du fichier vidéo de sortie")
    parser.add_argument("--num_frames", type=int, default=100,
                        help="Nombre total de trames (100 = 4s à 25fps)")
    parser.add_argument("--fps", type=int, default=25,
                        help="Images par seconde pour la vidéo")

    args = parser.parse_args()

    # Charger les images
    print("Chargement des images...")
    img1 = load_image(args.img1)
    img2 = load_image(args.img2)

    # Vérifier que les images ont les mêmes dimensions
    assert img1.shape == img2.shape, \
        f"Les images doivent avoir les mêmes dimensions! img1={img1.shape}, img2={img2.shape}"

    # Charger les points d'intérêt
    print("Chargement des points d'intérêt...")
    pts1 = load_points(args.pts1)
    pts2 = load_points(args.pts2)

    assert pts1.shape == pts2.shape, \
        f"Les deux fichiers de points doivent avoir le même nombre de points! pts1={pts1.shape}, pts2={pts2.shape}"

    # Ajouter les points de bordure pour gérer l'arrière-plan
    pts1 = add_border_points(pts1, img1.shape)
    pts2 = add_border_points(pts2, img2.shape)

    # Calculer la triangulation une seule fois (sur la moyenne des points)
    print("Calcul de la triangulation de Delaunay...")
    tri = compute_triangulation(pts1, pts2)
    print(f"  -> {len(tri.simplices)} triangles générés")

    # Générer les trames
    generate_frames(img1, img2, pts1, pts2, tri, args.num_frames, args.output_dir)

    # Créer la vidéo
    Path(args.video_output).parent.mkdir(parents=True, exist_ok=True)
    create_video(args.output_dir, args.video_output, args.fps)


if __name__ == "__main__":
    main()
