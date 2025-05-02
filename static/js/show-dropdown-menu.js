document.addEventListener("DOMContentLoaded", () => {
    const menuIcon = document.getElementById("menu-icon");
    const dropdownMenu = document.getElementById("dropdown-menu");

    menuIcon.addEventListener("click", () => {
        dropdownMenu.style.display =
            dropdownMenu.style.display === "flex" ? "none" : "flex";
    });

    document.addEventListener("click", (event) => {
        if (!menuIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.style.display = "none";
        }
    });
});
