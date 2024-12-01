const buttons = document.querySelectorAll('.btn-toggle');
  
    buttons.forEach(button => {
      button.addEventListener('click', () => {
        buttons.forEach(btn => btn.classList.remove('btn-selected'));
        button.classList.add('btn-selected');
      });
    });