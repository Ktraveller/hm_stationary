document.addEventListener("DOMContentLoaded", () => {

    // -------------------------------
    // ELEMENTS
    // -------------------------------
    const form = document.getElementById("editForm");
    const previewContainer = document.getElementById("previewContainer");
    const messageModal = document.getElementById("messageModal");
    const messageText = document.getElementById("messageText");
    const closeMessageBtn = document.getElementById("closeMessageBtn");
    const fileInput = document.getElementById("fileInput");
    const updateBtn = document.getElementById("update-btn");
    const btnLoader = document.getElementById("btn-loader");
    const progressContainer = document.getElementById("upload-progress-container");
    const progressBar = document.getElementById("upload-progress-bar");

    let selectedFiles = [];

    // -------------------------------
    // FILE VALIDATION CONFIG
    // -------------------------------
    const MAX_FILES = 5;
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
    const ALLOWED_TYPES = [
        "image/jpeg", "image/png", "image/jpg",
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ];

    let modalRedirectUrl = null;

    // -------------------------------
    // MODAL FUNCTION
    // -------------------------------
    function showMessage(message, redirectUrl = null) {
        messageText.textContent = message;
        messageModal.style.display = "flex";
        modalRedirectUrl = redirectUrl;
    }

    closeMessageBtn.addEventListener("click", () => {
        messageModal.style.display = "none";
        if (modalRedirectUrl) {
            window.location.href = modalRedirectUrl;
        }
    });

    messageModal.addEventListener("click", e => {
        if (e.target === messageModal) {
            messageModal.style.display = "none";
            if (modalRedirectUrl) {
                window.location.href = modalRedirectUrl;
            }
        }
    });

    // -------------------------------
    // REMOVE EXISTING FILE (AJAX)
    // -------------------------------
    previewContainer.addEventListener("click", e => {
        const removeBtn = e.target.closest(".remove-existing-file");
        if (!removeBtn) return;

        const card = removeBtn.closest(".file-card");
        const fileId = card.dataset.fileId;

        btnLoader.style.display = "inline-block";
        progressContainer.style.display = "block";
        progressBar.style.width = "0%";

        let percent = 0;
        const fakeProgress = setInterval(() => {
            percent += 10;
            if (percent > 80) percent = 80;
            progressBar.style.width = percent + "%";
        }, 50);

        fetch(`/customer/delete-uploaded-file/${fileId}/`, {
            method: "POST",
            headers: { "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value }
        })
        .then(res => res.json())
        .then(data => {
            clearInterval(fakeProgress);
            progressBar.style.width = "100%";
            setTimeout(() => {
                progressContainer.style.display = "none";
                btnLoader.style.display = "none";
            }, 200);

            if (data.success) card.remove();
            else showMessage(data.error || "Cannot remove file");
        })
        .catch(() => {
            clearInterval(fakeProgress);
            progressContainer.style.display = "none";
            btnLoader.style.display = "none";
            showMessage("Failed to remove file. Try again.");
        });
    });

    // -------------------------------
    // ADD NEW FILES & PREVIEW WITH VALIDATION
    // -------------------------------
    fileInput.addEventListener("change", () => {
        const newFiles = Array.from(fileInput.files);

        newFiles.forEach(file => {

            // -------- VALIDATION --------
            if (selectedFiles.length >= MAX_FILES) {
                showMessage(`Maximum ${MAX_FILES} files allowed.`);
                return;
            }

            if (file.size > MAX_FILE_SIZE) {
                showMessage(`${file.name} exceeds 5MB limit.`);
                return;
            }

            if (!ALLOWED_TYPES.includes(file.type)) {
                showMessage(`${file.name} type is not supported.`);
                return;
            }

            // Add valid file
            selectedFiles.push(file);

            // -------- PREVIEW --------
            const card = document.createElement("div");
            card.className = "file-card";

            if (file.type.startsWith("image/")) {
                const img = document.createElement("img");
                img.src = URL.createObjectURL(file);
                card.appendChild(img);
            } else {
                const icon = document.createElement("div");
                icon.className = "file-icon";
                icon.textContent = "📄";
                card.appendChild(icon);
            }

            const p = document.createElement("p");
            p.className = "file-name";
            p.textContent = file.name;
            card.appendChild(p);

            const removeBtn = document.createElement("button");
            removeBtn.type = "button";
            removeBtn.className = "remove-existing-file";
            removeBtn.innerHTML = '<i class="fas fa-trash"></i>';
            removeBtn.addEventListener("click", () => {
                selectedFiles = selectedFiles.filter(f => f !== file);
                card.remove();
                updateFileInput();
            });
            card.appendChild(removeBtn);

            previewContainer.appendChild(card);
        });

        updateFileInput();
        fileInput.value = "";
    });

    // -------------------------------
    // SYNC FILE INPUT
    // -------------------------------
    function updateFileInput() {
        const dataTransfer = new DataTransfer();
        selectedFiles.forEach(file => dataTransfer.items.add(file));
        fileInput.files = dataTransfer.files;
    }

    // -------------------------------
    // FORM SUBMIT WITH AJAX + VALIDATION
    // -------------------------------
    form.addEventListener("submit", e => {
        e.preventDefault();


        updateBtn.style.display = "none";
        btnLoader.style.display = "inline-block";
        progressContainer.style.display = "block";
        progressBar.style.width = "0%";

        const formData = new FormData(form);
        selectedFiles.forEach(file => formData.append("files", file));

        const xhr = new XMLHttpRequest();
        xhr.open("POST", form.action || "", true);
        xhr.setRequestHeader("X-CSRFToken", document.querySelector('[name=csrfmiddlewaretoken]').value);

        xhr.upload.addEventListener("progress", e => {
            if (e.lengthComputable) {
                const percent = (e.loaded / e.total) * 100;
                progressBar.style.width = percent + "%";
            }
        });

        xhr.onload = () => {
            progressContainer.style.display = "none";
            let data;
            try { data = JSON.parse(xhr.responseText); }
            catch { data = { success: false, message: "Invalid server response" }; }

            showMessage(
                data.message || (data.success ? "Service updated successfully" : "Failed to update service"),
                data.success ? data.next_url : null
            );

            if (!data.success) {
                updateBtn.style.display = "inline-block";
                btnLoader.style.display = "none";
            }
        };

        xhr.onerror = () => {
            progressContainer.style.display = "none";
            showMessage("Failed to update activity. Try again.");
            updateBtn.style.display = "inline-block";
            btnLoader.style.display = "none";
        };

        xhr.send(formData);
    });

});

// -------------------------------
// PAGE LOADER
// -------------------------------
window.addEventListener("load", function () {
    const loader = document.getElementById("page-loader");
    if (loader) {
        loader.style.transition = "opacity 0.5s ease";
        loader.style.opacity = "0";
        setTimeout(() => loader.style.display = "none", 500);
    }
});

