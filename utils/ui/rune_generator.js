$(document).ready(function() {
    $('#rune_generator_btn').on('click', function() {
        rune_generator();
    })

    async function rune_generator() {
        // Disable Button
        $('#rune_generator_btn').prop('disabled', true);
        $('#rune_generator_btn').val("RUNNING");

        // Display Progress
        $('#rune_generator_status').html("Waiting for Champ Select");
        await eel.wait_for_champ_select()();
        $('#rune_generator_status').html("Waiting for Lock-In");
        let champ = await eel.get_champion_pick()();
        $('#rune_generator_status').html("Generating " + champ + " Runes...");
        await eel.set_rune_page(champ)();
        $('#rune_generator_status').html("Generating " + champ + " Summoner Spells...");
        await eel.set_sum_spells(champ)();
        $('#rune_generator_status').html(champ + " Runes & Spells Set!");

        // Re-enable Button
        $('#rune_generator_btn').prop('disabled', false);
        $('#rune_generator_btn').val("START");



    }
})