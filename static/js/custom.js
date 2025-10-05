// JavaScript untuk tombol "Scroll Up"
document.addEventListener("DOMContentLoaded", function() {
    const scrollUpButton = document.getElementById('scrollUp');

    // Tampilkan atau sembunyikan tombol saat menggulir
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) { // Munculkan tombol setelah menggulir 300px
            scrollUpButton.classList.add('show');
        } else {
            scrollUpButton.classList.remove('show');
        }
    });

    // Gulir ke atas saat tombol diklik
    scrollUpButton.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});