document.addEventListener("DOMContentLoaded", function () {

    // ---------------------------
    // CSRF helper
    // ---------------------------
    function getCSRFToken() {
        const tokenElem = document.querySelector('#activityActionForm [name=csrfmiddlewaretoken]');
        return tokenElem ? tokenElem.value : '';
    }

    // ---------------------------
    // Message modal
    // ---------------------------
    const messageModal = document.getElementById('messageModal');
    const messageBody = document.getElementById('messageBody');

    window.openMessageModal = function (type, message, autoClose = true, duration = 2000) {
        messageBody.className = '';
        if (type === 'success') messageBody.classList.add('message-success');
        else if (type === 'error') messageBody.classList.add('message-error');
        else messageBody.classList.add('message-info');

        messageBody.innerHTML = message;
        messageModal.style.display = 'flex';

        if (autoClose) setTimeout(() => closeMessageModal(), duration);
    };

    window.closeMessageModal = function () { messageModal.style.display = 'none'; };
    window.addEventListener('click', function (event) {
        if (event.target === messageModal) closeMessageModal();
    });

    // ---------------------------
    // File preview modal
    // ---------------------------
    const fileModal = document.getElementById('fileModal');
    const modalBody = document.getElementById('modalBody');
    const modalTitle = document.getElementById('modalTitle');

    window.openModal = function (type, fileUrl, fileName) {
        modalTitle.textContent = fileName || '';
        if (type === 'image') modalBody.innerHTML = `<img src="${fileUrl}" style="max-width:100%;">`;
        else if (type === 'pdf') modalBody.innerHTML = `<embed src="${fileUrl}" width="100%" height="500">`;
        else modalBody.innerHTML = `<p>Download or view this file:</p>
                                    <a href="${fileUrl}" target="_blank" download>Download ${fileName}</a>`;
        fileModal.style.display = 'block';
    };
    window.closeModal = function () { fileModal.style.display = 'none'; };
    window.addEventListener('click', function (event) { if (event.target === fileModal) closeModal(); });

    // ---------------------------
    // Accept / Decline activity
    // ---------------------------
    window.activateProcessing = function (btn, url) {
        if (!btn || !url) return;
        btn.disabled = true;
        btn.innerHTML = 'Processing...';
        openMessageModal('info', 'Processing activity...');
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    openMessageModal('success', data.message || 'Activity accepted.');
                    setTimeout(() => location.reload(), 1200);
                } else {
                    openMessageModal('error', data.message || 'Failed to accept.');
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-circle-check"></i> Accept';
                }
            })
            .catch(() => {
                openMessageModal('error', 'Server error while accepting.');
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-circle-check"></i> Accept';
            });
    };

    window.declineActivity = function (btn, url) {
        if (!btn || !url) return;
        btn.disabled = true;
        btn.innerHTML = 'Declining...';
        openMessageModal('info', 'Declining activity...');
        fetch(url, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json' }
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    openMessageModal('success', data.message || 'Activity declined.');
                    setTimeout(() => location.reload(), 1200);
                } else {
                    openMessageModal('error', data.message || 'Failed to decline.');
                    btn.disabled = false;
                    btn.innerHTML = '<i class="fas fa-ban"></i> Decline';
                }
            })
            .catch(() => {
                openMessageModal('error', 'Server error while declining.');
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-ban"></i> Decline';
            });
    };

    // ---------------------------
    // File upload preview + confirm + client-side validation
    // ---------------------------
    const fileInput = document.getElementById("processedFileInput");
    const previewContainer = document.getElementById("processedPreviewContainer");
    const uploadForm = document.getElementById("processedUploadForm");

    let selectedFiles = [];
    const allowedTypes = ['image/png', 'image/jpeg', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const maxFileSize = 5 * 1024 * 1024; // 5MB
    const maxFiles = 5;

    if (fileInput && previewContainer && uploadForm) {

        // File select
        fileInput.addEventListener("change", function (e) {
            const files = Array.from(e.target.files);

            files.forEach(file => {
                // Check duplicates
                if (!selectedFiles.some(f => f.name === file.name && f.size === file.size && f.lastModified === file.lastModified)) {

                    // Validate type
                    if (!allowedTypes.includes(file.type)) {
                        openMessageModal('error', `File "${file.name}" is not allowed. Allowed types: PNG, JPG, PDF, DOC, DOCX.`);
                        return;
                    }

                    // Validate size
                    if (file.size > maxFileSize) {
                        openMessageModal('error', `File "${file.name}" exceeds 5MB limit.`);
                        return;
                    }

                    // Validate max files
                    if (selectedFiles.length >= maxFiles) {
                        openMessageModal('error', `You can upload a maximum of ${maxFiles} files.`);
                        return;
                    }

                    selectedFiles.push(file);
                }
            });

            renderPreview();
            fileInput.value = "";
        });

        // Render file preview
        function renderPreview() {
            previewContainer.innerHTML = "";
            selectedFiles.forEach((file, index) => {
                const div = document.createElement("div");
                div.className = "file-box";

                // Remove button
                const removeBtn = document.createElement("span");
                removeBtn.className = "delete-icon";
                removeBtn.innerHTML = "&times;";
                removeBtn.onclick = () => { removeFile(index); };
                div.appendChild(removeBtn);

                // File display
                if (file.type.startsWith("image/")) {
                    const img = document.createElement("img");
                    img.src = URL.createObjectURL(file);
                    img.style.maxWidth = "150px";
                    img.style.maxHeight = "120px";
                    img.style.cursor = "pointer";
                    img.onclick = () => openModal("image", URL.createObjectURL(file), file.name);
                    div.appendChild(img);
                } else if (file.type === "application/pdf") {
                    const embed = document.createElement("embed");
                    embed.src = URL.createObjectURL(file);
                    embed.type = "application/pdf";
                    embed.width = "100%";
                    embed.height = "120";
                    embed.style.cursor = "pointer";
                    embed.onclick = () => openModal("pdf", URL.createObjectURL(file), file.name);
                    div.appendChild(embed);
                } else {
                    const p = document.createElement("p");
                    p.innerText = file.name;
                    div.appendChild(p);
                }

                // File name
                const name = document.createElement("small");
                name.innerText = file.name;
                div.appendChild(name);

                previewContainer.appendChild(div);
            });
        }

        function removeFile(index) {
            selectedFiles.splice(index, 1);
            renderPreview();
        }

        // Submit form with confirm modal
        uploadForm.addEventListener("submit", function (e) {
            e.preventDefault();
            if (selectedFiles.length === 0) { openMessageModal('error', 'Please select at least one file.'); return; }

            const confirmModal = document.getElementById("userConfirmModal");
            const yesBtn = document.getElementById("userConfirmYes");
            const noBtn = document.getElementById("userConfirmNo");

            confirmModal.style.display = "block";

            yesBtn.onclick = () => {
                confirmModal.style.display = "none";

                const formData = new FormData();
                formData.append("csrfmiddlewaretoken", getCSRFToken());
                selectedFiles.forEach(file => formData.append("processed_file", file));

                const submitBtn = uploadForm.querySelector('button[type="submit"]');
                if (submitBtn) submitBtn.disabled = true;

                openMessageModal('info', 'Uploading files...');

                fetch(uploadForm.action, { method: "POST", body: formData })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            openMessageModal('success', data.message || 'Upload successful!');
                            selectedFiles = [];
                            renderPreview();
                            uploadForm.reset();

                            const stationaryUrl = document.getElementById('activityActions')?.dataset.stationaryUrl;
                            if (stationaryUrl) {
                                setTimeout(() => {
                                    window.location.href = stationaryUrl;
                                }, 1200);
                            }

                        } else {
                            openMessageModal('error', data.message || 'Upload failed!');
                            if (submitBtn) submitBtn.disabled = false;
                        }
                    })
                    .catch(err => {
                        console.error(err);
                        openMessageModal('error', 'Upload failed: ' + err.message);
                        if (submitBtn) submitBtn.disabled = false;
                    });
            };

            noBtn.onclick = () => { confirmModal.style.display = "none"; };
        });

        // Close confirm modal on outside click
        window.addEventListener("click", function (event) {
            const confirmModal = document.getElementById("userConfirmModal");
            if (event.target === confirmModal) confirmModal.style.display = "none";
        });
    }


    // ---------------------------
    // ACTIVITY COST SUBMISSION
    // ---------------------------
    document.querySelectorAll(".activity-cost-form").forEach(form => {

        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const formData = new FormData(form);
            const submitBtn = form.querySelector("button[type='submit']");

            // ✅ Extract values
            let activityId = formData.get("activity_id");
            let cost = formData.get("costs");

            // ---------------------------
            // Validation
            // ---------------------------
            if (!cost || parseFloat(cost) <= 0) {
                openMessageModal("error", "Enter valid cost");
                return;
            }

            submitBtn.disabled = true;
            submitBtn.innerText = "Sending...";

            openMessageModal("info", "Saving cost...");

            // ---------------------------
            // AJAX Request
            // ---------------------------
            fetch(window.APP_CONFIG.sendCostUrl, {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": getCSRFToken()
                }
            })
                .then(res => res.json())
                .then(data => {

                    if (data.success) {

                        // ---------------------------
                        // WhatsApp Message
                        // ---------------------------
                        let message = `Hello, cost has been set.\nActivity ID: ${activityId}\nCost: TZS ${cost}`;

                        let encodedMessage = encodeURIComponent(message);

                        let whatsappURL = `https://wa.me/${window.APP_CONFIG.whatsappNumber}?text=${encodedMessage}`;

                        // ---------------------------
                        // Success modal
                        // ---------------------------
                        openMessageModal("success", data.message || "Saved successfully");

                        // ---------------------------
                        // WhatsApp + Reload
                        // ---------------------------
                        setTimeout(() => {
                            window.open(whatsappURL, "_blank");
                            location.reload();
                        }, 1200);

                    } else {
                        openMessageModal("error", data.message || "Failed to save");
                        submitBtn.disabled = false;
                        submitBtn.innerText = "Send";
                    }

                })
                .catch(() => {
                    openMessageModal("error", "Server error occurred");
                    submitBtn.disabled = false;
                    submitBtn.innerText = "Send";
                });

        });

    });

});