document.addEventListener('DOMContentLoaded', function() {
    let hide_show_companion_enemies = document.getElementById('hide_show_companion_enemies');
    let companion_ememies = document.getElementById('companion_ememies');

    if ((hide_show_companion_enemies) && (companion_ememies)) {
        companion_ememies.style.display = "none"

        hide_show_companion_enemies.addEventListener('click', function(event) {
            if (companion_ememies.style.display === "none") {
                companion_ememies.style.display = ""
            }
            else {
                companion_ememies.style.display = "none"
            }
        })
    }
})
