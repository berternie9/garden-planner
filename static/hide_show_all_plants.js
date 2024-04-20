document.addEventListener('DOMContentLoaded', function() {
    let hide_show_all_plants = document.getElementById('hide_show_all_plants');
    let all_plants_table = document.getElementById('all_plants_table');

    if ((hide_show_all_plants) && (all_plants_table)) {
        all_plants_table.style.display = "none"

        hide_show_all_plants.addEventListener('click', function(event) {
            if (all_plants_table.style.display === "none") {
                all_plants_table.style.display = ""
            }
            else {
                all_plants_table.style.display = "none"
            }
        })
    }
})
