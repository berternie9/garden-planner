document.addEventListener('DOMContentLoaded', function() {
    let hide_show_remove_plants_from_garden = document.getElementById('hide_show_remove_plants_from_garden');
    let remove_plants_from_garden = document.getElementById('remove_plants_from_garden_form');

    if ((hide_show_remove_plants_from_garden) && (remove_plants_from_garden)) {
        remove_plants_from_garden.style.display = "none"

        hide_show_remove_plants_from_garden.addEventListener('click', function(event) {
            if (remove_plants_from_garden.style.display === "none") {
                remove_plants_from_garden.style.display = ""
            }
            else {
                remove_plants_from_garden.style.display = "none"
            }
        })
    }
})
