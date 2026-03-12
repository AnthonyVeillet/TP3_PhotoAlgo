"""
Script principal pour générer une séquence de métamorphose entre deux images.
"""

import numpy as np
from pathlib import Path
import subprocess

from morph import morph, compute_triangulation
from utils import load_image, load_points, add_border_points, save_image


# =============================================================================
# CHEMINS À MODIFIER SELON VOTRE CONFIGURATION
# =============================================================================

options = {
    1: {
        "img1_path": "../data/dataInput/53_Mbodj_Khalifa.jpg",
        "img2_path": "../data/dataInput/54_Veillet_Anthony.jpg",
        "pts1_path": "../data/dataInput/53_Mbodj_Khalifa.txt",
        "pts2_path": "../data/dataInput/54_Veillet_Anthony.txt",
        "output_dir": "../dataOutput/frames_1",
        "video_output": "../dataOutput/morphing_1.mp4",
    },
    2: {
        "img1_path": "../data/dataInput/Objet_1.jpg",
        "img2_path": "../data/dataInput/Objet_2.jpg",
        "pts1_path": "../data/dataInput/Objet_1.txt",
        "pts2_path": "../data/dataInput/Objet_2.txt",
        "output_dir": "../dataOutput/frames_2",
        "video_output": "../dataOutput/morphing_2.mp4",
    },
    3: {
        "img1_path": "../data/dataInput/perso1_img1.jpg",
        "img2_path": "../data/dataInput/perso1_img2.jpg",
        "pts1_path": "../data/dataInput/perso1_img1.txt",
        "pts2_path": "../data/dataInput/perso1_img2.txt",
        "output_dir": "../dataOutput/frames_3",
        "video_output": "../dataOutput/morphing_3.mp4",
    },
    4: {
        "img1_path": "../data/dataInput/perso2_img1.jpg",
        "img2_path": "../data/dataInput/perso2_img2.jpg",
        "pts1_path": "../data/dataInput/perso2_img1.txt",
        "pts2_path": "../data/dataInput/perso2_img2.txt",
        "output_dir": "../dataOutput/frames_4",
        "video_output": "../dataOutput/morphing_4.mp4",
    }
}

num_frames = 100
fps = 25

test = int(input(
    "Quelle métamorphose faire:\n"
    "1) Visage étudiant\n"
    "2) Objets/Animaux\n"
    "3) Animation perso 1\n"
    "4) Animation perso 2\n"
    "Entrez le choix entre 1 et 4: "
))

if test not in options:
    raise ValueError("Choix invalide. Entrez un nombre entre 1 et 4.")

config = options[test]

img1_path = config["img1_path"]
img2_path = config["img2_path"]
pts1_path = config["pts1_path"]
pts2_path = config["pts2_path"]
output_dir = config["output_dir"]
video_output = config["video_output"]


def generate_frames(img1, img2, pts1, pts2, tri, num_frames, output_dir):
    """
    Génère les trames de la métamorphose et les sauvegarde en PNG.

    Le warp_frac et dissolve_frac varient linéairement de 0 à 1 sur
    l'ensemble des trames. L'astuce suggérée dans l'énoncé (augmenter
    warp_frac avant dissolve_frac) est implémentée avec un décalage :
    warp_frac avance légèrement plus vite au début.
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


# =============================================================================
# EXÉCUTION
# =============================================================================

# Charger les images
print("Chargement des images...")
img1 = load_image(img1_path)
img2 = load_image(img2_path)

assert img1.shape == img2.shape, \
    f"Les images doivent avoir les mêmes dimensions! img1={img1.shape}, img2={img2.shape}"

# Charger les points d'intérêt
print("Chargement des points d'intérêt...")
pts1 = load_points(pts1_path)
pts2 = load_points(pts2_path)

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
generate_frames(img1, img2, pts1, pts2, tri, num_frames, output_dir)

# Créer la vidéo
Path(video_output).parent.mkdir(parents=True, exist_ok=True)
create_video(output_dir, video_output, fps)