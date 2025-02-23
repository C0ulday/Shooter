// Connexion WebSocket avec le serveur Flask
const socket = io("http://0.0.0.0:5000"); // Change avec la vraie adresse IP

// Création dynamique du menu avec JavaScript
document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    // Titre
    const title = document.createElement("h1");
    title.innerText = "Bienvenue sur Esi-Shoot";
    title.style.color = "#333";
    body.appendChild(title);

    // Conteneur des boutons
    const buttonContainer = document.createElement("div");
    body.appendChild(buttonContainer);

    // Fonction pour créer un bouton
    function createButton(text, color, callback) {
        const button = document.createElement("button");
        button.innerText = text;
        // Action du bouton
        button.addEventListener("click", callback);
        buttonContainer.appendChild(button);
    }

    // Ajout des boutons
    createButton("Jouer", "#28a745", () => socket.emit("startGame"));
    createButton("Paramètres", "#007bff", () => console.log("paramètres"));
    createButton("Classement", "#ffc107", () => console.log("classement"));
    createButton("Quitter", "#dc3545", () => {
        console.log("Fermeture du jeu");
        window.close(); 
    });

    // Gestion de la connexion WebSocket
    socket.on("connect", () => console.log("Connecté au serveur Flask WebSocket !"));
    socket.on("disconnect", () => console.log("Déconnecté du serveur."));
});
