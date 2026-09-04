import os
import re  # ← AJOUT : pour les expressions régulières

# Fonction pour formater le nom du fichier en "xxminxxs" ou "xxhxxminxxs"
def format_time(file_name):
    name_without_extension = os.path.splitext(file_name)[0]  # Retirer l'extension
    
    # Gestion spéciale pour le fichier "cover"
    if name_without_extension == "cover":
        return "cover"
    
    parts = name_without_extension.split('_')  # Séparer les parties
    
    # Extraire uniquement les chiffres de chaque partie (ignorer les lettres)
    clean_parts = []
    for part in parts:
        # Garder uniquement les chiffres (ex: "40b" → "40")
        digits = re.sub(r'\D', '', part)  # \D = tout ce qui n'est pas un chiffre
        if digits:  # Si on a trouvé des chiffres
            clean_parts.append(digits)
    
    # Maintenant, formater avec les parties nettoyées
    if len(clean_parts) == 2:
        minutes, seconds = clean_parts
        return f"{minutes}min{seconds}s"
    elif len(clean_parts) == 3:
        hours, minutes, seconds = clean_parts
        return f"{hours}h{minutes}min{seconds}s"
    else:
        # Si le format ne correspond pas, retourner le nom original nettoyé
        return '_'.join(clean_parts) if clean_parts else name_without_extension

# Fonction pour lister les images et générer les lignes HTML dans un fichier texte
def generate_image_list_txt(directory_path, output_file):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    
    with open(output_file, 'w', encoding='utf-8') as f:
        files = os.listdir(directory_path)
        files.sort(key=lambda x: (x != 'cover', x))
        
        for file_name in files:
            if any(file_name.endswith(ext) for ext in image_extensions):
                formatted_time = format_time(file_name)
                image_path = os.path.join(directory_path, file_name).replace("\\", "/")

                # Générer la ligne HTML avec 3 colonnes
                line = f"""
                <tr>
                    <td><img src="{image_path}" class="video-thumbnail"></td>
                    <td>{formatted_time}</td>
                    <td></td>
                </tr>
                """
                f.write(line + "\n")

# Exemple d'utilisation
directory = './images/sources/art_soustraction'
output_file = 'output_table.txt'

generate_image_list_txt(directory, output_file)
print(f"Les lignes HTML ont été générées dans le fichier {output_file}.")