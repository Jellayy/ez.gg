$(document).ready(function() {

    // Role selector handlers
    $('#primaryrole').on('change', function() {
        eel.autopilot_settings('primary_role', this.value);
    })
    $('#secondaryrole').on('change', function() {
        eel.autopilot_settings('secondary_role', this.value);
    })

    // Misc setting handlers
    $('#queueaccept').on('change', function() {
        eel.autopilot_settings('queueaccept', $('#queueaccept').is(':checked'));
    })
    $('#lockin').on('change', function() {
        eel.autopilot_settings('lockin', $('#lockin').is(':checked'));
    })

})