document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("loginBtn").addEventListener("click", function () {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        fetch("http://127.0.0.1:5000/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username: username, password: password }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                localStorage.setItem("token", data.access_token);
                window.location.href = "dashboard.html"; // Redirect to dashboard
            } else {
                alert("Login failed!");
            }
        });
    });
});
