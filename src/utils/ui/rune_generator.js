$(document).ready(function () {
    $('#rune_generator_btn').on('click', function () {
        rune_generator();
    })

    async function rune_generator() {
        // Disable Button & reset progressbar
        $('#rune_generator_btn').prop('disabled', true);
        $('#rune_generator_btn').val("RUNNING");
        update_progress_bar(0);

        // Wait for champ select
        $('#rune_generator_status').html("Waiting for Champ Select");
        await eel.wait_for_champ_select()();
        update_progress_bar(10);

        // Wait for lock-in
        $('#rune_generator_status').html("Waiting for Lock-In");
        let champ = await eel.get_champion_pick()();
        update_progress_bar(20);

        // Generate and set rune page
        $('#rune_generator_status').html("Generating " + champ + " Runes...");
        await eel.set_rune_page(champ)();
        update_progress_bar(70);

        // Generate and set summoner spells
        $('#rune_generator_status').html("Generating " + champ + " Summoner Spells...");
        await eel.set_sum_spells(champ)();
        update_progress_bar(100);

        // Show completed
        $('#rune_generator_status').html(champ + " Runes & Spells Set!");

        // Re-enable Button
        $('#rune_generator_btn').prop('disabled', false);
        $('#rune_generator_btn').val("START");
    }

    // Progressbar handler
    function update_progress_bar(value) {
        $('.progress__fill').css("width", `${value}%`);
        $('.progress__text').html(`${value}%`);
    }
})