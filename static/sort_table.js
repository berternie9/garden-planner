document.addEventListener('DOMContentLoaded', function() {
    var testing, all_plants_tbody_tr, search_all_plants_body_tr, freetext_plants_body_tr, companion_friends_body_tr, companion_enemies_body_tr, switching, shouldSwitch, i, x, y;

    all_plants_tbody_tr = document.getElementsByClassName("all_plants_tbody_tr");
    search_all_plants_body_tr = document.getElementsByClassName("search_all_plants_body_tr");
    freetext_plants_body_tr = document.getElementsByClassName("freetext_plants_body_tr");
    companion_friends_body_tr = document.getElementsByClassName("companion_friends_body_tr");
    companion_enemies_body_tr = document.getElementsByClassName("companion_enemies_body_tr");

    testing = document.getElementById("testing");

    function sort_table(tr) {
        if (tr) {
            switching = true;

            while (switching) {
                switching = false;

                for (i = 0; i < tr.length - 1; i++) {
                    for (j = i + 1; j < tr.length; j++) {
                        shouldSwitch = false;
                        x = tr[i].getElementsByTagName("TD")[0];
                        y = tr[j].getElementsByTagName("TD")[0];
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                        }

                        if (shouldSwitch == true) {
                            var clonedEarlier = tr[i].cloneNode(true);
                            var clonedLater = tr[j].cloneNode(true);
                            tr[i].parentNode.replaceChild(clonedLater, tr[i])
                            tr[j].parentNode.replaceChild(clonedEarlier, tr[j])
                            switching = true;
                        }
                    }
                }
            }
        }
    }

    sort_table(all_plants_tbody_tr);
    sort_table(search_all_plants_body_tr);
    sort_table(freetext_plants_body_tr);
    sort_table(companion_friends_body_tr);
    sort_table(companion_enemies_body_tr);

})
