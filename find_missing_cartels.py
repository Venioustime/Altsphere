import os
import re
from pathlib import Path

def find_missing_cartels(directory_path="."):
    """
    Parcourt tous les fichiers HTML d'un répertoire et liste les images sans cartel
    """
    files_data = []
    
    # Parcourir tous les fichiers HTML du répertoire
    for file_path in Path(directory_path).glob("**/*.html"):
        print(f"Analyse de {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Chercher tous les blocs d'images dans les tables
                pattern = r'<tr>\s*<td><img src="([^"]+)"[^>]*></td>\s*<td>([^<]+)</td>\s*<td>([^<]*)</td>\s*</tr>'
                
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                
                missing_cartels = []
                total_cartels = len(matches)
                
                for match in matches:
                    image_src, timecode, cartel = match
                    # Si le cartel est vide ou ne contient que des espaces
                    if not cartel.strip():
                        missing_cartels.append({
                            'image_src': image_src,
                            'timecode': timecode.strip()
                        })
                
                if total_cartels > 0 and missing_cartels:
                    files_data.append({
                        'file': file_path.name,
                        'file_path': str(file_path),
                        'missing_count': len(missing_cartels),
                        'missing_cartels': missing_cartels,
                        'filled_percentage': ((total_cartels - len(missing_cartels)) / total_cartels * 100)
                    })
                        
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
    
    return files_data

def save_to_file(files_data, output_file="cartels_manquants.txt"):
    """
    Sauvegarde la liste des cartels manquants dans un fichier texte
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("CARTELS MANQUANTS - RAPPORT\n")
        file.write("=" * 60 + "\n\n")
        
        # Calcul du total global de cartels manquants
        total_missing = sum(item['missing_count'] for item in files_data)
        
        # Écriture du total de cartels manquants
        file.write(f"TOTAL DE CARTELS VIDES RESTANTS : {total_missing}\n\n")
        
        # Trier les fichiers par pourcentage de remplissage (croissant)
        sorted_files_data = sorted(files_data, key=lambda x: x['filled_percentage'])
        
        # Écriture des pourcentages par page
        file.write("POURCENTAGES DE CARTELS REMPLIS PAR PAGE (trié par ordre croissant) :\n")
        file.write("-" * 60 + "\n")
        
        for item in sorted_files_data:
            file.write(f"{item['file']:<30} : {item['filled_percentage']:>6.1f}%  ({item['missing_count']} cartels vides)\n")
        
        file.write("-" * 60 + "\n\n")
        
        # Écriture des détails des cartels manquants
        file.write("DÉTAILS DES CARTELS VIDES PAR PAGE :\n\n")
        
        count = 0
        
        for item in sorted_files_data:
            if item['missing_count'] > 0:
                file.write(f"FICHIER: {item['file']} ({item['filled_percentage']:.1f}% de remplissage)\n")
                file.write("-" * 60 + "\n")
                
                for cartel in item['missing_cartels']:
                    count += 1
                    file.write(f"{count}. Timecode: {cartel['timecode']}\n")
                    file.write(f"   Image: {cartel['image_src']}\n")
                    file.write(f"   Cartel: [À COMPLÉTER]\n")
                    file.write("\n")
                
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
    files_data = find_missing_cartels(directory)
    
    if not files_data:
        print("Aucun cartel manquant trouvé!")
        return
    
    total_missing = sum(item['missing_count'] for item in files_data)
    
    print(f"\nTOTAL DE CARTELS VIDES RESTANTS : {total_missing}")
    
    # Trier les fichiers par pourcentage de remplissage (croissant)
    sorted_files_data = sorted(files_data, key=lambda x: x['filled_percentage'])
    
    # Afficher les pourcentages par page
    print("\nPOURCENTAGES DE CARTELS REMPLIS PAR PAGE (trié par ordre croissant) :")
    print("-" * 60)
    for item in sorted_files_data:
        print(f"{item['file']:<30} : {item['filled_percentage']:>6.1f}%  ({item['missing_count']} cartels vides)")
    print("-" * 60)
    
    # Sauvegarder dans un fichier
    count = save_to_file(files_data)
    print(f"\nRapport sauvegardé dans 'cartels_manquants.txt'")
    
    # Afficher un aperçu
    print("\nAperçu des 5 premiers cartels manquants:")
    print("-" * 50)
    
    display_count = 0
    for item in sorted_files_data:
        for cartel in item['missing_cartels'][:5 - display_count]:
            display_count += 1
            print(f"{display_count}. Fichier: {item['file']} ({item['filled_percentage']:.1f}%)")
            print(f"   Timecode: {cartel['timecode']}")
            print(f"   Image: {cartel['image_src']}")
            print()
            if display_count >= 5:
                break
        if display_count >= 5:
            break

if __name__ == "__main__":
    main()