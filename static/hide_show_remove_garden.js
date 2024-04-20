document.addEventListener('DOMContentLoaded', function() {
    let hide_show_remove_garden = document.getElementById('hide_show_remove_garden');
    let remove_garden = document.getElementById('remove_garden_form');

    if ((hide_show_remove_garden) && (remove_garden)) {
        remove_garden.style.display = "none"

        hide_show_remove_garden.addEventListener('click', function(event) {
            if (remove_garden.style.display === "none") {
                remove_garden.style.display = ""
            }
            else {
                remove_garden.style.display = "none"
            }
        })
    }
})
