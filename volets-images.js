// volets-images.js - VERSION AVEC SCROLL CORRIGÉ
document.addEventListener('DOMContentLoaded', function() {
    
    // Fonction pour convertir TOUS les formats de timecode en secondes
    function timecodeToSeconds(timecode) {
        // Nettoyer le timecode
        const cleanTimecode = timecode
            .replace(' et ensemble de la vidéo', '')
            .replace('h', ':')
            .replace('min', ':')
            .replace('s', '')
            .trim();
        
        // Format "hh:mm:ss" (comme 02:08:27)
        const hmsMatch = cleanTimecode.match(/(\d+):(\d+):(\d+)/);
        if (hmsMatch) {
            const hours = parseInt(hmsMatch[1]) || 0;
            const minutes = parseInt(hmsMatch[2]) || 0;
            const seconds = parseInt(hmsMatch[3]) || 0;
            return (hours * 3600) + (minutes * 60) + seconds;
        }
        
        // Format "mm:ss" (comme 08:27)
        const msMatch = cleanTimecode.match(/(\d+):(\d+)/);
        if (msMatch) {
            const minutes = parseInt(msMatch[1]) || 0;
            const seconds = parseInt(msMatch[2]) || 0;
            return (minutes * 60) + seconds;
        }
        
        // Ancien format "min" et "s" (comme 01min46s)
        const minsecMatch = cleanTimecode.match(/(\d+)min(\d+)s/);
        if (minsecMatch) {
            const minutes = parseInt(minsecMatch[1]) || 0;
            const seconds = parseInt(minsecMatch[2]) || 0;
            return (minutes * 60) + seconds;
        }
        
        // Si c'est "cover" ou contient "cover"
        if (timecode.toLowerCase().includes('cover')) {
            return 0;
        }
        
        // Si aucun format ne correspond
        console.warn('Format de timecode non reconnu:', timecode);
        return 99999; // Mettre à la fin
    }
    
    // Fonction pour faire défiler jusqu'à un élément
    function scrollToElement(element) {
        // Calculer la position après que tous les changements de DOM soient terminés
        setTimeout(() => {
            const headerOffset = 100; // Ajustez cette valeur selon la hauteur de votre en-tête
            const elementPosition = element.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }, 300); // Délai pour laisser le temps au volet précédent de se fermer
    }
    
    // ÉTAPE 1 : Récupérer TOUTES les images du tableau caché
    function getAllImages() {
        const sourceTable = document.getElementById('all-images-source');
        if (!sourceTable) return [];
        
        const rows = sourceTable.querySelectorAll('tr');
        const images = [];
        
        rows.forEach((row, index) => {
            // Sauter la ligne d'en-tête (première ligne <tr> dans tbody)
            if (index === 0 && row.parentElement.tagName === 'THEAD') return;
            
            const cells = row.querySelectorAll('td');
            // Prendre les 3 premières cellules (Image, Timecode, Cartel)
            if (cells.length >= 3) {
                const imgElement = cells[0].querySelector('img');
                const timecode = cells[1].textContent.trim();
                const caption = cells[2].textContent.trim();
                
                if (imgElement) {
                    const seconds = timecodeToSeconds(timecode);
                    
                    images.push({
                        src: imgElement.src,
                        timecode: timecode,
                        seconds: seconds,
                        caption: caption,
                        html: row.outerHTML
                    });
                }
            }
        });
        
        // Trier par timecode (secondes)
        return images.sort((a, b) => a.seconds - b.seconds);
    }
    
    // Fonction pour fermer un volet et attendre la fin de l'animation
    function closeVoletAndWait(volet) {
        return new Promise((resolve) => {
            volet.classList.remove('open');
            const content = volet.querySelector('.volet-content');
            content.style.maxHeight = null;
            
            // Attendre la fin de la transition (0.6s dans votre CSS)
            setTimeout(resolve, 600);
        });
    }
    
    // ÉTAPE 2 : Fonction pour ouvrir/fermer un volet
    async function toggleVolet(volet, scrollToVolet = true) {
        const isOpen = volet.classList.contains('open');
        const content = volet.querySelector('.volet-content');
        
        if (isOpen) {
            // Fermer ce volet
            volet.classList.remove('open');
            content.style.maxHeight = null;
        } else {
            // Fermer d'abord tous les autres volets et attendre
            const openVolets = Array.from(document.querySelectorAll('.image-volet.open')).filter(v => v !== volet);
            
            // Fermer tous les volets ouverts en parallèle
            await Promise.all(openVolets.map(closeVoletAndWait));
            
            // Maintenant ouvrir le nouveau volet
            volet.classList.add('open');
            
            // Charger les images si c'est la première fois
            if (!volet.dataset.loaded) {
                loadImagesIntoVolet(volet);
                volet.dataset.loaded = 'true';
            }
            
            // Ajuster la hauteur
            setTimeout(() => {
                content.style.maxHeight = content.scrollHeight + "px";
                
                // Défilement automatique vers le volet (sauf pour le premier chargement)
                if (scrollToVolet) {
                    scrollToElement(volet);
                }
            }, 50);
        }
    }
    
    // ÉTAPE 3 : Charger les images dans un volet
    function loadImagesIntoVolet(volet) {
        const startTime = parseInt(volet.dataset.timeStart) || 0;
        const endTime = parseInt(volet.dataset.timeEnd) || 99999;
        const content = volet.querySelector('.volet-content');
        const allImages = getAllImages();
        
        // Filtrer les images dans la plage de temps
        const filteredImages = allImages.filter(img => {
            return img.seconds >= startTime && img.seconds < endTime;
        });
        
        // Ajouter ou mettre à jour le compteur
        let countElement = volet.querySelector('.volet-count');
        if (!countElement) {
            const titleElement = volet.querySelector('.volet-title');
            if (titleElement) {
                titleElement.insertAdjacentHTML('afterend', 
                    `<span class="volet-count">(${filteredImages.length} images)</span>`);
                countElement = volet.querySelector('.volet-count');
            }
        } else {
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
        
        volets.forEach((volet, index) => {
            const header = volet.querySelector('.volet-header');
            
            // Ajouter l'événement click
            header.addEventListener('click', async () => {
                // Pour le premier volet au chargement, ne pas scroller
                const shouldScroll = !(index === 0 && !volet.dataset.loaded);
                await toggleVolet(volet, shouldScroll);
            });
            
            // Pré-calculer et afficher le nombre d'images pour chaque volet
            setTimeout(() => {
                const allImages = getAllImages();
                const startTime = parseInt(volet.dataset.timeStart) || 0;
                const endTime = parseInt(volet.dataset.timeEnd) || 99999;
                
                const count = allImages.filter(img => 
                    img.seconds >= startTime && img.seconds < endTime
                ).length;
                
                // Ajouter ou mettre à jour le compteur
                let countElement = volet.querySelector('.volet-count');
                if (!countElement) {
                    const titleElement = volet.querySelector('.volet-title');
                    if (titleElement) {
                        titleElement.insertAdjacentHTML('afterend', 
                            `<span class="volet-count">(${count} images)</span>`);
                    }
                } else {
                    countElement.textContent = `(${count} images)`;
                }
            }, 100);
        });
        
        // Ouvrir le premier volet automatiquement (sans scroll)
        if (volets[0]) {
            setTimeout(() => {
                toggleVolet(volets[0], false); // false = pas de scroll
            }, 200);
        }
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