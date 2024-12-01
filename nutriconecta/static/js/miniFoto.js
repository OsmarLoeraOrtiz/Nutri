$(document).ready(function() {
    // Hacer la solicitud AJAX al cargar la página
    $.ajax({
        url: UrlDatos, 
        type: 'GET',
        dataType: 'json',
        success: function(data) {
          if(data.foto && data.foto == "default"){
            $('#foto3').attr('src', UrlImagenDefault);
          }
          else if (data.foto) {
            $('#foto3').attr('src', 'data:image/jpeg;base64,' + data.foto);
          }
          else{
            $('#foto3').hide();
          }
        },
        error: function(error) {
            console.log("Valio verga");
        }
    });
});