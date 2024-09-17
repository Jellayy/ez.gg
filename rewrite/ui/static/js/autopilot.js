document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('championForm');
    const rolesContainer = document.getElementById('roles');
    const roleTemplate = document.getElementById('roleTemplate');
    const banTemplate = document.getElementById('banTemplate');
    const pickTemplate = document.getElementById('pickTemplate');

    const roles = ['top', 'jungle', 'mid', 'adc', 'support'];
    let allChampions = [];


    // Function to fetch all champion names
    async function fetchAllChampions() {
        try {
            const response = await fetch('/autopilot/all_champions_list');
            allChampions = await response.json();
            console.log('All champions loaded:', allChampions.length);
        } catch (error) {
            console.error('Error fetching all champions:', error);
        }
    }


    // Function to create role sections
    function createRoleSections() {
        roles.forEach(role => {
            const roleSection = roleTemplate.content.cloneNode(true);
            roleSection.querySelector('h2').textContent = role.charAt(0).toUpperCase() + role.slice(1);
            
            const addBanBtn = roleSection.querySelector('.add-ban');
            addBanBtn.addEventListener('click', () => addBan(role));

            const addPickBtn = roleSection.querySelector('.add-pick');
            addPickBtn.addEventListener('click', () => addPick(role));

            rolesContainer.appendChild(roleSection);
        });
    }


    // Function to add a ban
    function addBan(role) {
        const banList = document.querySelector(`#roles > div:nth-child(${roles.indexOf(role) + 1}) .ban-list`);
        const banItem = banTemplate.content.cloneNode(true);
        
        const removeBtn = banItem.querySelector('.remove-ban');
        removeBtn.addEventListener('click', (e) => {
            e.target.closest('.ban-item').remove();
            sendFormData();
        });

        const championInput = banItem.querySelector('.champion-input');
        setupChampionAutocomplete(championInput);

        banList.appendChild(banItem);
    }


    // Function to add a pick
    function addPick(role) {
        const pickList = document.querySelector(`#roles > div:nth-child(${roles.indexOf(role) + 1}) .pick-list`);
        const pickItem = pickTemplate.content.cloneNode(true);
        
        const removeBtn = pickItem.querySelector('.remove-pick');
        removeBtn.addEventListener('click', (e) => {
            e.target.closest('.pick-item').remove();
            sendFormData();
        });

        const championInput = pickItem.querySelector('.champion-input');
        setupChampionAutocomplete(championInput);

        const summonerSpells = pickItem.querySelectorAll('.summoner-spell');
        summonerSpells.forEach(select => {
            select.addEventListener('change', sendFormData);
        });

        pickList.appendChild(pickItem);
    }


    // Function to set up champion autocomplete
    function setupChampionAutocomplete(input) {
        const datalist = document.createElement('datalist');
        datalist.id = `champions-${Math.random().toString(36).substr(2, 9)}`;
        input.setAttribute('list', datalist.id);
        input.insertAdjacentElement('afterend', datalist);

        input.addEventListener('input', debounce(() => {
            const query = input.value.toLowerCase();
            
            // Clear existing options
            datalist.innerHTML = '';

            // Add matching champions to datalist
            allChampions.filter(champion => champion.toLowerCase().includes(query))
                .forEach(champion => {
                    const option = document.createElement('option');
                    option.value = champion;
                    datalist.appendChild(option);
                });
        }, 100));

        input.addEventListener('change', sendFormData);
    }


    // Debounce function to limit updates
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }


    // Function to send form data to server
    function sendFormData() {
        const formData = {
            auto_queue_accept: document.getElementById('auto_queue_accept').checked,
            auto_champion_ban: document.getElementById('auto_champion_ban').checked,
            auto_champion_lock_in: document.getElementById('auto_champion_lock_in').checked
        };

        roles.forEach(role => {
            formData[role] = {
                bans: [],
                picks: []
            };

            const roleSection = document.querySelector(`#roles > div:nth-child(${roles.indexOf(role) + 1})`);
            
            roleSection.querySelectorAll('.ban-item .champion-input').forEach(input => {
                if (input.value) formData[role].bans.push(input.value);
            });

            roleSection.querySelectorAll('.pick-item').forEach(pickItem => {
                const champion = pickItem.querySelector('.champion-input').value;
                const summonerSpells = Array.from(pickItem.querySelectorAll('.summoner-spell'))
                    .map(select => select.value)
                    .filter(value => value !== '' && value !== 'Select Spell');

                // Only add the pick if the champion is selected and exactly two valid summoner spells are chosen
                if (champion && summonerSpells.length === 2) {
                    formData[role].picks.push({
                        champion: champion,
                        summoner_spells: summonerSpells
                    });
                }
            });
        });

        fetch('/autopilot/update_settings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => console.log('Settings saved:', data))
        .catch(error => console.error('Error saving settings:', error));
    }


    // Function to load existing settings
    async function loadSettings() {
        try {
            const response = await fetch('/autopilot/load_settings');
            const settings = JSON.parse(await response.json());

            document.getElementById('auto_queue_accept').checked = settings.auto_queue_accept;
            document.getElementById('auto_champion_ban').checked = settings.auto_champion_ban;
            document.getElementById('auto_champion_lock_in').checked = settings.auto_champion_lock_in;

            roles.forEach(role => {
                const roleData = settings[role];
                if (roleData) {
                    roleData.bans.forEach(() => addBan(role));
                    roleData.picks.forEach(() => addPick(role));

                    const roleSection = document.querySelector(`#roles > div:nth-child(${roles.indexOf(role) + 1})`);
                    const banInputs = roleSection.querySelectorAll('.ban-item .champion-input');
                    const pickItems = roleSection.querySelectorAll('.pick-item');

                    roleData.bans.forEach((ban, index) => {
                        if (banInputs[index]) banInputs[index].value = ban;
                    });

                    roleData.picks.forEach((pick, index) => {
                        if (pickItems[index]) {
                            const championInput = pickItems[index].querySelector('.champion-input');
                            const summonerSpells = pickItems[index].querySelectorAll('.summoner-spell');

                            championInput.value = pick.champion;
                            pick.summoner_spells.forEach((spell, spellIndex) => {
                                if (summonerSpells[spellIndex]) summonerSpells[spellIndex].value = spell;
                            });
                        }
                    });
                }
            });
        } catch (error) {
            console.error('Error loading settings:', error);
        }
    }


    // Initialize the form
    async function initForm() {
        await fetchAllChampions(); // Fetch all champions first
        createRoleSections();
        await loadSettings();
    }
    initForm();


    // Add event listeners for form changes
    form.addEventListener('change', (e) => {
        if (e.target.matches('#auto_queue_accept, #auto_champion_ban, #auto_champion_lock_in')) {
            sendFormData();
        }
    });
});