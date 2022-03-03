$(document).ready(function() {

    eel.expose(get_roles);
    function get_roles() {
        return [$('#primaryrole').value, $('#secondaryrole').value]
    }

    // // Role selector handlers
    // $('#primaryrole').on('change', function() {
    //     eel.autopilot_settings('primary_role', this.value);
    // })
    // $('#secondaryrole').on('change', function() {
    //     eel.autopilot_settings('secondary_role', this.value);
    // })

    // // Misc setting handlers
    // $('#queueaccept').on('change', function() {
    //     eel.autopilot_settings('queueaccept', $('#queueaccept').is(':checked'));
    // })
    // $('#lockin').on('change', function() {
    //     eel.autopilot_settings('lockin', $('#lockin').is(':checked'));
    // })

})