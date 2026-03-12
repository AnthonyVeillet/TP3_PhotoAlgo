from __future__ import annotations

from datetime import datetime
from pathlib import Path


# =========================
# Config
# =========================

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_HTML = SCRIPT_DIR / "rapport.html"

TITLE = "🎭 Rapport TP3 - <votre nom>"
COURSE_FOOTER = "Photographie algorithmique — TP3 | Métamorphose de visages"

# Métamorphose 1 — Visage (N-1 → N)
IMG_M1_SRC = "53_Mbodj_Khalifa.jpg"
IMG_M1_DST = "54_Veillet_Anthony.jpg"
VID_M1 = "morphing_1.mp4"

# Métamorphose 2 — Objets / Animaux
IMG_M2_SRC = "Objet_1.jpg"
IMG_M2_DST = "Objet_2.jpg"
VID_M2 = "morphing_2.mp4"

# Métamorphose 3 — Photos personnelles #1
IMG_M3_SRC = "perso1_img1.jpg"
IMG_M3_DST = "perso1_img2.jpg"
VID_M3 = "morphing_3.mp4"

# Métamorphose 4 — Photos personnelles #2
IMG_M4_SRC = "perso2_img1.jpg"
IMG_M4_DST = "perso2_img2.jpg"
VID_M4 = "morphing_4.mp4"


# =============================================================================
# TODO — ÉCRIS TES RÉPONSES ICI (entre les triple guillemets)
# =============================================================================

# TODO: Décris brièvement ton algorithme de métamorphose
TEXTE_ALGORITHME = """
L'algorithme de métamorphose fonctionne en plusieurs étapes. D'abord, les points de correspondance sont sélectionnés manuellement sur les deux images avec selectpoints.py,
puis des points de bordure sont ajoutés aux coins et bords de l'image pour couvrir l'arrière-plan. Une triangulation de Delaunay est ensuite calculée une seule fois sur la
moyenne des deux ensembles de points afin de minimiser la déformation des triangles. Pour chaque trame, des points intermédiaires sont calculés selon warp_frac, puis pour
chaque triangle, la transformation affine inverse est calculée manuellement (sans skimage.transform) afin de retrouver les coordonnées correspondantes dans les images
originales. L'interpolation des couleurs est effectuée avec RectBivariateSpline, et le fondu entre les deux images est pondéré par dissolve_frac. Finalement, warp_frac
avance légèrement avant dissolve_frac pour aligner les formes avant de mélanger les couleurs, tel que recommandé dans l'énoncé.
"""

# TODO: Discussion sur la métamorphose visage (N-1 → N)
TEXTE_MORPH1 = """
La métamorphose du visage donne un résultat globalement réussi et la transition entre les deux personnes reste fluide sur l’ensemble de la séquence.
Les points de correspondance semblent bien placés au niveau des yeux, du nez, de la bouche et du contour du visage, ce qui aide à conserver une bonne cohérence visuelle.
Les problèmes sont surtout visibles au front, dans les cheveux, sur les épaules et légèrement dans le vêtement, surtout dans les images intermédiaires où les deux visages se superposent.
L’arrière-plan se déforme aussi un peu près du miroir et des contours du mur, mais cela reste secondaire par rapport au visage.
Dans l’ensemble, le résultat est à la hauteur de mes attentes et montre que l’algorithme fonctionne bien lorsque les traits principaux des deux visages sont correctement alignés.
"""

# TODO: Discussion sur la métamorphose objets / animaux
TEXTE_MORPH2 = """
La métamorphose de la banane vers la pomme fonctionne bien et la transition reste facile à suivre du début à la fin.
J’ai choisi ce test pour utiliser deux formes très différentes et voir comment l’algorithme allait réagir malgré cette grande différence de silhouette.
Les problèmes sont surtout visibles aux extrémités et près de la tige, où certaines images intermédiaires montrent des déformations plus marquées.
Malgré cela, le résultat reste intéressant et démontre que l’algorithme peut réussir une métamorphose même entre deux objets ayant une structure très différente.
"""

# TODO: Discussion sur les photos personnelles #1
TEXTE_MORPH3 = """
La métamorphose entre le crâne et le Memoji donne un résultat visuellement intéressant, car la transition entre deux styles très différents reste progressive et facile à suivre.
J’ai choisi ce test pour voir comment l’algorithme se comporterait entre deux visuels stylisés ayant des proportions faciales très différentes.
Les problèmes sont surtout visibles autour des yeux, de la bouche, de la mâchoire et du haut de la tête, où les formes changent beaucoup dans les images intermédiaires.
Malgré cela, le résultat final est convaincant et il est globalement à la hauteur de mes attentes pour une métamorphose entre deux images aussi différentes.
"""

