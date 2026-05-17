document.addEventListener("DOMContentLoaded", function () {

    // Notifications

    console.log("✅ Notification JS Loaded");

    // =============================
    // ELEMENTS
    // =============================
    const notifBtn = document.getElementById("notifBtn");
    const userBtn = document.getElementById("userBtn");

    const notifMenu = document.getElementById("notifMenu");
    const userMenu = document.getElementById("userMenu");

    const notifList = document.getElementById("notifList");
    const notifCount = document.getElementById("notifCount");

    const user_type = USER_TYPE;

    const NOTIF_URL = "/stationary/notifications/";
    const MARK_READ_URL = "/stationary/notifications/read/";

    const DELETE_URL = "/stationary/notifications/delete/";



    // =========================
    // GLOBAL STATE
    // =========================
    let selectedFiles = [];
    let redirectUrl = "";

    const MAX_FILES = 5;
    const MAX_FILE_SIZE = 5 * 1024 * 1024;

    const ALLOWED_TYPES = [
        "image/jpeg",
        "image/png",
        "image/jpg",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];

    // =========================
    // ELEMENTS
    // =========================
    const input = document.getElementById("fileInput");
    const container = document.getElementById("previewContainer");
    const form = document.getElementById("printingForm");
    const spinner = document.getElementById("loadingSpinner");

    const modal = document.getElementById("errorModal"); // single modal for all messages
    const modalTitle = modal.querySelector("h3");
    const modalMessage = document.getElementById("errorMessage");
    const modalCloseBtn = document.getElementById("closeErrorBtn");

    const activityActions = document.getElementById("activityActions");

    // =========================
    // HELPERS
    // =========================
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    function getFallbackUrl() {
        return activityActions?.dataset.dashboardUrl || "/";
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    }

    // =========================
    // MODAL FUNCTION
    // =========================
    function showMessage(title, message, callback = null) {
        modalTitle.textContent = title;
        modalMessage.textContent = message;
        modal.style.display = "block";

        // Close button handler
        modalCloseBtn.onclick = () => {
            modal.style.display = "none";
            if (callback) callback();
        };

        // Click outside modal closes
        window.onclick = function (e) {
            if (e.target === modal) {
                modal.style.display = "none";
                if (callback) callback();
            }
        };
    }

    // =========================
    // FILE INPUT HANDLER
    // =========================
    if (input) {
        input.addEventListener("change", function () {
            Array.from(this.files).forEach(file => {

                if (selectedFiles.length >= MAX_FILES) {
                    return showMessage("❌ Error", `Maximum ${MAX_FILES} files allowed.`);
                }

                if (file.size > MAX_FILE_SIZE) {
                    return showMessage("❌ Error", `${file.name} exceeds 5MB limit.`);
                }

                if (!ALLOWED_TYPES.includes(file.type)) {
                    return showMessage("❌ Error", `${file.name} is not supported.`);
                }

                selectedFiles.push(file);

                // =========================
                // FILE PREVIEW
                // =========================
                const fileHolder = document.createElement("div");
                fileHolder.style.float = "left";
                fileHolder.style.margin = "5px";
                fileHolder.style.width = "140px";
                fileHolder.style.position = "relative";

                const preview = document.createElement("div");
                preview.style.border = "1px solid #ccc";
                preview.style.borderRadius = "8px";
                preview.style.padding = "10px";
                preview.style.textAlign = "center";

                // ICON
                const icon = document.createElement("i");
                icon.style.fontSize = "30px";

                if (file.type.startsWith("image/")) {
                    icon.className = "fas fa-image";
                } else if (file.name.endsWith(".pdf")) {
                    icon.className = "fas fa-file-pdf";
                    icon.style.color = "#d9534f";
                } else if (file.name.endsWith(".docx")) {
                    icon.className = "fas fa-file-word";
                    icon.style.color = "#2B579A";
                } else {
                    icon.className = "fas fa-file";
                }

                // NAME + SIZE (with text overflow)
                const info = document.createElement("div");

                const name = document.createElement("div");
                name.textContent = file.name;
                name.style.fontSize = "12px";
                name.style.whiteSpace = "nowrap";
                name.style.overflow = "hidden";
                name.style.textOverflow = "ellipsis";
                name.style.width = "100%";
                name.title = file.name;

                const size = document.createElement("div");
                size.style.fontSize = "11px";
                size.style.color = "#777";
                size.textContent = formatFileSize(file.size);

                info.appendChild(name);
                info.appendChild(size);

                // PROGRESS BAR
                const progress = document.createElement("div");
                progress.style.height = "6px";
                progress.style.background = "#eee";
                progress.style.marginTop = "5px";
                progress.style.borderRadius = "4px";

                const bar = document.createElement("div");
                bar.style.height = "100%";
                bar.style.width = "0%";
                bar.style.background = "#2B579A";
                bar.style.borderRadius = "4px";

                progress.appendChild(bar);

                // REMOVE BUTTON
                const removeBtn = document.createElement("button");
                removeBtn.type = "button";
                removeBtn.textContent = "×";
                removeBtn.style.position = "absolute";
                removeBtn.style.top = "2px";
                removeBtn.style.right = "2px";
                removeBtn.style.border = "none";
                removeBtn.style.background = "transparent";
                removeBtn.style.cursor = "pointer";

                removeBtn.onclick = () => {
                    fileHolder.remove();
                    selectedFiles = selectedFiles.filter(f => f !== file);
                };

                preview.appendChild(icon);
                preview.appendChild(info);
                preview.appendChild(progress);

                fileHolder.appendChild(removeBtn);
                fileHolder.appendChild(preview);
                container.appendChild(fileHolder);

                file.progressBar = bar;
            });

            input.value = "";
        });
    }

    // =========================
    // FORM SUBMIT
    // =========================
    if (form) {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            if (selectedFiles.length === 0) {
                return showMessage("❌ Error", "Please attach at least one file.", () => {
                    document.getElementById("fileInput").focus();
                });
            }

            if (spinner) spinner.style.display = "flex";

            const formData = new FormData(form);
            selectedFiles.forEach(file => formData.append("files", file));

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "", true);
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());

            xhr.upload.onprogress = function (e) {
                if (e.lengthComputable) {
                    const percent = (e.loaded / e.total) * 100;
                    selectedFiles.forEach(file => {
                        if (file.progressBar) file.progressBar.style.width = percent + "%";
                    });
                }
            };

            xhr.onload = function () {
                if (spinner) spinner.style.display = "none";

                try {
                    const data = JSON.parse(xhr.responseText);

                    if (data.success) {
                        // ---------------------------
                        // WhatsApp Message
                        // ---------------------------
                        let message = `Hello, I have submitted service request, Please confirm the request.`;
                        const selected_s = document.querySelector('input[name="stationary_id"]:checked');
                        let s_phone = selected_s.getAttribute("data-phone");
                        s_phone = s_phone.replace(/^0/, '255');
                        let whatsappNumber = s_phone; // Stationary's WhatsApp number
                        let whatsappURL = `https://wa.me/${whatsappNumber}?text=${message}`;

                        redirectUrl = data.next_url;
                        showMessage("✅ Success", "Your activity request has been submitted successfully, wait for stationary confirmation.", () => {

                            window.open(whatsappURL, "_blank"); // open WhatsApp
                            window.location.href = redirectUrl || getFallbackUrl();

                        });


                    } else {
                        showMessage("❌ Error", data.message || "Something went wrong");
                    }
                } catch {
                    showMessage("❌ Error", "Invalid server response.");
                }
            };

            xhr.onerror = function () {
                if (spinner) spinner.style.display = "none";
                showMessage("❌ Error", "Upload failed. Try again.");
            };

            xhr.send(formData);
        });
    }

});

