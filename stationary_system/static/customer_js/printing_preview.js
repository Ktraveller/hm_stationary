document.addEventListener("DOMContentLoaded", function () {

    // =============================
    // ELEMENTS
    // =============================
    const notifBtn = document.getElementById("notifBtn");
    const userBtn = document.getElementById("userBtn");

    const notifMenu = document.getElementById("notifMenu");
    const userMenu = document.getElementById("userMenu");

    const notifList = document.getElementById("notifList");
    const notifCount = document.getElementById("notifCount");

    const user_type = (typeof USER_TYPE !== "undefined") ? USER_TYPE : "customer";

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
    // PAGE ELEMENTS
    // =========================
    const input = document.getElementById("fileInput");
    const container = document.getElementById("previewContainer");
    const form = document.getElementById("printingForm");
    const spinner = document.getElementById("loadingSpinner");

    const errorModal = document.getElementById("errorModal");
    const errorTitle = errorModal ? errorModal.querySelector("h3") : null;
    const errorMessage = document.getElementById("errorMessage");
    const errorCloseBtn = document.getElementById("closeErrorBtn");

    const activityActions = document.getElementById("activityActions");

    const fileModal = document.getElementById("fileModal");
    const fileModalContent = document.getElementById("fileModalContent");

    const optionsSection = document.getElementById("options_100");

    // =========================
    // HELPERS
    // =========================
    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
    }

    function getFallbackUrl() {
        return activityActions?.dataset.dashboardUrl || "/";
    }

    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
        return (bytes / (1024 * 1024)).toFixed(1) + " MB";
    }

    function fileIconClass(file) {
        if (file.type.startsWith("image/")) return { cls: "fas fa-image", color: "" };
        if (file.name.toLowerCase().endsWith(".pdf")) return { cls: "fas fa-file-pdf", color: "#dc2626" };
        if (file.name.toLowerCase().endsWith(".docx")) return { cls: "fas fa-file-word", color: "#2563eb" };
        return { cls: "fas fa-file", color: "#64748b" };
    }

    // =========================
    // MODAL (error / success)
    // =========================
    function showMessage(title, message, callback = null) {
        if (!errorModal) return;
        if (errorTitle) errorTitle.textContent = title;
        errorMessage.textContent = message;
        errorModal.style.display = "block";

        const closeHandler = () => {
            errorModal.style.display = "none";
            if (callback) callback();
        };

        errorCloseBtn.onclick = closeHandler;

        window.onclick = function (e) {
            if (e.target === errorModal) closeHandler();
        };
    }

    // =========================
    // IMAGE LIGHTBOX
    // =========================
    function openFileModal(src) {
        if (!fileModal || !fileModalContent) return;
        fileModalContent.innerHTML = "";

        const img = document.createElement("img");
        img.src = src;
        img.alt = "Preview";

        const closeBtn = document.createElement("span");
        closeBtn.innerHTML = "&times;";
        closeBtn.setAttribute("aria-label", "Close preview");
        closeBtn.onclick = closeFileModal;

        fileModalContent.appendChild(img);
        fileModalContent.appendChild(closeBtn);
        fileModal.style.display = "flex";
    }

    function closeFileModal() {
        if (fileModal) fileModal.style.display = "none";
    }

    if (fileModal) {
        fileModal.addEventListener("click", function (e) {
            if (e.target === fileModal) closeFileModal();
        });
        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape") closeFileModal();
        });
    }

    // =========================
    // EMPTY HINT
    // =========================
    function showEmptyHint() {
        if (!container) return;
        if (container.querySelector(".file-holder-18")) return;
        const hint = document.createElement("p");
        hint.className = "empty-hint";
        hint.innerHTML = '<i class="fas fa-paperclip"></i> No files attached yet';
        container.appendChild(hint);
    }

    function hideEmptyHint() {
        const hint = container?.querySelector(".empty-hint");
        if (hint) hint.remove();
    }

    // =========================
    // FILE INPUT
    // =========================
    if (input && container) {
        input.addEventListener("change", function () {
            Array.from(this.files).forEach((file) => {

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

                if (optionsSection) optionsSection.style.display = "block";
                hideEmptyHint();

                // ---------- BUILD CARD WITH CLASSES ----------
                const fileHolder = document.createElement("div");
                fileHolder.className = "file-holder-18";

                const preview = document.createElement("div");
                preview.className = "file-preview-15";

                // Thumbnail or icon
                if (file.type.startsWith("image/")) {
                    const img = document.createElement("img");
                    img.src = URL.createObjectURL(file);
                    img.alt = file.name;
                    preview.appendChild(img);
                    preview.classList.add("is-clickable");
                    preview.addEventListener("click", (e) => {
                        if (e.target.closest("button")) return;
                        openFileModal(URL.createObjectURL(file));
                    });
                } else {
                    const info = fileIconClass(file);
                    const icon = document.createElement("i");
                    icon.className = info.cls;
                    if (info.color) icon.style.color = info.color;
                    preview.appendChild(icon);
                }

                // Name
                const name = document.createElement("div");
                name.className = "file-name";
                name.textContent = file.name;
                name.title = file.name;
                preview.appendChild(name);

                // Size
                const size = document.createElement("div");
                size.className = "file-size";
                size.textContent = formatFileSize(file.size);
                preview.appendChild(size);

                // Progress
                const progress = document.createElement("div");
                progress.className = "file-progress";
                const bar = document.createElement("div");
                bar.className = "file-progress-bar";
                progress.appendChild(bar);
                preview.appendChild(progress);

                // Remove button
                const removeBtn = document.createElement("button");
                removeBtn.type = "button";
                removeBtn.innerHTML = "&times;";
                removeBtn.setAttribute("aria-label", "Remove file");
                removeBtn.onclick = (e) => {
                    e.stopPropagation();
                    fileHolder.remove();
                    selectedFiles = selectedFiles.filter((f) => f !== file);

                    if (selectedFiles.length === 0) {
                        if (optionsSection) optionsSection.style.display = "none";
                        showEmptyHint();
                    }
                };

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
                    input?.focus();
                });
            }

            const selectedStationary = document.querySelector('input[name="stationary_id"]:checked');
            if (!selectedStationary) {
                return showMessage("❌ Error", "Please choose a stationary.");
            }

            if (spinner) spinner.style.display = "flex";

            const formData = new FormData(form);
            selectedFiles.forEach((file) => formData.append("files", file));

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "", true);
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());

            xhr.upload.onprogress = function (e) {
                if (e.lengthComputable) {
                    const percent = (e.loaded / e.total) * 100;
                    selectedFiles.forEach((file) => {
                        if (file.progressBar) file.progressBar.style.width = percent + "%";
                    });
                }
            };

            xhr.onload = function () {
                if (spinner) spinner.style.display = "none";

                let data;
                try {
                    data = JSON.parse(xhr.responseText);
                } catch {
                    return showMessage("❌ Error", "Invalid server response.");
                }

                if (!data.success) {
                    return showMessage("❌ Error", data.message || "Something went wrong");
                }

                // Build WhatsApp link
                const s_phone_raw = selectedStationary.getAttribute("data-phone") || "";
                const whatsappNumber = s_phone_raw.replace(/^0/, "255");
                const message = "Hello, I have submitted a service request. Please confirm the request.";
                const whatsappURL = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(message)}`;

                redirectUrl = data.next_url;

                showMessage(
                    "✅ Success",
                    "Your activity request has been submitted successfully. Wait for stationary confirmation.",
                    () => {
                        window.open(whatsappURL, "_blank");
                        window.location.href = redirectUrl || getFallbackUrl();
                    }
                );
            };

            xhr.onerror = function () {
                if (spinner) spinner.style.display = "none";
                showMessage("❌ Error", "Upload failed. Try again.");
            };

            xhr.send(formData);
        });
    }

    // =========================
    // MAP BUTTON VISIBILITY
    // =========================
    function updateMapButton() {
        const viewMapBtn = document.getElementById("viewMapBtn");
        if (!viewMapBtn) return;
        const selected = document.querySelector('input[name="stationary_id"]:checked');
        viewMapBtn.style.display = selected ? "inline-flex" : "none";
    }

    document.querySelectorAll('input[name="stationary_id"]').forEach((radio) => {
        radio.addEventListener("change", function () {
            if (this.checked) updateMapButton();
        });
    });

    updateMapButton();
});

// =========================
// PAGE LOADER
// =========================
window.addEventListener("load", function () {
    const loader = document.getElementById("page-loader");
    if (loader) {
        loader.style.transition = "opacity 0.5s ease";
        loader.style.opacity = "0";
        setTimeout(() => (loader.style.display = "none"), 500);
    }
});

// =========================
// STATIONARY SEARCH
// =========================
const stationarySearch = document.getElementById("stationarySearch");
const noResultMsg = document.getElementById("noStationaryResult");

if (stationarySearch) {
    stationarySearch.addEventListener("input", function () {
        const query = this.value.toLowerCase().trim();
        const items = document.querySelectorAll(".stationary-list-25 .option-25-1");
        let visibleCount = 0;

        items.forEach((item) => {
            const text = item.innerText.toLowerCase();
            if (text.includes(query)) {
                item.style.display = "";
                visibleCount++;
            } else {
                item.style.display = "none";
            }
        });

        if (noResultMsg) {
            noResultMsg.style.display = visibleCount === 0 ? "flex" : "none";
        }
    });
}

// =========================
// MAP MODAL
// =========================
function openMap() {
    const selected = document.querySelector('input[name="stationary_id"]:checked');
    if (!selected) {
        return alert("Please select a stationary first");
    }

    const lat = selected.getAttribute("data-lat");
    const lng = selected.getAttribute("data-lng");
    if (!lat || !lng) {
        return alert("Location not available");
    }

    const mapFrame = document.getElementById("mapFrame");
    if (mapFrame) {
        mapFrame.src = `https://maps.google.com/maps?q=${lat},${lng}&z=15&output=embed`;
    }
    document.getElementById("mapModal").style.display = "flex";
}

function closeMap() {
    document.getElementById("mapModal").style.display = "none";
}

const mapModalEl = document.getElementById("mapModal");
if (mapModalEl) {
    mapModalEl.addEventListener("click", function (e) {
        if (e.target === this) closeMap();
    });
}