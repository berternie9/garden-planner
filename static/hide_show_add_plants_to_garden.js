document.addEventListener('DOMContentLoaded', function() {
    let hide_show_add_plants_to_garden = document.getElementById('hide_show_add_plants_to_garden');
    let add_plants_to_garden = document.getElementById('add_plants_to_garden_form');

    if ((hide_show_add_plants_to_garden) && (add_plants_to_garden)) {
        add_plants_to_garden.style.display = "none"

        hide_show_add_plants_to_garden.addEventListener('click', function(event) {
            if (add_plants_to_garden.style.display === "none") {
                add_plants_to_garden.style.display = ""
            }
            else {
                add_plants_to_garden.style.display = "none"
            }
        })
    }
})
