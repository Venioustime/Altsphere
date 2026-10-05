import os
import re

ROOT = "."  # dossier racine du site

# Marqueur pour ne pas ajouter le script plusieurs fois
LAZY_TAG = '<script src="lazy-images.js" defer></script>'

for dossier, _, fichiers in os.walk(ROOT):
    # Ignorer les dossiers inutiles
    if any(skip in dossier for skip in ['.git', 'node_modules']):
        continue

    for fichier in fichiers:
        if not fichier.lower().endswith(".html"):
            continue

        chemin = os.path.join(dossier, fichier)
        with open(chemin, "r", encoding="utf-8") as f:
            contenu = f.read()
        original = contenu

        # 1) Réparer les balises <script data-src= -> <script src=
        contenu = re.sub(r'<script\s+data-src=', '<script src=', contenu)

        # 2) Réparer au cas où d'autres data-src auraient été mal appliqués
        #    sur <link>, <iframe>, <source> (au cas où)
        contenu = re.sub(r'<link\s+data-src=', '<link src=', contenu)
        contenu = re.sub(r'<iframe\s+data-src=', '<iframe src=', contenu)
        contenu = re.sub(r'<source\s+data-src=', '<source src=', contenu)

        # 3) Ajouter lazy-images.js si absent
        if 'lazy-images.js' not in contenu:
            if '</body>' in contenu:
                contenu = contenu.replace(
                    '</body>',
                    f'    {LAZY_TAG}\n</body>'
                )
            else:
                # Fichier sans </body> (par ex. head.txt partiel) → on ignore
                pass

        if contenu != original:
            with open(chemin, "w", encoding="utf-8") as f:
                f.write(contenu)
            print(f"✅ Corrigé : {chemin}")

print("\nTerminé.")
