document.addEventListener('DOMContentLoaded', function() {
    var searchbar_all_plants_table, search_all_plants_header_footer_tr, search_all_plants_body_tr, name_cell;

    searchbar_all_plants_table = document.getElementById("searchbar_all_plants_table");
    search_all_plants_header_footer_tr = document.querySelectorAll(".search_all_plants_header_footer_tr");
    search_all_plants_body_tr = document.querySelectorAll(".search_all_plants_body_tr");

    if ((searchbar_all_plants_table) && (search_all_plants_header_footer_tr) && (search_all_plants_body_tr)) {
        for (i = 0; i < search_all_plants_header_footer_tr.length; i++) {
            search_all_plants_header_footer_tr[i].style.display = 'none';
        }
        for (i = 0; i < search_all_plants_body_tr.length; i++) {
            search_all_plants_body_tr[i].style.display = 'none';
        }

        searchbar_all_plants_table.addEventListener('click', function(event) {
            document.addEventListener('keyup', function(event) {
                if (searchbar_all_plants_table.value == '') {
                    for (i = 0; i < search_all_plants_header_footer_tr.length; i++) {
                        search_all_plants_header_footer_tr[i].style.display = 'none';
                    }
                    for (i = 0; i < search_all_plants_body_tr.length; i++) {
                        search_all_plants_body_tr[i].style.display = 'none';
                    }
                }

                for (i = 0; i < search_all_plants_body_tr.length; i++) {
                    name_cell = search_all_plants_body_tr[i].getElementsByTagName("TD")[0];
                    for (j = 0; j < searchbar_all_plants_table.value.toLowerCase().length; j++) {
                        if (searchbar_all_plants_table.value.toLowerCase().length <= name_cell.innerHTML.toLowerCase().length) {
                            if (searchbar_all_plants_table.value.toLowerCase().localeCompare(name_cell.innerHTML.slice(0, searchbar_all_plants_table.value.toLowerCase().length).toLowerCase()) === 0) {
                                for (k = 0; k < search_all_plants_header_footer_tr.length; k++) {
                                    search_all_plants_header_footer_tr[k].style.display = 'table-row';
                                }
                                search_all_plants_body_tr[i].style.display = 'table-row';
                            }
                            else {
                                search_all_plants_body_tr[i].style.display = 'none';
                            }
                        }
                    }
                }
            })
        })
    }
})
