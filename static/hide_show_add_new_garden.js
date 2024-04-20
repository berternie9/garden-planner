document.addEventListener('DOMContentLoaded', function() {
    let hide_show_add_new_garden = document.getElementById('hide_show_add_new_garden');
    let add_new_garden = document.getElementById('add_new_garden_form');

    if ((hide_show_add_new_garden) && (add_new_garden)) {
        add_new_garden.style.display = "none"

        hide_show_add_new_garden.addEventListener('click', function(event) {
            if (add_new_garden.style.display === "none") {
                add_new_garden.style.display = ""
            }
            else {
                add_new_garden.style.display = "none"
            }
        })
    }
})
