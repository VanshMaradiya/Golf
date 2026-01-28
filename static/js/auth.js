function login() {

    fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    })
    .then(r => r.json())
    .then(d => {

        if (d.user_id) {
            localStorage.setItem("user_id", d.user_id);
            localStorage.setItem("role", d.role);
            window.location.href = "/dashboard";
        } else {
            document.getElementById("msg").innerText = d.error || "Login failed";
        }
    });
}


function register() {

    console.log("REGISTER FUNCTION");

    fetch("/api/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value,
            role: document.getElementById("role").value
        })
    })
    .then(r => r.json())
    .then(d => {

        console.log(d);

        if (d.user_id) {
            alert("Registered!");
            window.location.href = "/";
        } else {
            document.getElementById("msg").innerText = d.error || "Failed";
        }
    });
}
