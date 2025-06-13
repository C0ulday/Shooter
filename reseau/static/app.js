// Connexion WebSocket avec le serveur Flask
const socket = io("http://localhost:8000");

document.addEventListener("DOMContentLoaded", function () {
    console.log("Script chargé !");

    document.getElementById("playButton").addEventListener("click", () => { 
        socket.emit("startGame");
        
        // on affiche les boutons du menu
        document.querySelectorAll(".gameOptions").forEach(btn => {
            btn.style.display = "inline-block";
        });

        // on cache les boutons du menu
        document.querySelectorAll(".menuOptions").forEach(btn => {
            btn.style.display = "none";
        });
    });

    document.getElementById("mode1Button").addEventListener("click", () => { 
        socket.emit("startMode1");
        // on cache les boutons du menu
        document.querySelectorAll(".gameOptions").forEach(btn => {
            btn.style.display = "none";
        });
        // on affiche les boutons de jeu
        document.querySelectorAll(".playOptions").forEach(btn => {
            btn.style.display = "inline-block";
        });
    });
    document.getElementById("mode2Button").addEventListener("click", () => { 
        socket.emit("startMode2");
    });

    document.getElementById("pauseButton").addEventListener("click", () => { 
        socket.emit("pauseGame");
    });

    document.getElementById("reprendreButton").addEventListener("click", () => { 
        socket.emit("reprendreGame");
    });

    document.getElementById("returnButton").addEventListener("click", () => { 

        socket.emit("returnToMenu");
        
        // on cache les options du jeu
        document.querySelectorAll(".gameOptions").forEach(btn => {
            btn.style.display = "none";
        });
        document.querySelectorAll(".playOptions").forEach(btn => {
            btn.style.display = "none";
        });

        // on affiche les boutons du menu
        document.querySelectorAll(".menuOptions").forEach(btn => {
                btn.style.display = "inline-block";
        });

    });

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