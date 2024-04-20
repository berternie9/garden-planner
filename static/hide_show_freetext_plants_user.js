document.addEventListener('DOMContentLoaded', function() {
    let hide_show_freetext_plants_user = document.getElementById('hide_show_freetext_plants_user');
    let freetext_plants_user_table = document.getElementById('freetext_plants_user_table');

    if ((hide_show_freetext_plants_user) && (freetext_plants_user_table)) {
        freetext_plants_user_table.style.display = "none"

        hide_show_freetext_plants_user.addEventListener('click', function(event) {
            if (freetext_plants_user_table.style.display === "none") {
                freetext_plants_user_table.style.display = ""
            }
            else {
                freetext_plants_user_table.style.display = "none"
            }
        })
    }
})
