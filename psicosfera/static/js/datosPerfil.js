$(document).ready(function() {
    // Hacer la solicitud AJAX al cargar la página
  $.ajax({
      url: UrlDatos, 
      type: 'GET',
      dataType: 'json',
      success: function(data) {
        if (data.usuario == "default"){
          $('#foto3').attr('src', UrlImagenDefault);
        }
        // Mostrar detalles de los contactos
        var contactosHTML = '<div class="row justify-content-center">';
        if (data.contactos) {
          data.contactos.forEach(function(contacto) {
            contactosHTML += `
                <div class="col-md-6 mb-4">
                    <a href="../perfil/${contacto.usuario}" class="card-link">
                        <div class="card h-100">
                            <div class="card-body d-flex flex-column justify-content-center">
                                <h5 class="card-title text-center">${contacto.nombre} ${contacto.apellido}</h5>
                                <p class="card-text text-center">${contacto.especialidad}</p>
                                <p class="card-text text-center">${contacto.ubicacion}</p>
                                <!-- Agrega más detalles según tus necesidades -->
                            </div>
                        </div>
                    </a>
                </div>
            `;
        });
        } else {
          contactosHTML = '<p>Sin contactos</p>';  
      }
        contactosHTML += '</div>';

        if (data.usuario == "registrado"){
          if (data.foto) {
            $('#foto').attr('src', 'data:image/jpeg;base64,' + data.foto);
            $('#foto2').attr('src', 'data:image/jpeg;base64,' + data.foto);
            $('#foto3').attr('src', 'data:image/jpeg;base64,' + data.foto);
          }else{
            $('#foto').hide();
            $('#foto2').hide();
            $('#foto3').hide();
          }
          $('#user2').text(data.user);
          $('#user').text(data.user);
          $('#userName').val(data.user);
          $('#nombre').text(data.nombre +' '+ data.apellidos);
          $("#firstName").val(data.nombre);
          $("#lastName").val(data.apellidos);
          $('#edad').text(data.edad);
          $('#age').val(data.edad);
          $('#correo').text(data.correo);
          //document.getElementById('correo2').value = data.correo;
          $('#numero').text(data.telefono);
          $("#Phone").val(data.telefono);
          $('#descripcion').text(data.descripcion);
          $('#descripcion2').text(data.descripcion);
          $('#ubicacion').text(data.ubicacion);
          $('#contactos').html(contactosHTML);
          

          if (data.psicologo == 1){
            // Mostrar detalles de los contactos
        var contactosHTML2 = '<div class="row justify-content-center">';
        // Crear opciones para el select
        var dropdownOptions = '';
        
        if (data.contactos) {
          data.contactos.forEach(function(contacto) {
              contactosHTML2 += `
                  <div class="col-md-6 mb-4">
                      <a href="../perfil/${contacto.usuario}" class="card-link">
                          <div class="card h-100">
                              <div class="card-body d-flex flex-column justify-content-center">
                                  <h5 class="card-title text-center">${contacto.nombre} ${contacto.apellido}</h5>
                                  <p class="card-text text-center">Paciente</p>
                                  <p class="card-text text-center">${contacto.ubicacion}</p>
                                  <!-- Agrega más detalles según tus necesidades -->
                              </div>
                          </div>
                      </a>
                  </div>
              `;

              dropdownOptions += `<option value="${contacto.usuario}">${contacto.nombre} ${contacto.apellido}</option>`;
          });
        } else {
          contactosHTML2 = '<p>Sin contactos</p>';  
      }
        contactosHTML2 += '</div>';

            $('#especialidad').text(data.especialidad);
            $('#especialidad2').text(data.especialidad);
            $('#institucion').text(data.institucion);
            $('#certificado').attr('src', 'data:application/pdf;base64,' + data.certificado);
            $('#curriculum').attr('src', 'data:application/pdf;base64,' + data.curriculum);
            $('#institucion2').val(data.institucion);
            $('#cedula1').text(data.cedula);
            $('#cedula').val(data.cedula);
            $('#especiality').val(data.especialidad);
            $('#facebook').attr('href', data.facebook);
            $("#Facebook").val(data.facebook);
            $('#instagram').attr('href', data.instagram);
            $("#Instagram").val(data.instagram);
            $('#linkedin').attr('href', data.linkedin);
            $("#Linkedin").val(data.linkedin);
            $('#twitter').attr('href', data.twitter);
            $("#Twitter").val(data.twitter);
            $('#contactosPsico').html(contactosHTML2);
            console.log('Opciones del select:', dropdownOptions);
            $('#dropdownPacientes').html(dropdownOptions);
           



            $('#direccion').text(data.direccion);
            $('#address').val(data.direccion);
            $('#costo_consulta').text("$"+data.costo_consulta);
            $('#costo_consulta2').val(data.costo_consulta);
            $('#cierre').text(data.cierre);
            $('#apertura').text(data.apertura);
            $('#cierre2').val(data.cierre);
            $('#apertura2').val(data.apertura);
            $('#horario').text(data.apertura + ' - ' + data.cierre);
          }
        }
      },
    error: function(error) {
      console.log(error);
    }
  });
});

