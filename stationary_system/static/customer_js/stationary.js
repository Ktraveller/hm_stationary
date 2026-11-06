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

        noResultMsg.style.display = (visibleCount === 0) ? "block" : "none";
    });
}

// Highlight accessory card on button click
document.addEventListener("DOMContentLoaded", () => {
    const accessoryButtons = document.querySelectorAll(".option-25-1 button");
    const cards = document.querySelectorAll(".accessory-card-6");

    accessoryButtons.forEach(button => {
        button.addEventListener("click", () => {
            const name = button.textContent.trim().toLowerCase().replace(/\s+/g, '-');

            cards.forEach(c => c.classList.remove("highlight-card"));
            const targetCard = document.querySelector(`.accessory-card-6[data-accessory-name="${name}"]`);
            if (targetCard) {
                targetCard.classList.add("highlight-card");
                targetCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }

            accessoryButtons.forEach(b => b.classList.remove("active"));
            button.classList.add("active");
        });
    });
});



// for add to cart
document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll(".add-to-cart-form");

    const modal = document.getElementById("cartMessageModal");
    const messageText = document.getElementById("cartMessageText");
    const closeBtn = document.getElementById("closeCartMessageBtn");

    // Show modal safely
    function showModal(message) {
        if (modal && messageText) {
            messageText.textContent = message;
            modal.style.display = "flex";
        } else {
            alert(message);
        }
    }

    // Close modal manually
    if (closeBtn) closeBtn.onclick = () => modal.style.display = "none";

    // Close modal if click outside content
    if (modal) modal.addEventListener("click", e => {
        if (e.target === modal) modal.style.display = "none";
    });

    forms.forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const submitBtn = this.querySelector("button[type='submit']");
            if (submitBtn) submitBtn.disabled = true;

            fetch(this.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showModal(data.message || "Added to cart successfully");

                        // Keep modal visible for 2 seconds, then reload
                        setTimeout(() => {
                            location.reload();
                        }, 2000); // 2 seconds
                    } else {
                        showModal(data.error || "Failed to add to cart");
                    }
                })
                .catch(err => showModal(err.message || "Something went wrong"))
                .finally(() => { if (submitBtn) submitBtn.disabled = false; });
        });
    });
});


// confirm order
document.addEventListener("DOMContentLoaded", () => {
    const confirmForm = document.getElementById("confirmOrdersForm");
    const modal = document.getElementById("cartMessageModal");
    const messageText = document.getElementById("cartMessageText");
    const closeBtn = document.getElementById("closeCartMessageBtn");

    function showModal(message) {
        if (modal && messageText) {
            messageText.textContent = message;
            modal.style.display = "flex";
        } else {
            alert(message); // fallback
        }
    }

    if (closeBtn) {
        closeBtn.onclick = () => modal.style.display = "none";
    }

    if (modal) {
        modal.addEventListener("click", e => {
            if (e.target === modal) modal.style.display = "none";
        });
    }

    if (confirmForm) {
        confirmForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const submitBtn = this.querySelector("button[type='submit']");
            if (submitBtn) submitBtn.disabled = true;

            fetch(this.action, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showModal("Orders confirmed successfully!");
                        // Optional: reload page or remove pending orders from UI
                        setTimeout(() => window.location.reload(), 1000);
                    } else {
                        showModal("Failed to confirm orders!");
                    }
                })
                .catch(err => {
                    showModal("Something went wrong!");
                })
                .finally(() => {
                    if (submitBtn) submitBtn.disabled = false;
                });
        });
    }
});


// remove item in cart
document.addEventListener("DOMContentLoaded", () => {
    const removeForms = document.querySelectorAll(".remove-order-form");

    const modal = document.getElementById("cartMessageModal");
    const messageText = document.getElementById("cartMessageText");
    const closeBtn = document.getElementById("closeCartMessageBtn");

    // ✅ Show modal
    function showModal(message) {
        if (modal && messageText) {
            messageText.textContent = message;
            modal.style.display = "flex";
        } else {
            alert(message); // fallback
        }
    }

    // ✅ Close modal
    if (closeBtn) closeBtn.onclick = () => modal.style.display = "none";
    if (modal) {
        modal.addEventListener("click", e => {
            if (e.target === modal) modal.style.display = "none";
        });
    }

    removeForms.forEach(form => {
        form.addEventListener("submit", (e) => {
            e.preventDefault();

            const submitBtn = form.querySelector("button[type='submit']");
            const formData = new FormData(form);

            if (submitBtn) submitBtn.disabled = true;

            fetch(form.action, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" },
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        // Remove the card
                        const card = form.closest(".activity-card-12");
                        if (card) card.remove();
                        showModal(data.message || "Order removed successfully");
                    } else {
                        showModal(data.message || "Failed to remove order");
                    }
                })
                .catch(err => {
                    console.error(err);
                    showModal("Failed to remove order. Try again.");
                })
                .finally(() => {
                    if (submitBtn) submitBtn.disabled = false;
                });
        });
    });
});


// for order progress
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".progress-bar").forEach(circle => {
        const progress = parseInt(circle.dataset.progress || 0, 10);
        const dashOffset = 126 - (126 * progress / 100);
        setTimeout(() => {
            circle.style.strokeDashoffset = dashOffset;
        }, 100); // slight delay to trigger CSS transition
    });
});






// Delete delivered orders
// Get modal elements
const cartModal = document.getElementById("cartMessageModal");
const cartMessageText = document.getElementById("cartMessageText");
const closeCartMessageBtn = document.getElementById("closeCartMessageBtn");

// Function to show modal with message
function showCartModal(message) {
    cartMessageText.textContent = message;
    cartModal.style.display = "block";
}

// Close modal on button click
closeCartMessageBtn.addEventListener("click", () => {
    cartModal.style.display = "none";
});

// Delete delivered/submitted orders
const deleteForms = document.querySelectorAll(".delete-order-form");

deleteForms.forEach(form => {
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const orderId = this.querySelector("input[name='order_id']").value;
        const card = this.closest(".activity-card-12");
        const url = this.dataset.url;  // Get URL from data-url
        const csrfToken = this.querySelector('[name=csrfmiddlewaretoken]').value;

        // Debug: check order id
        console.log("Deleting order_id:", orderId);

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ order_id: orderId })
        })
            .then(res => {
                if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
                return res.json();
            })
            .then(data => {
                if (data.success) {
                    // Remove the card smoothly
                    card.style.transition = "opacity 0.4s";
                    card.style.opacity = 0;
                    setTimeout(() => card.remove(), 400);

                    showCartModal(data.message || "Order deleted successfully");
                } else {
                    showCartModal(data.message || "Failed to delete order");
                }
            })
            .catch(err => {
                console.error("Delete order error:", err);
                showCartModal("Error deleting order. Try again.");
            });
    });
});


// show or hide order icon
const btn = document.getElementById("toggleOrdersBtn");
const box = document.getElementById("ordersBox");
const icon = document.getElementById("toggleIcon");

btn.addEventListener("click", function () {
    if (box.style.display === "none" || box.style.display === "") {
        box.style.display = "block";
        icon.classList.remove("fa-shopping-cart");
        icon.classList.add("fa-times"); // close icon
    } else {
        box.style.display = "none";
        icon.classList.remove("fa-times");
        icon.classList.add("fa-shopping-cart");
    }
});

