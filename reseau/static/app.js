// Connexion WebSocket avec le serveur Flask
const socket = io("http://localhost:8000");

document.addEventListener("DOMContentLoaded", function () {
    console.log("Script chargé !");

    // Récupérer les boutons existants
    document.getElementById("playButton").addEventListener("click", () => socket.emit("startGame"));
    document.getElementById("settingsButton").addEventListener("click", () => console.log("parametres"));
    document.getElementById("leaderboardButton").addEventListener("click", () => console.log("classement"));
    document.getElementById("quitButton").addEventListener("click", () => {
        console.log("Fermeture du jeu");
        window.close();
    });

    // Gestion de la connexion WebSocket
    socket.on("connect", () => console.log("Connecté au serveur Flask WebSocket !"));
    socket.on("disconnect", () => console.log("Déconnecté du serveur."));
});