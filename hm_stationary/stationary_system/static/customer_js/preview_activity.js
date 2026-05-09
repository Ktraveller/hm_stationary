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

    // ======================
    // Delete Activity
    // ======================
    const confirmModal = document.getElementById("confirmDeleteModal");
    const confirmBtn = document.getElementById("confirmDeleteBtn");
    const cancelBtn = document.getElementById("cancelDeleteBtn");
    const messageModal = document.getElementById("messageModal");
    const messageText = document.getElementById("messageText");
    const closeMessageBtn = document.getElementById("closeMessageBtn");

    if (!confirmModal || !confirmBtn || !cancelBtn || !messageModal || !messageText || !closeMessageBtn) {
        console.error("Delete or message modal elements missing!");
        return;
    }

    let selectedActivityId = null;
    let selectedButton = null;

    // Attach delete button clicks
    document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", () => {
            selectedActivityId = btn.dataset.activityId;
            selectedButton = btn;
            confirmModal.style.display = "flex";
        });
    });

    // Cancel deletion
    cancelBtn.addEventListener("click", () => {
        confirmModal.style.display = "none";
        selectedActivityId = null;
        selectedButton = null;
    });

    // Confirm deletion
    confirmBtn.addEventListener("click", () => {
        if (!selectedActivityId) return;

        const csrf = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrf) {
            alert("CSRF token not found. Cannot delete activity.");
            return;
        }

        const xhr = new XMLHttpRequest();
        xhr.open("POST", `/stationary/customer/delete-pending-activity/${selectedActivityId}/`, true);
        xhr.setRequestHeader("X-CSRFToken", csrf.value);

        xhr.onload = function () {
            confirmModal.style.display = "none";
            if (xhr.status === 200) {
                const data = JSON.parse(xhr.responseText);
                if (data.success) {
                    // Remove card from DOM
                    if (selectedButton) {
                        const card = selectedButton.closest(".activity-card-12");
                        if (card) card.remove();
                    }
                    // Show success message and redirect to dashboard on OK
                    showMessage("Activity deleted successfully.", DASHBOARD_URL);
                } else {
                    showMessage(data.error || "Error deleting activity.");
                }
            } else {
                showMessage("Server error. Try again.");
            }
            selectedActivityId = null;
            selectedButton = null;
        };

        xhr.onerror = function () {
            confirmModal.style.display = "none";
            showMessage("Request failed. Try again.");
            selectedActivityId = null;
            selectedButton = null;
        };

        xhr.send();
    });

    // ======================
    // Show message modal with optional redirect
    // ======================
    function showMessage(msg, redirectUrl = null) {
        messageText.textContent = msg;
        messageModal.style.display = "flex";

        closeMessageBtn.onclick = () => {
            messageModal.style.display = "none";
            if (redirectUrl) {
                window.location.href = redirectUrl;
            }
        };
    }

    // Close message modal if click outside content
    [confirmModal, messageModal].forEach(modal => {
        modal.addEventListener("click", e => {
            if (e.target === modal) modal.style.display = "none";
        });
    });

});

