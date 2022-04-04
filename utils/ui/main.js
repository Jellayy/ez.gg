var expanded = false;
    function showCheckboxes() {
        var checkboxes = document.getElementById('checkboxes');
        if (!expanded) {
            checkboxes.style.display = "block";
            expanded = true;
        }
        else {
            checkboxes.style.display = "none";
            expanded = false;
        }
    }

$(document).ready(function() {
    $('#alsotest').hover(function() {
        $('#test').css("background-color", "rgba(0, 136, 169, 0.8)")
    },
    function() {
        $('#test').css("background-color", "#202124")
    })
})