# TODO: Discussion sur les photos personnelles #2
TEXTE_MORPH4 = """
La métamorphose du PCB vierge vers le PCB avec composantes donne un résultat propre et naturel, puisque les deux images ont la même taille générale et le même cadrage.
J’ai choisi ce test pour vérifier comment l’algorithme se comporte avec deux objets de même grosseur, mais avec des différences surtout visibles dans les détails à la surface.
Les images de départ ont été générées avec ChatGPT, ce qui m’a permis d’obtenir deux visuels très semblables et bien contrôlés pour ce type d’essai.
Ce cas est à la hauteur de mes attentes et fonctionne bien, car la structure principale reste la même et seules les composantes apparaissent progressivement avec peu d’artefacts.
"""

# TODO: Colle tes 2 prompts ChatGPT
TEXTE_PROMPT1 = """
Yo
1) Analyse et comprend le travail que je dois faire en Python, soit TP3.pdf
2) J'ai déjà fait la section de ma photo pour placer les points demandé
3) Voici le code selectpoints.py, analyse et comprend le, il poura nous etre utile
4) Fait moi un plan détaillé de ce que je vais devoir faire ainsi qu'un plan des différents fichiers que je vasi devoir créer et faire. En d'autres mots, fait moi un squelette de ce que je vais devoir faire incluant les nom de variables et fonctions.
5) Je veux que tu agiste comme un tuteur pour favoriser mon apprentissage, donc ne me donne pas le code complet des différents fichier. Aussi, s'il te manque d'informations pour en compléter, dit moi le et ajoute des zones TODO expliquant quoi faire. De plus, pas besoin de faire la documentation Doxygen.
6) Donne moi une section commentaire que je vais mettre dans les fonctions qui expliquera se que fait cette fonction.
7) Ne t'occupe pas de la section des questions à répondre dans le rapport, pour l'instant.
8) Avant de donner ta réponse, analyse la pour etre certain qu'elle répond à mes critères et aux attentes de TP3.pdf. Tu n'as aucune limite de temps pour répondre. Mentionne  moi s'il te manque des informations où si quelque chose est pas clair

"""

TEXTE_PROMPT2 = """
Yo, garde ce code, mais est-ce possible qu'il affiche au terminal s'il a bien trouver les fichiers et si les fichier de output son valide et existant:

options = {
    1: {
        "img1_path": "../data/dataInput/14_Lebel_Philippe.jpg",
        "img2_path": "../data/dataInput/54_Veillet_Anthony.jpg",
        "pts1_path": "../data/dataInput/14_Lebel_Philippe.txt",
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
"""


# =========================
# Helpers HTML
# =========================

def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def pair_two(img_a: str, cap_a: str, img_b: str, cap_b: str) -> str:
    ca = _escape(cap_a)
    cb = _escape(cap_b)
    return f"""
    <div class="comparison-images">
        <div class="comparison-image-item" onclick="openLightbox(this.querySelector('img'))">
            <img src="{img_a}" alt="{ca}" data-fullsize="{img_a}">
            <div class="comparison-image-label">{ca}</div>
        </div>
        <div class="comparison-image-item" onclick="openLightbox(this.querySelector('img'))">
            <img src="{img_b}" alt="{cb}" data-fullsize="{img_b}">
            <div class="comparison-image-label">{cb}</div>
        </div>
    </div>
    """


def video_block(video_src: str, caption: str) -> str:
    cap = _escape(caption)
    return f"""
    <div class="video-container">
        <video controls loop>
            <source src="{video_src}" type="video/mp4">
            Votre navigateur ne supporte pas la lecture vidéo.
        </video>
        <p class="figure-caption">{cap}</p>
    </div>
    """


def text_block(title: str, content: str) -> str:
    """Bloc de texte statique avec le contenu déjà rempli (visible par le correcteur)."""
    t = _escape(title)
    # Convertir les sauts de ligne en <br> et les espaces en HTML
    content_html = _escape(content.strip()).replace("\n", "<br>")
    return f"""
    <div class="text-block">
        <div class="text-block-title">📝 {t}</div>
        <div class="text-content">{content_html}</div>
    </div>
    """


def section(title: str, inner: str) -> str:
    return f"""
    <section class="image-section">
        <h2>{_escape(title)}</h2>
        {inner}
    </section>
    """


