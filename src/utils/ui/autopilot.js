$(document).ready(function () {

    // Populate champion selection fields with all champions from python ddragon
    async function get_champs() {
        let champs = await eel.get_all_champs()();
        for (var i = 0; i < champs.length; i++) {
            $('#champs').append("<option value='" + champs[i] + "'>");
        }
    }
    get_champs();

    // Auto queue accept button handler
    $('#queueaccept').change(function () {
        button_ready_check();
    })

    // Auto Lock-in button handler
    $('#lockin').change(function () {
        if (this.checked) {
            $("#firstpick").removeClass('disabled')
            $('#firstpospicks').removeClass('disabled')
        } else {
            $("#firstpick").addClass('disabled')
            $("#secondpick").addClass('disabled')
            $('#firstpospicks').addClass('disabled')
            $('#secondpospicks').addClass('disabled')
            $('#secondposbans').addClass('disabled')
            $('input[name=firstpos]:checked').prop('checked', false)
            $('input[name=secondpos]:checked').prop('checked', false)
        }

        button_ready_check();
    })

    // Auto Ban button handler
    $('#ban').change(function () {
        if (this.checked) {
            $('#firstposbans').removeClass('disabled')
            if ($('input[name=firstpos]:checked').val() != 'FILL' && $('input[name=firstpos]:checked').val() != undefined) {
                console.log($('input[name=firstpos]:checked').val())
                $('#secondposbans').removeClass('disabled')
            }
        } else {
            $('#firstposbans').addClass('disabled')
            $('#secondposbans').addClass('disabled')
        }

        button_ready_check();
    })

    // On firstpos change
    $('#firstpos input').on('change', function () {
        if ($('input[name=firstpos]:checked').val() != 'FILL') {
            $("#secondpick").removeClass('disabled')
            $('#secondpospicks').removeClass('disabled')
            if ($('#ban').is(':checked')) {
                $('#secondposbans').removeClass('disabled')
            }
        } else {
            $("#secondpick").addClass('disabled')
            $('#secondpospicks').addClass('disabled')
            $('#secondposbans').addClass('disabled')
        }

        button_ready_check();
    })

    // On secondpos change
    $('#secondpos input').on('change', function () {
        button_ready_check();
    })

    // On champ entry box change
    $('.champentrybox').on('input', function () {
        button_ready_check();
    })

    var autopilotReady = false;
    // State engine for input checks
    function button_ready_check() {
        // Is auto lock-in selected?
        if ($('#lockin').is(':checked')) {
            // Is first role selected?
            if ($('input[name=firstpos]:checked', '#firstpos').val() != undefined) {
                // Are first role champs selected?
                if ($('#firstpos_firstpick').val() && $('#firstpos_secondpick').val()) {
                    // Is first role fill?
                    if ($('input[name=firstpos]:checked', '#firstpos').val() == 'FILL') {
                        // Is auto ban selected?
                        if ($('#ban').is(':checked')) {
                            // Are first role bans selected?
                            if ($('#firstpos_firstban').val() && $('#firstpos_secondban').val()) {
                                // All ok, enable autopilot
                                autopilotReady = true;
                                $('#autopilot_status').text('Autopilot is ready');
                            } else {
                                autopilotReady = false;
                                $('#autopilot_status').text('Awaiting Ban selections...');
                            }
                        } else {
                            // All ok, enable autopilot
                            autopilotReady = true;
                            $('#autopilot_status').text('Autopilot is ready');
                        }
                    } else {
                        // Is second role selected?
                        if ($('input[name=secondpos]:checked', '#secondpos').val() != undefined) {
                            // Is second role different from first role?
                            if ($('input[name=secondpos]:checked', '#secondpos').val() != $('input[name=firstpos]:checked', '#firstpos').val()) {
                                // Are second role champs selected?
                                if ($('#secondpos_firstpick').val() && $('#secondpos_secondpick').val()) {
                                    // Is auto ban selected?
                                    if ($('#ban').is(':checked')) {
                                        // Are all bans selected?
                                        if ($('#firstpos_firstban').val() && $('#firstpos_secondban').val() && $('#secondpos_firstban').val() && $('#secondpos_secondban').val()) {
                                            // All ok, enable autopilot
                                            autopilotReady = true;
                                            $('#autopilot_status').text('Autopilot is ready');
                                        } else {
                                            autopilotReady = false;
                                            $('#autopilot_status').text('Awaiting ban selections...');
                                        }
                                    } else {
                                        // All ok, enable autopilot
                                        autopilotReady = true;
                                        $('#autopilot_status').text('Autopilot is ready');
                                    }
                                } else {
                                    autopilotReady = false;
                                    $('#autopilot_status').text('Awaiting secondary role pick selections...');
                                }
                            } else {
                                autopilotReady = false;
                                $('#autopilot_status').text('Secondary role must be different from primary...');
                            }
                        } else {
                            autopilotReady = false;
                            $('#autopilot_status').text('Awaiting secondary role selection...');
                        }
                    }
                } else {
                    autopilotReady = false;
                    $('#autopilot_status').text('Awaiting primary role pick selections...');
                }
            } else {
                autopilotReady = false;
                $('#autopilot_status').text('Awaiting primary role selection...');
            }
        } else {
            // Is auto ban selected?
            if ($('#ban').is(':checked')) {
                // Are two bans selected?
                if ($('#firstpos_firstban').val() && $('#firstpos_secondban').val()) {
                    // All ok, enable autopilot
                    autopilotReady = true;
                    $('#autopilot_status').text('Autopilot is ready');
                } else {
                    autopilotReady = false;
                    $('#autopilot_status').text('Awaiting ban selections...');
                }
            } else {
                // Is auto queue accept selected?
                if ($('#queueaccept').is(':checked')) {
                    autopilotReady = true;
                    $('#autopilot_status').text('Autopilot is ready');
                } else {
                    autopilotReady = false;
                    $('#autopilot_status').text('Awaiting selections...');
                }
            }
        }
    }

    // Expose progressbar and status text to python
    eel.expose(update_progressbar);
    function update_progressbar(value) {
        $('.progress__fill').css("width", `${value}%`);
        $('.progress__text').html(`${value}%`);
    }

    eel.expose(update_status_text);
    function update_status_text(value) {
        $('#autopilot_status').text(value);
    }

    // Expose selections
    eel.expose(is_autopilot_ready);
    function is_autopilot_ready() {
        return autopilotReady;
    }

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

    eel.expose(get_ban_preferences);
    function get_ban_preferences() {
        return [$('#firstpos_firstban').val(), $('#firstpos_secondban').val(), $('#secondpos_firstban').val(), $('#secondpos_secondban').val()]
    }

})