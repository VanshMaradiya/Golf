function requireLogin() {
    const userId = localStorage.getItem("user_id");
    const role = localStorage.getItem("role");

    if (!userId || !role) {
        window.location.href = "/";
    }
}

function logout() {
    console.log("Logout clicked");

    localStorage.removeItem("user_id");
    localStorage.removeItem("role");

    window.location.href = "/";
}
