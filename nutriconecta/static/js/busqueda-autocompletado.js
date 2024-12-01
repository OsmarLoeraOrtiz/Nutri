function setupAutocomplete(inputElement, resultsContainer, endpoint) {
    inputElement.on('input', function () {
        var query = $(this).val();

        if (query.length >= 2) {
            $.ajax({
                url: endpoint,
                method: 'GET',
                data: {
                    query: query
                },
                success: function (data) {
                    resultsContainer.empty();

                    data.forEach(function (sugerencia) {
                        var suggestionItem = $('<div>').addClass('autocomplete-item');
                        var regex = new RegExp('(' + query + ')', 'gi');
                        sugerencia = sugerencia.replace(regex, '<b>$1</b>');
                        suggestionItem.html(sugerencia);

                        suggestionItem.on('click', function () {
                            inputElement.val(sugerencia.replace(/<\/?b>/g, ''));
                            resultsContainer.hide();
                        });

                        resultsContainer.append(suggestionItem);
                    });

                    resultsContainer.show();
                }
            });
        } else {
            resultsContainer.hide();
        }
    });

    // Manejar la animación al hacer clic
    resultsContainer.on('click', '.autocomplete-item', function () {
        $(this).addClass('clicked');
    });
}

// Configurar la funcionalidad de autocompletado para la barra de búsqueda de especialidades
setupAutocomplete($('#specialty-input'), $('#autocomplete-results-specialty'), 'autocompletar-especialidades/');

// Configurar la funcionalidad de autocompletado para la barra de búsqueda de ubicaciones
setupAutocomplete($('#location-input'), $('#autocomplete-results-location'), 'autocompletar-ubicaciones/');

// Configurar la funcionalidad de autocompletado para la barra de direccion del consultorio
setupAutocomplete($('#direccion-input'), $('#autocomplete-results-location'), '/../paciente/autocompletar-ubicaciones/');

// Configurar la funcionalidad de autocompletado para la barra de búsqueda de especialidades en el form
setupAutocomplete($('#especialidad-input'), $('#autocomplete-results-specialty'), '/../paciente/autocompletar-especialidades/');
