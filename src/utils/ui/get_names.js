$(document).ready(function () {
    document.getElementById("get-names-btn").addEventListener("click", async function () {
        const names = await eel.get_ranked_names()();
        const namesList = document.getElementById("names-list");
        namesList.innerHTML = ""; // Clear the list before adding new names
    
        names.forEach((name) => {
            const listItem = document.createElement("li");
            listItem.textContent = name;
            namesList.appendChild(listItem);
        });
    });    

    document.getElementById("get-names-btn").addEventListener("click", async function () {
        const names = await eel.get_ranked_names()();
        const namesList = document.getElementById("names-list");
        namesList.innerHTML = ""; // Clear the list before adding new names
    
        names.forEach((name) => {
            const listItem = document.createElement("li");
            listItem.textContent = name;
            namesList.appendChild(listItem);
        });
    
        // Show the button and set the redirection URL
        const gotoMultisearchBtn = document.getElementById("goto-multisearch-btn");
        const namesUrl = names.map((name) => name.replace(/ /g, "%20")).join(",");
        gotoMultisearchBtn.setAttribute("hidden", false);
        gotoMultisearchBtn.onclick = function () {
            window.open(`https://u.gg/multisearch?summoners=${namesUrl}&region=na1`, "_blank");
        };
    });    

    function displayNames(names) {
        const container = document.getElementById("names-container");
        container.innerHTML = ""; // Clear the container before displaying new names

        names.forEach((name) => {
            const nameDiv = document.createElement("div");
            nameDiv.textContent = name;
            container.appendChild(nameDiv);
        });
    }
});
