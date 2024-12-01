function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var preview = document.getElementById('preview');
        preview.src = reader.result;
        preview.style.display = 'block';
    };
    if (event.target.files.length === 0) {
        // Si no se selecciona ninguna imagen, muestra la imagen predeterminada
        preview.src = "{% static 'img/usuario.png' %}";
        preview.style.display = 'block';
    } else {
        reader.readAsDataURL(event.target.files[0]);
    }
}