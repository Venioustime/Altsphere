// back-to-top.js
document.addEventListener('DOMContentLoaded', function() {
    // Fonction pour le bouton "Retour en haut"
    const backToTopButton = document.getElementById('back-to-top');
    
    if (!backToTopButton) return;
    
    // Afficher/masquer le bouton au scroll
    function toggleBackToTop() {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.add('visible');
        } else {
            backToTopButton.classList.remove('visible');
        }
    }
    
    // Événement scroll
    window.addEventListener('scroll', toggleBackToTop);
    
    // Événement click pour remonter
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Initialiser l'état au chargement
    toggleBackToTop();
});

// Fonction pour le bouton "Retour à la page précédente"
function initBackButton() {
    const backButton = document.getElementById('go-back');
    
    if (!backButton) {
        console.warn("Bouton 'Retour' non trouvé");
        return;
    }
    
    // Fonction pour revenir en arrière
    function goBack() {
        // Vérifier s'il y a une page précédente dans l'historique
        if (document.referrer !== "" && document.referrer.indexOf(window.location.hostname) !== -1) {
            // Si on vient du même site, utiliser l'historique
            window.history.back();
        } else {
            // Sinon, rediriger vers une page par défaut (ex: index.html)
            window.location.href = "./index.html"; // Changez selon votre structure
        }
    }
    
    // Événement click
    backButton.addEventListener('click', goBack);
    
    // Navigation au clavier
    backButton.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            goBack();
        }
    });
}

// Appeler cette fonction après initBackToTop()
initBackButton();