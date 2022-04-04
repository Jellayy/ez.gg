$(document).ready(function() {

    async function get_summoner_info() {
        let summoner = await eel.get_summoner_info()();
        console.log(summoner)
        $('#test').text(summoner['displayName'] + " | Level: " + summoner['summonerLevel'] + " | Profile Icon: " + summoner['profileIconId']);
    }
    get_summoner_info();

})