def morph_block(subtitle: str, img_src: str, cap_src: str,
                img_dst: str, cap_dst: str, video: str, cap_video: str,
                discussion_title: str, discussion_text: str) -> str:
    block = ""
    block += f"<h3>{_escape(subtitle)}</h3>"
    block += f"""
    <div class="comparison-pair">
        <div class="comparison-pair-title">Images source et cible</div>
        {pair_two(img_src, cap_src, img_dst, cap_dst)}
    </div>
    """
    block += video_block(video, cap_video)
    block += text_block(discussion_title, discussion_text)
    return block


# =========================
# Construction du HTML
# =========================

now = datetime.now().strftime("%d %B %Y à %H:%M")

# --- Section 1 : Description de l'algorithme
algo = text_block("Description de l'algorithme", TEXTE_ALGORITHME)

# --- Section 2 : Métamorphose visage (N-1 → N)
m1 = morph_block(
    "Visage : Mbodj Khalifa (#53) → Veillet Anthony (#54)",
    IMG_M1_SRC, "Image source — 53_Mbodj_Khalifa",
    IMG_M1_DST, "Image cible — 54_Veillet_Anthony",
    VID_M1, "Métamorphose visage (100 trames, 4s à 25fps)",
    "Discussion", TEXTE_MORPH1,
)

# --- Section 3 : Métamorphose objets / animaux
m2 = morph_block(
    "Objets / Animaux",
    IMG_M2_SRC, "Objet 1",
    IMG_M2_DST, "Objet 2",
    VID_M2, "Métamorphose objets / animaux",
    "Discussion", TEXTE_MORPH2,
)

# --- Section 4 : Photos personnelles #1
m3 = morph_block(
    "Photos personnelles #1",
    IMG_M3_SRC, "Photo personnelle 1 — source",
    IMG_M3_DST, "Photo personnelle 1 — cible",
    VID_M3, "Métamorphose photos personnelles #1",
    "Discussion", TEXTE_MORPH3,
)

# --- Section 5 : Photos personnelles #2
m4 = morph_block(
    "Photos personnelles #2",
    IMG_M4_SRC, "Photo personnelle 2 — source",
    IMG_M4_DST, "Photo personnelle 2 — cible",
    VID_M4, "Métamorphose photos personnelles #2",
    "Discussion", TEXTE_MORPH4,
)

# --- Section 6 : Prompts ChatGPT
prompts = ""
prompts += text_block("Prompt #1 utilisé avec ChatGPT", TEXTE_PROMPT1)
prompts += text_block("Prompt #2 utilisé avec ChatGPT", TEXTE_PROMPT2)


# =========================
# Template HTML complet
# =========================

