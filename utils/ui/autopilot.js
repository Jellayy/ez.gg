$(document).ready(function() {

    eel.expose(get_roles);
    function get_roles() {
        return [$('#primaryrole').val(), $('#secondaryrole').val()]
    }

    eel.expose(get_queue_prefrence);
    function get_queue_prefrence() {
        return $('#queueaccept').is(':checked');
    }

    eel.expose(get_lock_in_prefrence);
    function get_queue_prefrence() {
        return $('#lockin').is(':checked');
    }

})