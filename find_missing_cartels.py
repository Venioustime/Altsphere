import os
import re
from pathlib import Path

def find_missing_cartels(directory_path="."):
    """
    Parcourt tous les fichiers HTML d'un répertoire et liste les images sans cartel
    """
    missing_cartels = []
    
    # Parcourir tous les fichiers HTML du répertoire
    for file_path in Path(directory_path).glob("**/*.html"):
        print(f"Analyse de {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Chercher tous les blocs d'images dans les tables
                # Pattern pour capturer chaque ligne du tableau d'images
                pattern = r'<tr>\s*<td><img src="([^"]+)"[^>]*></td>\s*<td>([^<]+)</td>\s*<td>([^<]*)</td>\s*</tr>'
                
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    image_src, timecode, cartel = match
                    # Si le cartel est vide ou ne contient que des espaces
                    if not cartel.strip():
                        missing_cartels.append({
                            'file': file_path.name,
                            'image_src': image_src,
                            'timecode': timecode.strip()
                        })
                        
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
    
    return missing_cartels

def save_to_file(missing_cartels, output_file="cartels_manquants.txt"):
    """
    Sauvegarde la liste des cartels manquants dans un fichier texte
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("LISTE DES CARTELS MANQUANTS\n")
        file.write("=" * 50 + "\n\n")
        
        current_file = None
        count = 0
        
        for item in missing_cartels:
            if item['file'] != current_file:
                current_file = item['file']
                file.write(f"\nFICHIER: {current_file}\n")
                file.write("-" * 40 + "\n")
            
            count += 1
            file.write(f"{count}. Timecode: {item['timecode']}\n")
            file.write(f"   Image: {item['image_src']}\n")
            file.write(f"   Cartel: [À COMPLÉTER]\n")
            file.write("\n")
    
    return count

def main():
    # Demander le répertoire à analyser
    directory = input("Entrez le chemin du répertoire contenant les fichiers HTML (tapez Entrée pour le répertoire courant): ").strip()
    if not directory:
        directory = "."
    
    if not os.path.exists(directory):
        print("Le répertoire spécifié n'existe pas!")
        return
    
    print("Recherche des cartels manquants...")
    missing = find_missing_cartels(directory)
    
    if not missing:
        print("Aucun cartel manquant trouvé!")
        return
    
    print(f"Trouvé {len(missing)} cartels manquants!")
    
    # Sauvegarder dans un fichier
    count = save_to_file(missing)
    print(f"Liste sauvegardée dans 'cartels_manquants.txt' ({count} éléments)")
    
    # Afficher un aperçu
    print("\nAperçu des 5 premiers cartels manquants:")
    print("-" * 50)
    for i, item in enumerate(missing[:5]):
        print(f"{i+1}. Fichier: {item['file']}")
        print(f"   Timecode: {item['timecode']}")
        print(f"   Image: {item['image_src']}")
        print()

if __name__ == "__main__":
    main()