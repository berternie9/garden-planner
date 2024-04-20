document.addEventListener('DOMContentLoaded', function() {

    let yearly_garden_tables = document.querySelectorAll('.yearly_garden_table');
    for (let i = 0; i < yearly_garden_tables.length; i++) {
        let months_rows = yearly_garden_tables[i].getElementsByTagName('TR');
        months_rows[1].style.background = 'rgba(240, 193, 193, 0.2)';
        months_rows[2].style.background = 'rgba(240, 193, 193, 0.2)';
        months_rows[3].style.background = 'rgba(240, 228, 193, 0.2)';
        months_rows[4].style.background = 'rgba(240, 228, 193, 0.2)';
        months_rows[5].style.background = 'rgba(240, 228, 193, 0.2)';
        months_rows[6].style.background = 'rgba(193, 240, 240, 0.2)';
        months_rows[7].style.background = 'rgba(193, 240, 240, 0.2)';
        months_rows[8].style.background = 'rgba(193, 240, 240, 0.2)';
        months_rows[9].style.background = 'rgba(193, 240, 193, 0.2)';
        months_rows[10].style.background = 'rgba(193, 240, 193, 0.2)';
        months_rows[11].style.background = 'rgba(193, 240, 193, 0.2)';
        months_rows[12].style.background = 'rgba(240, 193, 193, 0.2)';
    }
})