html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_escape(TITLE)}</title>

  <style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&family=Fira+Code:wght@400;500&display=swap');
    * {{ box-sizing: border-box; }}

    body {{
      font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      color: #e8e8e8;
      min-height: 100vh;
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 30px 20px;
    }}

    header {{
      text-align: center;
      padding: 40px 0;
      border-bottom: 2px solid rgba(255,255,255,0.1);
      margin-bottom: 40px;
    }}

    h1 {{
      font-size: 2.5em;
      font-weight: 700;
      margin: 0 0 10px 0;
      text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}

    .date-badge {{
      display: inline-block;
      background: rgba(255,255,255,0.1);
      padding: 8px 20px;
      border-radius: 20px;
      margin-top: 12px;
      font-size: 0.9em;
      color: #b0b0b0;
    }}

    .image-section {{
      background: rgba(255,255,255,0.05);
      backdrop-filter: blur(10px);
      border-radius: 16px;
      padding: 30px;
      margin-bottom: 40px;
      border: 1px solid rgba(255,255,255,0.1);
      box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }}

    .image-section h2 {{
      color: #778da9;
      font-size: 1.6em;
      margin: 0 0 25px 0;
      padding-bottom: 15px;
      border-bottom: 2px solid rgba(119, 141, 169, 0.25);
    }}

    h3 {{
      color: #e0e1dd;
      font-size: 1.3em;
      margin: 26px 0 14px 0;
    }}

    .figure-caption {{
      margin-top: 10px;
      font-style: italic;
      color: #a0a0a0;
      font-size: 0.9em;
    }}

    .comparison-pair {{
      background: rgba(0,0,0,0.25);
      border-radius: 12px;
      padding: 18px;
      border: 1px solid rgba(255,255,255,0.08);
      margin: 16px 0;
    }}

    .comparison-pair-title {{
      text-align: center;
      color: #fff;
      font-size: 1.05em;
      font-weight: 600;
      margin-bottom: 12px;
      padding-bottom: 10px;
      border-bottom: 2px solid rgba(255,255,255,0.15);
    }}

    .comparison-images {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }}

    .comparison-image-item {{
      position: relative;
      border-radius: 10px;
      overflow: hidden;
      background: rgba(0,0,0,0.2);
      cursor: pointer;
      transition: transform 0.15s, box-shadow 0.15s;
    }}

    .comparison-image-item:hover {{
      transform: translateY(-3px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.5);
    }}

    .comparison-image-item img {{
      width: 100%;
      height: auto;
      display: block;
    }}

    .comparison-image-label {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
      color: #fff;
      padding: 12px 8px 8px;
      font-size: 0.85em;
      text-align: center;
      font-weight: 500;
    }}

    /* ---- Vidéo ---- */
    .video-container {{
      text-align: center;
      margin: 20px 0;
      padding: 15px;
      background: rgba(0,0,0,0.2);
      border-radius: 12px;
    }}

    .video-container video {{
      max-width: 80%;
      max-height: 520px;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }}

    /* ---- Bloc de texte (réponses) ---- */
    .text-block {{
      background: rgba(0,0,0,0.25);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px;
      padding: 18px;
      margin: 18px 0 0 0;
    }}

    .text-block-title {{
      font-weight: 700;
      color: #cbd5e1;
      margin-bottom: 10px;
    }}

    .text-content {{
      color: #d0d0d0;
      font-size: 1em;
      line-height: 1.7;
    }}

    footer {{
      text-align: center;
      padding: 30px;
      color: #777;
      font-size: 0.95em;
    }}

    /* Lightbox */
    .lightbox {{
      display: none;
      position: fixed;
      z-index: 9999;
      left: 0; top: 0;
      width: 100%; height: 100%;
      background-color: rgba(0,0,0,0.92);
      animation: fadeIn 0.2s;
    }}

    .lightbox.active {{
      display: flex;
      align-items: center;
      justify-content: center;
    }}

    .lightbox-content {{
      max-width: 95vw;
      max-height: 95vh;
      padding: 18px;
    }}

    .lightbox-content img {{
      max-width: 100%;
      max-height: 95vh;
      object-fit: contain;
      border-radius: 10px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.8);
    }}

    .lightbox-close {{
      position: absolute;
      top: 16px;
      right: 30px;
      color: #fff;
      font-size: 44px;
      font-weight: bold;
      cursor: pointer;
      transition: color 0.2s;
      user-select: none;
    }}

    .lightbox-close:hover {{
      color: #ffc107;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}

    @media (max-width: 900px) {{
      .comparison-images {{ grid-template-columns: 1fr; }}
      .video-container video {{ max-width: 100%; }}
    }}
  </style>
</head>

<body>
  <div id="lightbox" class="lightbox" onclick="closeLightbox(event)">
    <span class="lightbox-close">&times;</span>
    <div class="lightbox-content">
      <img id="lightbox-img" src="" alt="">
    </div>
  </div>

  <div class="container">
    <header>
      <h1>{_escape(TITLE)}</h1>
      <div class="date-badge">Généré le {now}</div>
    </header>

    {section("Partie 1 — Description de l'algorithme", algo)}
    {section("Partie 2 — Métamorphose visage (N-1 → N)", m1)}
    {section("Partie 3 — Métamorphose objets / animaux", m2)}
    {section("Partie 4 — Photos personnelles #1", m3)}
    {section("Partie 5 — Photos personnelles #2", m4)}
    {section("Partie 6 — Prompts ChatGPT utilisés", prompts)}

    <footer>
      <p>{_escape(COURSE_FOOTER)}</p>
    </footer>
  </div>

  <script>
    function openLightbox(img) {{
      const lightbox = document.getElementById('lightbox');
      const lightboxImg = document.getElementById('lightbox-img');
      const fullSizeSrc = img.getAttribute('data-fullsize') || img.src;
      lightboxImg.src = fullSizeSrc;
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function closeLightbox(event) {{
      const lightbox = document.getElementById('lightbox');
      if (event.target === lightbox || event.target.classList.contains('lightbox-close')) {{
        lightbox.classList.remove('active');
        document.body.style.overflow = 'auto';
      }}
    }}

    document.addEventListener('keydown', function(event) {{
      if (event.key === 'Escape') {{
        const lightbox = document.getElementById('lightbox');
        lightbox.classList.remove('active');
        document.body.style.overflow = 'auto';
      }}
    }});
  </script>
</body>
</html>
"""

# =========================
# Génération du fichier
# =========================

OUTPUT_HTML.write_text(html, encoding="utf-8")
print(f"[OK] Rapport généré: {OUTPUT_HTML.resolve()}")