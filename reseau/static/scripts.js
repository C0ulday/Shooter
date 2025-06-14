document.addEventListener("DOMContentLoaded", fetchUsers);

function fetchUsers() {
    fetch("/api/users")
        .then(response => response.json())
        .then(data => {
            const userList = document.getElementById("user-list");
            userList.innerHTML = "";

            data.forEach(user => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${user.id}</td>
                    <td>${user.name}</td>
                    <td>${user.email}</td>
                    <td>
                        <button onclick="editUser(${user.id}, '${user.name}', '${user.email}')"> Modifier</button>
                        <button onclick="deleteUser(${user.id})"> Supprimer</button>
                    </td>
                `;
                userList.appendChild(row);
            });
        })
        .catch(error => console.error("Erreur:", error));
}

function addUser() {
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    fetch("/api/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email })
    })
    .then(() => fetchUsers())
    .catch(error => console.error("Erreur:", error));
}

function deleteUser(userId) {
    fetch(`/api/users/${userId}`, { method: "DELETE" })
    .then(() => fetchUsers())
    .catch(error => console.error("Erreur:", error));
}

function editUser(userId, userName, userEmail) {
    document.getElementById("edit-id").value = userId;
    document.getElementById("edit-name").value = userName;
    document.getElementById("edit-email").value = userEmail;
    document.getElementById("edit-form").style.display = "block";
}

function updateUser() {
    const userId = document.getElementById("edit-id").value;
    const name = document.getElementById("edit-name").value;
    const email = document.getElementById("edit-email").value;

    fetch(`/api/users/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email })
    })
    .then(() => {
        document.getElementById("edit-form").style.display = "none";
        fetchUsers();
    })
    .catch(error => console.error("Erreur:", error));
}
