$(document).ready(function() {

    $('#autopilot_btn').on('click', function() {
        autopilot();
    })

    async function autopilot() {
        await eel.run_autopilot()();
    }

    // Populate champion selection fields with all champions
    async function get_champs() {
        let champs = await eel.get_all_champs()();
        for (var i = 0; i < champs.length; i++) {
            $('#champs').append("<option value='" + champs[i] + "'>");
        }
    }
    get_champs();

    // Auto queue accept button handler
    $('#queueaccept').change(function() {
        button_ready_check();
    })

    // Auto Lock-in button handler
    $('#lockin').change(function() {
        if(this.checked) {
            $("#firstpick").removeClass('disabled')
            $('#firstpospicks').removeClass('disabled')
        }
        else {
            $("#firstpick").addClass('disabled')
            $("#secondpick").addClass('disabled')
            $('#firstpospicks').addClass('disabled')
        }

        button_ready_check();
    })

    // Auto Ban button handler
    $('#ban').change(function() {
        if(this.checked) {
            $('#firstposbans').removeClass('disabled')
            if($('input[name=firstpos]:checked').val() != 'FILL') {
                $('#secondposbans').removeClass('disabled')
            }
        }
        else {
            $('#firstposbans').addClass('disabled')
            $('#secondposbans').addClass('disabled')
        }

        button_ready_check();
    })

    // On firstpos change
    $('#firstpos input').on('change', function() {
        if($('input[name=firstpos]:checked').val() != 'FILL') {
            $("#secondpick").removeClass('disabled')
            $('#secondpospicks').removeClass('disabled')
            if($('#ban').is(':checked')) {
                $('#secondposbans').removeClass('disabled')
            }
        }
        else {
            $("#secondpick").addClass('disabled')
            $('#secondpospicks').addClass('disabled')
            $('#secondposbans').addClass('disabled')
        }

        button_ready_check();
    })

    // On secondpos change
    $('#secondpos input').on('change', function() {
        button_ready_check();
    })

    // On champ entry box change
    $('.champentrybox').on('input', function() {
        button_ready_check();
    })

    function button_ready_check() {
        // Is auto lock-in selected?
        if($('#lockin').is(':checked')) {
            // Is first role selected?
            if($('input[name=firstpos]:checked', '#firstpos').val() != undefined) {
                // Are first role champs selected?
                if($('#firstpos_firstpick').val() && $('#firstpos_secondpick').val()) {
                    // Is first role fill?
                    if($('input[name=firstpos]:checked', '#firstpos').val() == 'FILL') {
                        // Is auto ban selected?
                        if($('#ban').is(':checked')) {
                            // Are first role bans selected?
                            if($('#firstpos_firstban').val() && $('#firstpos_secondban').val()) {
                                // All ok, enable button
                                $('#autopilot_btn').prop("disabled", false);
                            }
                            else {
                                $('#autopilot_btn').prop("disabled", true);
                            }
                        }
                        else {
                            // All ok, enable button
                            $('#autopilot_btn').prop("disabled", false);
                        }
                    }
                    else {
                        // Is second role selected?
                        if($('input[name=secondpos]:checked', '#secondpos').val() != undefined) {
                            // Is second role different from first role?
                            if($('input[name=secondpos]:checked', '#secondpos').val() != $('input[name=firstpos]:checked', '#firstpos').val()) {
                                // Are second role champs selected?
                                if($('#secondpos_firstpick').val() && $('#secondpos_secondpick').val()) {
                                    // Is auto ban selected?
                                    if($('#ban').is(':checked')) {
                                        // Are all bans selected?
                                        if($('#firstpos_firstban').val() && $('#firstpos_secondban').val() && $('#secondpos_firstban').val() && $('#secondpos_secondban').val()) {
                                            // All ok, enable button
                                            $('#autopilot_btn').prop("disabled", false);
                                        }
                                        else {
                                            $('#autopilot_btn').prop("disabled", true);
                                        }
                                    }
                                    else {
                                        // All ok, enable button
                                        $('#autopilot_btn').prop("disabled", false);
                                    }
                                }
                                else {
                                    $('#autopilot_btn').prop("disabled", true);
                                }
                            }
                            else {
                                $('#autopilot_btn').prop("disabled", true);
                            }
                        }
                        else {
                            $('#autopilot_btn').prop("disabled", true);
                        }
                    }
                }
                else {
                    $('#autopilot_btn').prop("disabled", true);
                }
            }
            else {
                $('#autopilot_btn').prop("disabled", true);
            }
        }
        else {
            // Is auto ban selected?
            if($('#ban').is(':checked')) {
                // Are two bans selected?
                if($('#firstpos_firstban').val() && $('#firstpos_secondban').val()) {
                    // All ok, enable button
                    $('#autopilot_btn').prop("disabled", false);
                }
                else {
                    $('#autopilot_btn').prop("disabled", true);
                }
            }
            else {
                // Is auto queue accept selected?
                if($('#queueaccept').is(':checked')) {
                    $('#autopilot_btn').prop("disabled", false);
                }
                else {
                    $('#autopilot_btn').prop("disabled", true);
                }
            }
        }
    }

    // Expose selections
    eel.expose(get_queue_preference);
    function get_queue_preference() {
        return $('#queueaccept').is(':checked');
    }
    eel.expose(get_lock_in_preference);
    function get_lock_in_preference() {
        return $('#lockin').is(':checked');
    }
    eel.expose(get_auto_ban_preference);
    function get_auto_ban_preference() {
        return $('#ban').is(':checked');
    }
    eel.expose(get_runes_preference);
    function get_runes_preference() {
        return $('#runes').is(':checked');
    }
    eel.expose(get_roles);
    function get_roles() {
        return [$('input[name=firstpos]:checked', '#firstpos').val(), $('input[name=secondpos]:checked', '#secondpos').val()]
    }
    eel.expose(get_pick_preferences);
    function get_pick_preferences() {
        return [$('#firstpos_firstpick').val(), $('#firstpos_secondpick').val(), $('#secondpos_firstpick').val(), $('#secondpos_secondpick').val()]
    }
    eel.expose(get_ban_prefrences);
    function get_ban_prefrences() {
        return [$('#firstpos_firstban').val(), $('#firstpos_secondban').val(), $('#secondpos_firstban').val(), $('#secondpos_secondban').val()]
    }

})