// Connexion WebSocket avec le serveur Flask
const socket = io("http://localhost:8000");

socket.on("returnToMenuButton", () => {
    console.log("Serveur demande de revenir au menu");

    // Cacher toutes les options de jeu
    document.querySelectorAll(".playOptions").forEach(btn => {
        btn.style.display = "none";
    });
    document.querySelectorAll(".gameOptions").forEach(btn => {
        btn.style.display = "none";
    });    
    
    document.querySelectorAll(".returnButton").forEach(btn => {
        btn.style.display = "none";
    });

    // Réafficher les boutons du menu
    document.querySelectorAll(".menuOptions").forEach(btn => {
        btn.style.display = "inline-block";
    });
});

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

    document.querySelectorAll(".returnButton").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".gameOptions").forEach(b => b.style.display = "none");
            document.querySelectorAll(".playOptions").forEach(b => b.style.display = "none");
            document.querySelectorAll(".menuOptions").forEach(b => b.style.display = "inline-block");
            socket.emit("returnToMenu");
        });
    });

    document.getElementById("pauseButton").addEventListener("click", () => { 
        socket.emit("pauseGame");
    });

    document.getElementById("reprendreButton").addEventListener("click", () => { 
        socket.emit("reprendreGame");
    });
    
    document.getElementById("leaderboardButton").addEventListener("click", () => { 
        console.log("classement");
        socket.emit("getleaderboard");
        document.querySelectorAll(".menuOptions").forEach(btn => {
            btn.style.display = "none";
        });
        //document.getElementById("returnClassement").style.display = "inline-block";

    });

    // document.getElementById("returnClassement").addEventListener("click", () => { 
    //     socket.emit("returnFromClassement");
    //     document.querySelectorAll(".Classement").forEach(btn => {
    //         btn.style.display = "none";
    //     });
    //     document.querySelectorAll(".menuOptions").forEach(btn => {
    //         btn.style.display = "inline-block";
    //     });
    // });
    
    document.getElementById("quitButton").addEventListener("click", () => {
        socket.emit("quitGame");
        console.log("Fermeture du jeu");
        window.close();
    });

    document.getElementById("logout").addEventListener("click", () => {
        window.location.href = "/logout";
    });

    
    document.getElementById("settingsButton").addEventListener("click", () => console.log("parametres"));

    // Gestion de la connexion WebSocket
    socket.on("connect", () => console.log("Connecté au serveur Flask WebSocket !"));
    socket.on("disconnect", () => console.log("Déconnecté du serveur."));
});