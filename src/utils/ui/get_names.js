$(document).ready(function () {
    $("#get-names-btn").on("click", async function () {
        const names = await eel.get_ranked_names()();
        const namesList = $("#names-list");
        namesList.empty(); // Clear the list before adding new names
    
        names.forEach((name) => {
            const listItem = $("<li>").text(name);
            namesList.append(listItem);
        });
    });

    $("#get-names-btn").on("click", async function () {
        const names = await eel.get_ranked_names()();
        const namesList = $("#names-list");
        namesList.empty(); // Clear the list before adding new names
    
        names.forEach((name) => {
            const listItem = $("<li>").text(name);
            namesList.append(listItem);
        });
    
        // Show the button and set the redirection URL
        const gotoMultisearchBtn = $("#goto-multisearch-btn");
        const namesUrl = names.map((name) => name.replace(/ /g, "%20")).join(",");
        gotoMultisearchBtn.attr("hidden", false);
        gotoMultisearchBtn.on("click", function () {
            window.open(`https://u.gg/multisearch?summoners=${namesUrl}&region=na1`, "_blank");
        });
    });

    function displayNames(names) {
        const container = $("#names-container");
        container.empty(); // Clear the container before displaying new names

        names.forEach((name) => {
            const nameDiv = $("<div>").text(name);
            container.append(nameDiv);
        });
    }
});
