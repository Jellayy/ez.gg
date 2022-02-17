// Get Elements
let btn = document.querySelector("#sidebar-btn");
let sidebar = document.querySelector(".sidebar");

// Sidebar toggle handler
btn.onclick = function() {
    sidebar.classList.toggle("active");
}