// =========================
// PAGE LOADER
// =========================
window.addEventListener("load", function () {
    const loader = document.getElementById("page-loader");
    if (loader) {
        loader.style.transition = "opacity 0.5s ease";
        loader.style.opacity = "0";
        setTimeout(() => loader.style.display = "none", 500);
    }
});



// Search stationary
const stationarySearch = document.getElementById("stationarySearch");
const noResultMsg = document.getElementById("noStationaryResult");

if (stationarySearch) {
    stationarySearch.addEventListener("input", function () {
        const query = this.value.toLowerCase();
        const items = document.querySelectorAll(".stationary-list-25 .option-25-1");

        let visibleCount = 0;

        items.forEach(item => {
            const text = item.innerText.toLowerCase();

            if (text.includes(query)) {
                item.style.display = "";
                visibleCount++;
            } else {
                item.style.display = "none";
            }
        });

        // Show/hide "No result found"
        if (noResultMsg) {
            noResultMsg.style.display = (visibleCount === 0) ? "block" : "none";
        }
    });
}


// Show map
// Open map modal
function openMap() {
    const selected = document.querySelector('input[name="stationary_id"]:checked');

    if (!selected) {
        alert("Please select a stationary first");
        return;
    }

    const lat = selected.getAttribute("data-lat");
    const lng = selected.getAttribute("data-lng");

    if (!lat || !lng) {
        alert("Location not available");
        return;
    }

    const mapFrame = document.getElementById("mapFrame");

    // Google Maps Embed with marker
    mapFrame.src = `https://maps.google.com/maps?q=${lat},${lng}&z=15&output=embed`;

    document.getElementById("mapModal").style.display = "flex";
}

// Close modal
function closeMap() {
    document.getElementById("mapModal").style.display = "none";
}

// Close when clicking outside
document.getElementById("mapModal").addEventListener("click", function (e) {
    if (e.target === this) {
        closeMap();
    }
});


// show button
// Get button
const viewMapBtn = document.getElementById("viewMapBtn");

// Listen for radio selection
document.querySelectorAll('input[name="stationary_id"]').forEach(radio => {
    radio.addEventListener("change", function () {
        if (this.checked) {
            viewMapBtn.style.display = "inline-block";
        }
    });
});


function updateMapButton() {
    const selected = document.querySelector('input[name="stationary_id"]:checked');
    viewMapBtn.style.display = selected ? "inline-block" : "none";
}

// Run once on load
document.addEventListener("DOMContentLoaded", updateMapButton);


