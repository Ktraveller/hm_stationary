// ======================
// PREVIEW ACTIVITY JS
// ======================

document.addEventListener("DOMContentLoaded", () => {

    // ======== Progress Circles (Optional) ========
    const cards = document.querySelectorAll(".activity-card-12");
    const progressMap = {
        "pending": 20,
        "processing": 50,
        "completed": 80,
        "delivery": 100
    };
    const colorMap = {
        "pending": "#f0ad4e",
        "processing": "#0275d8",
        "completed": "#5cb85c",
        "delivery": "#d9534f"
    };

    cards.forEach(card => {
        const status = card.dataset.status;
        const progress = progressMap[status] || 0;
        const circle = card.querySelector(".progress-circle circle:nth-child(2)");
        const text = card.querySelector(".progress-circle text");
        if (!circle || !text) return;

        const radius = circle.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;

        circle.style.strokeDasharray = circumference;
        circle.style.strokeDashoffset = circumference * (1 - progress / 100);
        circle.style.stroke = colorMap[status] || "#4caf50";

        text.textContent = progress + "%";
    });

    // ======================
    // File Preview Modal
    // ======================
    window.openModal = function(url) {
        const modal = document.getElementById("fileModal");
        const content = document.getElementById("fileModalContent");
        if (!modal || !content) return;
        content.innerHTML = '<span onclick="closeModal()" style="float:right;cursor:pointer;font-size:20px">&times;</span>';
        const img = document.createElement("img");
        img.src = url;
        img.style.maxWidth = "90%";
        img.style.maxHeight = "90vh";
        content.appendChild(img);
        modal.style.display = "flex";
    }

    window.closeModal = function() {
        const modal = document.getElementById("fileModal");
        if (modal) modal.style.display = "none";
    }

});
