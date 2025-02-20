// Connexion WebSocket avec le serveur Flask
const socket = io("http://0.0.0.0:5000"); // iL faut le changer avec la vrai adresse ip

// Création dynamique du menu avec JavaScript
document.addEventListener("DOMContentLoaded", function () {
    const body = document.body;
    body.style.fontFamily = "Arial, sans-serif";
    body.style.textAlign = "center";
    body.style.marginTop = "100px";

    // Titre
    const title = document.createElement("h1");
    title.innerText = "Bienvenue sur le Jeu";
    body.appendChild(title);

    // Bouton "Jouer"
    const playButton = document.createElement("button");
    playButton.innerText = "Jouer";
    playButton.style.padding = "10px 20px";
    playButton.style.fontSize = "20px";
    playButton.style.cursor = "pointer";
    playButton.style.border = "none";
    playButton.style.backgroundColor = "#28a745";
    playButton.style.color = "white";
    playButton.style.borderRadius = "5px";

    body.appendChild(playButton);

    // Action du bouton "Jouer"
    playButton.addEventListener("click", function () {
        console.log("Bouton cliqué, envoi de la commande au serveur...");
        socket.emit("start_game");  // Envoie la commande au serveur Python
    });

    // Gestion de la connexion WebSocket
    socket.on("connect", function () {
        console.log("Connecté au serveur Flask WebSocket !");
    });

    socket.on("disconnect", function () {
        console.log("Déconnecté du serveur.");
    });
});
