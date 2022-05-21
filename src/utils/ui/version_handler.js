$(document).ready(function () {

    // Function to compare version numbers
    function versionCompare(v1, v2, options) {
        var lexicographical = options && options.lexicographical,
            zeroExtend = options && options.zeroExtend,
            v1parts = v1.split('.'),
            v2parts = v2.split('.');
    
        function isValidPart(x) {
            return (lexicographical ? /^\d+[A-Za-z]*$/ : /^\d+$/).test(x);
        }
    
        if (!v1parts.every(isValidPart) || !v2parts.every(isValidPart)) {
            return NaN;
        }
    
        if (zeroExtend) {
            while (v1parts.length < v2parts.length) v1parts.push("0");
            while (v2parts.length < v1parts.length) v2parts.push("0");
        }
    
        if (!lexicographical) {
            v1parts = v1parts.map(Number);
            v2parts = v2parts.map(Number);
        }
    
        for (var i = 0; i < v1parts.length; ++i) {
            if (v2parts.length == i) {
                return 1;
            }
    
            if (v1parts[i] == v2parts[i]) {
                continue;
            }
            else if (v1parts[i] > v2parts[i]) {
                return 1;
            }
            else {
                return -1;
            }
        }
    
        if (v1parts.length != v2parts.length) {
            return -1;
        }
    
        return 0;
    }

    // Update page title with version number
    async function update_title() {
        var currentVersion = await eel.get_version()();
        $(document).prop('title', `EZ.GG ${currentVersion}`)
    }
    update_title()

    // AJAX call to github for latest release number
    $.ajax({
        url: "https://api.github.com/repos/jellayy/ez.gg/releases/latest",
        type: "GET",
        success: async function(result) {
            var currentVersion = await eel.get_version()();
            var currentVersion = currentVersion.replace(/[^0-9\.]+/g,"");

            // Extract version number from result
            var latestVersion = result["name"].replace(/[^0-9\.]+/g,"");
            
            if (versionCompare(latestVersion, currentVersion) == 1) {
                $('.update-banner').attr("hidden", false)
                $('#update_description').html(`EZ.GG version ${latestVersion} is available on GitHub, please update for the latest features and fixes!`)
            }
        },
        error: function(error) {
            console.log(`Error while calling github API: ${error}`)
        }
    })

})