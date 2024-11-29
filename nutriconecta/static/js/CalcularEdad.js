$(document).ready(function() {
    $('#id_fecha_nacimiento').change(function() {
        var fechaNacimiento = $(this).val();
        $.ajax({
            url: calcularEdadUrl, // Usa la URL definida en el HTML
            data: {
                'fecha_nacimiento': fechaNacimiento
            },
            dataType: 'json',
            success: function(data) {
                console.log('Edad recibida:', data.edad);
                $('#id_edad').val(data.edad);
            }
        });
    });
});