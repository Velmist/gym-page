document.addEventListener("DOMContentLoaded", function () {
    const animatedButton = document.getElementById("animated-button");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    animatedButton.classList.add("visible");
                    observer.unobserve(animatedButton);
                }
            });
        },
        { threshold: 0.1 } // Activa la animación cuando el 10% del elemento esté visible
    );

    observer.observe(animatedButton);
    
    if (entry.isIntersecting) {
        console.log("Botón visible - Añadiendo clase 'visible'");
        animatedButton.classList.add("visible");
    }
document.addEventListener('DOMContentLoaded', function() {
    // Manejar el envío del formulario de logout
    document.querySelectorAll('form[action="{{ url_for("logout") }}"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            fetch(this.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(new FormData(this))
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
});   
