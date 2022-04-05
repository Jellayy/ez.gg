// Add animations after load
setTimeout(function () {
    document.body.className = "";
}, 500);

// Get Elements
let btn = document.querySelector("#sidebar-btn");
let sidebar = document.querySelector(".sidebar");

// Sidebar toggle handler
btn.onclick = function () {
    sidebar.classList.toggle("active");
}