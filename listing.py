import os

# Fonction pour formater le nom du fichier en "xxminxxs"
def format_time(file_name):
    name_without_extension = os.path.splitext(file_name)[0]  # Retirer l'extension
    minutes, seconds = name_without_extension.split('_')  # Séparer les minutes et secondes
    return f"{minutes}min{seconds}s"

# Fonction pour lister les images et générer les lignes HTML dans un fichier texte
def generate_image_list_txt(directory_path, output_file):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']  # Extensions d'images autorisées
    
    # Ouvrir le fichier de sortie en mode écriture
    with open(output_file, 'w', encoding='utf-8') as f:
        # Lister tous les fichiers dans le répertoire donné
        for file_name in os.listdir(directory_path):
            # Vérifier si le fichier a une extension d'image
            if any(file_name.endswith(ext) for ext in image_extensions):
                formatted_time = format_time(file_name)
                image_path = os.path.join(directory_path, file_name).replace("\\", "/")  # Chemin complet

                # Générer la ligne HTML
                line = f"""
                <tr>
                    <td><img src="{image_path}" class="video-thumbnail"></td>
                    <td>{formatted_time}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>
                """
                # Écrire la ligne dans le fichier texte
                f.write(line + "\n")

# Exemple d'utilisation
directory = './images/sources/all_seeing_eye_video'  # Chemin vers le dossier d'images
output_file = 'output_table.txt'  # Fichier texte de sortie

# Appeler la fonction pour générer le fichier texte
generate_image_list_txt(directory, output_file)

print(f"Les lignes HTML ont été générées dans le fichier {output_file}.")
