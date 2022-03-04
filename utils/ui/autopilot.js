$(document).ready(function() {

    // Populate champion selection fields with all champions
    async function get_champs() {
        let champs = await eel.get_all_champs()();
        for (var i = 0; i < champs.length; i++) {
            $('#champs').append("<option value='" + champs[i] + "'>");
        }
    }
    get_champs();

    // On firstpos change
    $('#firstpos input').on('change', function() {
        console.log($('input[name=firstpos]:checked', '#firstpos').val());
        console.log($('#firstpos_firstpick').val());
    })

    // On secondpos change
    $('#secondpos input').on('change', function() {
        console.log($('input[name=secondpos]:checked', '#secondpos').val());
    })

    // Expose selections
    eel.expose(get_roles);
    function get_roles() {
        return [$('input[name=firstpos]:checked', '#firstpos').val(), $('input[name=secondpos]:checked', '#secondpos').val()]
    }
    eel.expose(get_queue_prefrence);
    function get_queue_prefrence() {
        return $('#queueaccept').is(':checked');
    }
    eel.expose(get_lock_in_prefrence);
    function get_lock_in_prefrence() {
        return $('#lockin').is(':checked');
    }
    eel.expose(get_pick_prefrences);
    function get_pick_prefrences() {
        return [$('#firstpos_firstpick').val(), $('#firstpos_secondpick').val(), $('#secondpos_firstpick').val(), $('#secondpos_secondpick').val()]
    }
    eel.expose(get_ban_prefrences);
    function get_ban_prefrences() {
        return [$('#firstpos_firstban').val(), $('#firstpos_secondban').val(), $('#secondpos_firstban').val(), $('#secondpos_secondban').val()]
    }

})