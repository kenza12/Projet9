document.addEventListener("DOMContentLoaded", function() {
    var imageField = document.querySelector('.field-image-checkbox');

    if(imageField) {
        imageField.innerHTML = imageField.innerHTML.replace('Actuellement:', '<span class="current-label">Actuellement:</span>');
        imageField.innerHTML = imageField.innerHTML.replace('Modifier:', '<span class="modify-label">Modifier:</span>');
    }
});

