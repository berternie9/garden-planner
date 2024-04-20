document.addEventListener('DOMContentLoaded', function() {
    let hide_show_companion_friends = document.getElementById('hide_show_companion_friends');
    let companion_friends = document.getElementById('companion_friends');

    if ((hide_show_companion_friends) && (companion_friends)) {
        companion_friends.style.display = "none"

        hide_show_companion_friends.addEventListener('click', function(event) {
            if (companion_friends.style.display === "none") {
                companion_friends.style.display = ""
            }
            else {
                companion_friends.style.display = "none"
            }
        })
    }
})
