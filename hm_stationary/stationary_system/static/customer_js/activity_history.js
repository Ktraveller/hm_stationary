
// Containers for different activity statuses
const statusContainers = {
    all: document.getElementById("all"),
    pending: document.getElementById("pending"),
    processing: document.getElementById("processing"),
    completed: document.getElementById("completed")
};

// Filter buttons
const filterButtons = document.querySelectorAll(".filter-btn");

// Switch visible container and set active button
function switch_activity(status) {
    for (let key in statusContainers) {
        statusContainers[key].style.display = (key === status) ? "block" : "none";
    }

    // Set active button style
    filterButtons.forEach(btn => btn.classList.remove("active-110"));
    const activeBtn = document.querySelector(`.filter-btn[onclick="switch_activity('${status}')"]`);
    if (activeBtn) activeBtn.classList.add("active-110");

    // Clear search input when switching
    const searchInput = document.getElementById("activitySearch");
    if (searchInput) {
        searchInput.value = "";
        filter_activities();
    }
}

// Search function: filter cards inside the visible container
function filter_activities() {
    const query = document.getElementById("activitySearch").value.toLowerCase();
    const visibleContainer = Object.values(statusContainers).find(c => c.style.display !== "none");
    if (!visibleContainer) return;

    const cards = visibleContainer.querySelectorAll(".activity-card-12");
    cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        // Use "block" to preserve layout
        card.style.display = text.includes(query) ? "block" : "none";
    });
}

// Attach event to search input
const searchInput = document.getElementById("activitySearch");
if (searchInput) {
    searchInput.addEventListener("input", filter_activities);
}

// Initialize page
document.addEventListener("DOMContentLoaded", () => switch_activity("all"));

