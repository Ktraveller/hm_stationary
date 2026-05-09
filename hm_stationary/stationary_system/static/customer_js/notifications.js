document.addEventListener("DOMContentLoaded", function () {

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

    const change_password_url = CHANGE_PASSWORD;

    const notifSound = new Audio("/static/sounds/notify.mp3");

    // =============================
    // DROPDOWNS
    // =============================
    if (notifBtn && userBtn && notifMenu && userMenu) {

        notifBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            notifMenu.style.display =
                notifMenu.style.display === "block" ? "none" : "block";
            userMenu.style.display = "none";
        });

        userBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            userMenu.style.display =
                userMenu.style.display === "block" ? "none" : "block";
            notifMenu.style.display = "none";
        });

        document.addEventListener("click", function () {
            notifMenu.style.display = "none";
            userMenu.style.display = "none";
        });
    }

    // =============================
    // CSRF
    // =============================
    function getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : "";
    }

    // =============================
    // LOAD NOTIFICATIONS (FROM DATABASE)
    // =============================
    function loadNotifications() {
        fetch(NOTIF_URL)
            .then(res => res.json())
            .then(data => {
                renderNotifications(data.notifications);
                if (notifCount) notifCount.innerText = data.unread_count;
            })
            .catch(err => console.log("❌ Load error:", err));
    }

    loadNotifications();

    // =============================
    // RENDER LIST
    // =============================
    function renderNotifications(notifs) {

        if (!notifList) return;

        if (!notifs || notifs.length === 0) {
            notifList.innerHTML = `<div class="notif-empty">No notifications</div>`;
            return;
        }

        notifList.innerHTML = "";

        notifs.forEach(n => createNotifElement(n, false));
    }

    // =============================
    // CREATE NOTIFICATION ITEM
    // =============================
    function createNotifElement(n, prepend = true) {

        const div = document.createElement("div");
        div.className = "notif-item " + (!n.is_read ? "notif-unread" : "");

        div.innerHTML = `
            <div class="notif-content">
                <div class="notif-text">${n.message}</div>
                <div class="notif-actions">
                    <small class="notif-view">Click to view</small>
                    <button class="notif-delete" data-id="${n.id}">×</button>
                </div>
            </div>
        `;

        // VIEW + MARK READ
        div.querySelector(".notif-view").addEventListener("click", function (e) {
            e.stopPropagation();

            fetch(MARK_READ_URL, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `id=${n.id}`
            });

            div.classList.remove("notif-unread");

            if (user_type === "customer") {
                window.location.href =
                    `/stationary/customer/preview-activity/${n.activity_id}/`;
            } else if (user_type === "stationary") {
                window.location.href =
                    `/stationary/stationary/preview_activity/${n.activity_id}/`;
            }
        });

        if (prepend) {
            notifList.prepend(div);
        } else {
            notifList.appendChild(div);
        }
    }

    // =============================
    // DELETE NOTIFICATION
    // =============================
    document.addEventListener("click", function (e) {

        if (e.target.classList.contains("notif-delete")) {

            e.stopPropagation();

            const notifId = e.target.getAttribute("data-id");
            const notifItem = e.target.closest(".notif-item");

            fetch(DELETE_URL, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `id=${notifId}`
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        notifItem.remove();

                        notifCount.innerText =
                            Math.max(0, parseInt(notifCount.innerText || 0) - 1);
                    }
                });
        }
    });



    // changes user password
    document.querySelector('.change-password-20 form')
        .addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(this);

            fetch(change_password_url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
                .then(res => res.json())
                .then(data => {
                    alert(data.message);

                    if (data.status === 'success') {
                        userMenu.style.display = "none";
                    }
                });
        });

});