// carousel.js

document.addEventListener('DOMContentLoaded', function () {
    const carouselTexts = document.querySelectorAll('.carousel-text');
    const phrases = Array.from(carouselTexts).map(text => text.textContent.trim());

    // Función para mezclar el arreglo en orden aleatorio
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    // Mezcla el arreglo de frases en orden aleatorio
    shuffle(phrases);

    let currentIndex = 0;

    // Función para mostrar la siguiente frase
    function showNextText() {
        carouselTexts[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % carouselTexts.length;
        carouselTexts[currentIndex].textContent = phrases[currentIndex];
        carouselTexts[currentIndex].classList.add('active');
    }

    // Muestra la primera frase aleatoria
    carouselTexts[currentIndex].textContent = phrases[currentIndex];
    carouselTexts[currentIndex].classList.add('active');

    // Cambia las frases cada 10 segundos (10000 milisegundos)
    setInterval(showNextText, 10000);
});
