$(document).ready(function() {
    $('#rune_generator_button').on('click', function() {
        rune_generator();
    })

    async function rune_generator() {
        let n = await eel.rune_generator()();
        console.log(n)
    }
})