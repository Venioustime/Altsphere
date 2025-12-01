// volets-images.js
document.addEventListener('DOMContentLoaded', function() {
    
    // ÉTAPE 1 : Récupérer TOUTES les images du tableau caché
    function getAllImages() {
        const sourceTable = document.getElementById('all-images-source');
        if (!sourceTable) return [];
        
        const rows = sourceTable.querySelectorAll('tr');
        const images = [];
        
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            if (cells.length >= 3) {
                const imgElement = cells[0].querySelector('img');
                const timecode = cells[1].textContent.trim();
                const caption = cells[2].textContent.trim();
                
                if (imgElement) {
                    // Convertir le timecode en secondes pour faciliter le tri
                    let seconds = 0;
                    if (timecode === 'cover') {
                        seconds = 0;
                    } else {
                        const match = timecode.match(/(\d+)min(\d+)s/);
                        if (match) {
                            seconds = parseInt(match[1]) * 60 + parseInt(match[2]);
                        }
                    }
                    
                    images.push({
                        src: imgElement.src,
                        timecode: timecode,
                        seconds: seconds,
                        caption: caption,
                        html: row.outerHTML // Garder le HTML original
                    });
                }
            }
        });
        
        return images;
    }
    
    // ÉTAPE 2 : Fonction pour ouvrir/fermer un volet
    function toggleVolet(volet) {
        const isOpen = volet.classList.contains('open');
        const content = volet.querySelector('.volet-content');
        const arrow = volet.querySelector('.volet-arrow');
        
        // Fermer tous les autres volets (optionnel)
        // Si vous voulez que plusieurs puissent rester ouverts, enlevez ces 3 lignes
        document.querySelectorAll('.image-volet.open').forEach(openVolet => {
            if (openVolet !== volet) {
                openVolet.classList.remove('open');
                openVolet.querySelector('.volet-content').style.maxHeight = null;
            }
        });
        
        if (isOpen) {
            // Fermer ce volet
            volet.classList.remove('open');
            content.style.maxHeight = null;
        } else {
            // Ouvrir ce volet
            volet.classList.add('open');
            
            // Charger les images si c'est la première fois
            if (!volet.dataset.loaded) {
                loadImagesIntoVolet(volet);
                volet.dataset.loaded = 'true';
            }
            
            // Ajuster la hauteur
            content.style.maxHeight = content.scrollHeight + "px";
        }
    }
    
    // ÉTAPE 3 : Charger les images dans un volet
    function loadImagesIntoVolet(volet) {
        const startTime = parseInt(volet.dataset.timeStart) || 0;
        const endTime = parseInt(volet.dataset.timeEnd) || 9999;
        const content = volet.querySelector('.volet-content');
        const allImages = getAllImages();
        
        // Filtrer les images dans la plage de temps
        const filteredImages = allImages.filter(img => {
            return img.seconds >= startTime && img.seconds < endTime;
        });
        
        // Mettre à jour le compteur
        const countElement = volet.querySelector('.volet-count');
        if (countElement) {
            countElement.textContent = `(${filteredImages.length} images)`;
        }
        
        // Créer le tableau dans le volet
        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th>Image</th>
                        <th>Timecode</th>
                        <th>Cartel</th>
                    </tr>
                </thead>
                <tbody>
        `;
        
        filteredImages.forEach(img => {
            tableHTML += img.html;
        });
        
        tableHTML += `
                </tbody>
            </table>
        `;
        
        // Insérer le tableau
        content.innerHTML = tableHTML;
        
        // Ajouter du lazy loading à toutes les images
        content.querySelectorAll('img').forEach(img => {
            img.loading = 'lazy';
        });
    }
    
    // ÉTAPE 4 : Initialiser tous les volets
    function initVolets() {
        const volets = document.querySelectorAll('.image-volet');
        
        volets.forEach(volet => {
            const header = volet.querySelector('.volet-header');
            
            // Ajouter l'événement click
            header.addEventListener('click', () => {
                toggleVolet(volet);
            });
            
            // Option : ouvrir le premier volet automatiquement
            if (volet === volets[0]) {
                setTimeout(() => {
                    toggleVolet(volet);
                }, 500);
            }
        });
    }
    
    // Démarrer tout
    initVolets();
    
    // Fonction utilitaire pour créer un volet dynamiquement (si besoin)
    window.createVolet = function(title, start, end) {
        const section = document.querySelector('.image-table');
        
        const voletHTML = `
            <div class="image-volet" data-time-start="${start}" data-time-end="${end}">
                <button class="volet-header">
                    <span class="volet-title">${title}</span>
                    <span class="volet-count">(0 images)</span>
                    <span class="volet-arrow">▼</span>
                </button>
                <div class="volet-content"></div>
            </div>
        `;
        
        section.insertAdjacentHTML('beforeend', voletHTML);
        initVolets(); // Ré-initialiser pour ce nouveau volet
    };
});