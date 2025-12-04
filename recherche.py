import os
import re
from pathlib import Path

def search_in_cartels(directory_path=".", search_term=""):
    """
    Parcourt tous les fichiers HTML d'un répertoire et recherche un terme dans les cartels
    """
    results = []
    
    # Compiler le terme de recherche (insensible à la casse)
    pattern = re.compile(re.escape(search_term), re.IGNORECASE)
    
    # Parcourir tous les fichiers HTML du répertoire
    for file_path in Path(directory_path).glob("**/*.html"):
        print(f"Analyse de {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Chercher tous les blocs d'images dans les tables
                html_pattern = r'<tr>\s*<td><img src="([^"]+)"[^>]*></td>\s*<td>([^<]+)</td>\s*<td>([^<]*)</td>\s*</tr>'
                
                matches = re.findall(html_pattern, content, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    image_src, timecode, cartel = match
                    cartel_text = cartel.strip()
                    
                    # Rechercher le terme dans le cartel
                    if cartel_text and pattern.search(cartel_text):
                        results.append({
                            'file': file_path.name,
                            'file_path': str(file_path),
                            'image_src': image_src,
                            'timecode': timecode.strip(),
                            'cartel': cartel_text,
                            'match': pattern.search(cartel_text).group()
                        })
                        
        except Exception as e:
            print(f"Erreur lors de la lecture de {file_path}: {e}")
    
    return results

def save_search_results(results, search_term, output_file="recherche_cartels.txt"):
    """
    Sauvegarde les résultats de la recherche dans un fichier texte
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"RECHERCHE DU TERME : '{search_term}'\n")
        file.write("=" * 80 + "\n\n")
        
        file.write(f"Nombre total d'occurrences trouvées : {len(results)}\n\n")
        
        if not results:
            file.write("Aucun résultat trouvé.\n")
            return
        
        # Grouper les résultats par fichier
        results_by_file = {}
        for item in results:
            if item['file'] not in results_by_file:
                results_by_file[item['file']] = []
            results_by_file[item['file']].append(item)
        
        # Écrire les résultats par fichier
        for filename, file_results in results_by_file.items():
            file.write(f"\nFICHIER: {filename}\n")
            file.write("-" * 80 + "\n")
            
            for i, item in enumerate(file_results, 1):
                file.write(f"{i}. Timecode: {item['timecode']}\n")
                file.write(f"   Image: {item['image_src']}\n")
                
                # Mettre en évidence le terme trouvé dans le cartel
                cartel_text = item['cartel']
                match_text = item['match']
                
                # Remplacer le terme par sa version en majuscule pour la mise en évidence
                highlighted_cartel = re.sub(
                    re.escape(match_text), 
                    f"**{match_text.upper()}**", 
                    cartel_text, 
                    flags=re.IGNORECASE
                )
                
                file.write(f"   Cartel: {highlighted_cartel}\n")
                file.write("\n")
    
    return len(results)

def main():
    # Demander le répertoire à analyser
    directory = input("Entrez le chemin du répertoire contenant les fichiers HTML (tapez Entrée pour le répertoire courant): ").strip()
    if not directory:
        directory = "."
    
    if not os.path.exists(directory):
        print("Le répertoire spécifié n'existe pas!")
        return
    
    # Demander le terme à rechercher
    search_term = input("Entrez le terme à rechercher dans les cartels: ").strip()
    if not search_term:
        print("Vous devez entrer un terme à rechercher!")
        return
    
    print(f"\nRecherche du terme '{search_term}' dans les cartels...")
    results = search_in_cartels(directory, search_term)
    
    if not results:
        print(f"\nAucune occurrence du terme '{search_term}' trouvée dans les cartels.")
        
        # Demander si on veut quand même créer un fichier de rapport vide
        create_empty = input("\nVoulez-vous créer un fichier de rapport vide? (o/n): ").strip().lower()
        if create_empty == 'o':
            with open("recherche_cartels.txt", 'w', encoding='utf-8') as file:
                file.write(f"RECHERCHE DU TERME : '{search_term}'\n")
                file.write("=" * 80 + "\n\n")
                file.write("Aucune occurrence trouvée.\n")
            print("Fichier 'recherche_cartels.txt' créé avec un rapport vide.")
        return
    
    print(f"\nTrouvé {len(results)} occurrence(s) du terme '{search_term}' dans les cartels.")
    
    # Afficher un aperçu des résultats
    print("\nAperçu des 5 premiers résultats:")
    print("-" * 80)
    
    for i, item in enumerate(results[:5], 1):
        print(f"{i}. Fichier: {item['file']}")
        print(f"   Timecode: {item['timecode']}")
        print(f"   Image: {item['image_src']}")
        
        # Mettre en évidence le terme dans l'affichage console
        cartel_text = item['cartel']
        match_text = item['match']
        highlighted = re.sub(
            re.escape(match_text), 
            f"\033[1;31m{match_text}\033[0m", 
            cartel_text, 
            flags=re.IGNORECASE
        )
        
        print(f"   Cartel: {highlighted}")
        print()
    
    # Sauvegarder les résultats
    count = save_search_results(results, search_term)
    print(f"\nRésultats sauvegardés dans 'recherche_cartels.txt' ({count} occurrence(s) trouvée(s))")
    
    # Option pour afficher plus de résultats
    if len(results) > 5:
        show_more = input(f"\nIl y a {len(results)} résultats au total. Voulez-vous tous les afficher? (o/n): ").strip().lower()
        if show_more == 'o':
            print("\n" + "=" * 80)
            for i, item in enumerate(results, 1):
                print(f"{i}. Fichier: {item['file']}")
                print(f"   Timecode: {item['timecode']}")
                print(f"   Image: {item['image_src']}")
                
                cartel_text = item['cartel']
                match_text = item['match']
                highlighted = re.sub(
                    re.escape(match_text), 
                    f"\033[1;31m{match_text}\033[0m", 
                    cartel_text, 
                    flags=re.IGNORECASE
                )
                
                print(f"   Cartel: {highlighted}")
                print()

if __name__ == "__main__":
    main()