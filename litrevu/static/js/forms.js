// Cibler des labels du formulaire django pour mise en forme (Modification de posts Ticket)
document.addEventListener("DOMContentLoaded", function() {
    var imageField = document.querySelector('.field-image-checkbox');

    if(imageField) {
        imageField.innerHTML = imageField.innerHTML.replace('Actuellement:', '<span class="current-label">Actuellement:</span>');
        imageField.innerHTML = imageField.innerHTML.replace('Modifier:', '<span class="modify-label">Modifier:</span>');
    }
});


// Système de notation avec des étoiles
document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.rating-stars .star');
    const ratingInput = document.getElementById('rating');

    stars.forEach(star => {
        star.addEventListener('click', () => {
            // Si la première étoile est déjà sélectionnée et qu'on clique dessus à nouveau
            if (star.dataset.value === '1' && star.classList.contains('selected')) {
                ratingInput.value = 0;
                highlightStars(0);
            } else {
                ratingInput.value = star.dataset.value;
                highlightStars(star.dataset.value);
            }
        });
    });

    function highlightStars(value) {
        stars.forEach((star, index) => {
            if (index < value) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }
});