$(document).ready(function() {
    $('#primaryrole').on('change', function() {
        eel.set_roles('primary', this.value);
    })
    $('#secondaryrole').on('change', function() {
        eel.set_roles('secondary', this.value);
    })
})