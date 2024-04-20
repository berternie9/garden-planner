document.addEventListener('DOMContentLoaded', function() {
    let hide_show_remove_freetext_plant = document.getElementById('hide_show_remove_freetext_plant');
    let remove_freetext_plant = document.getElementById('remove_freetext_plant_form');

    if ((hide_show_remove_freetext_plant) && (remove_freetext_plant)) {
        remove_freetext_plant.style.display = "none"

        hide_show_remove_freetext_plant.addEventListener('click', function(event) {
            if (remove_freetext_plant.style.display === "none") {
                remove_freetext_plant.style.display = ""
            }
            else {
            remove_freetext_plant.style.display = "none"
            }
        })
    }
})
