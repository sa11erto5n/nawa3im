document.addEventListener("DOMContentLoaded", function () {
    // Get the current URL path
    const currentPath = window.location.pathname;

    // Select all nav-items
    const navItems = document.querySelectorAll("#menu .nav-item");
    
    // Loop through nav-items to find a match
    navItems.forEach(item => {
        const itemUrl = item.getAttribute("data-url");

        if (currentPath.startsWith(itemUrl)) {
            // Add the active class
            item.classList.add("active");
        }
    });
});
// JavaScript to add any interactivity if needed
document.querySelectorAll('.dropdown-menu').forEach(menu => {
    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (!menu.parentElement.contains(e.target)) {
            menu.style.display = 'none';
        }
    });

    // Open dropdown on button click
    menu.parentElement.addEventListener('click', () => {
        const isVisible = menu.style.display === 'flex';
        menu.style.display = isVisible ? 'none' : 'flex';
    });
});
// Rest Notifications Count
document.addEventListener('DOMContentLoaded', function () {
    const notificationButton = document.querySelector('.mark-as-read');

    if (notificationButton) {
        notificationButton.addEventListener('click', function () {
            // SweetAlert Confirmation
            Swal.fire({
                title: 'Mark all as read?',
                text: "This will mark all your notifications as read.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Yes, reset!',
                cancelButtonText: 'Cancel'
            }).then((result) => {
                if (result.isConfirmed) {
                    // If user confirms, make the POST request
                    fetch("/dashboard/reset-notifications/", {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": "{{ csrf_token }}", // Replace with CSRF token
                            "Content-Type": "application/json"
                        }
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                Swal.fire(
                                    'Reset!',
                                    'Done.',
                                    'success'
                                );

                                // Update the notifications count
                                const notificationCount = document.querySelector('.notification-btn .bg-warning');
                                if (notificationCount) {
                                    notificationCount.textContent = "0";
                                }
                            } else {
                                Swal.fire(
                                    'Error!',
                                    data.message || 'Failed to reset notifications.',
                                    'error'
                                );
                            }
                        })
                        .catch(error => {
                            console.error('Request failed:', error);
                            Swal.fire(
                                'Error!',
                                'An unexpected error occurred.',
                                'error'
                            );
                        });
                }
            });
        });
    }
});

// Controlling the sidebar visibility
let MenuBtn = document.getElementById('menu-btn')
let SideBar = document.getElementById('sidebar')
MenuBtn.addEventListener('click', () => {
    if (SideBar.classList.contains('show-sidebar')) {
        SideBar.classList.replace('show-sidebar', 'hide-sidebar')
    }
    else {
        SideBar.classList.replace('hide-sidebar', 'show-sidebar')
    }

})
