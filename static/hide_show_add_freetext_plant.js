document.addEventListener('DOMContentLoaded', function() {
    let hide_show_add_freetext_plant = document.getElementById('hide_show_add_freetext_plant');
    let add_freetext_plant = document.getElementById('add_freetext_plant_form');

    if ((add_freetext_plant) && (hide_show_add_freetext_plant)) {
        add_freetext_plant.style.display = "none";

        hide_show_add_freetext_plant.addEventListener('click', function(event) {
            if (add_freetext_plant.style.display === "none") {
                add_freetext_plant.style.display = "";
            }
            else {
                add_freetext_plant.style.display = "none";
            }
        })
    }
})
