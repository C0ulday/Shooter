document.addEventListener("DOMContentLoaded", fetchProfile);

function fetchProfile() {
    fetch("/api/profile")
        .then(response => response.json())
        .then(data => {
            const profileInfo = document.getElementById("profile-info");
            if (data.error || data.message) {
                profileInfo.textContent = "Aucun profil trouvé.";
            } else {
                profileInfo.innerHTML = `
                    <p><strong>Bio :</strong> ${data.bio}</p>
                    <p><strong>Avatar :</strong> <img src="${data.avatar_url}" width="100"></p>
                `;
            }
        })
        .catch(error => console.error("Erreur :", error));
}

document.getElementById("profile-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const bio = document.getElementById("bio").value;
    const avatar_url = document.getElementById("avatar_url").value;

    fetch("/api/profile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bio, avatar_url })
    })
    .then(response => response.json())
    .then(() => {
        alert("Profil créé avec succès !");
        fetchProfile();
    })
    .catch(error => console.error("Erreur :", error));
});
