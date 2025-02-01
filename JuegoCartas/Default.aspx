<%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="Memoria.Default" %>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Juego de Memoria</title>
    
    <!-- Librería SweetAlert2 para mostrar mensajes emergentes -->
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

    <!-- Enlace a la hoja de estilos personalizada -->
    <link rel="stylesheet" href="Content/styles.css">

    <!-- Enlace a Bootstrap para diseño responsivo -->
    <link rel="stylesheet" href="Content/bootstrap.min.css">
</head>
<body>
    <form id="form1" runat="server">
        <div class="container mt-4">
            
            <!-- Fila del Título -->
            <div class="row text-center">
                <div class="col-12">
                    <h1 class="text-black">Juego de Memoria</h1>
                </div>
            </div>

            <!-- Fila de Vidas -->
            <div class="row text-center">
                <div class="col-12">
                    <div class="vidas">
                        <asp:Literal ID="contadorVidas" runat="server"></asp:Literal>
                    </div>
                </div>
            </div>

            <!-- Fila principal con 3 columnas -->
            <div class="row justify-content-center mt-3">
                <!-- Primera columna (Botones de dificultad) -->
                <div class="col-lg-4 text-center">
                    <div class="dificultad p-3">
                        <h2 class="text-center">DIFICULTAD</h2>
                        <!-- Botones para seleccionar la dificultad -->
                        <button type="button" class="btn btn-success btn-lg mb-2" onclick="cambiarDificultad(2)">2x2 Fácil</button>
                        <br />
                        <button type="button" class="btn btn-danger btn-lg" onclick="cambiarDificultad(4)">4x4 Difícil</button>
                    </div>
                </div>

                <!-- Segunda columna (Tablero de Juego) -->
                <div class="col-lg-4 text-center">
                    <asp:Panel ID="tablero" runat="server" CssClass="tablero"></asp:Panel>

                    <!-- Botón de Reinicio -->
                    <div class="mt-3">
                        <asp:Button ID="btnReiniciar" runat="server" Text="REINICIAR" OnClick="ReiniciarJuego_Click" CssClass="btn btn-primary btn-lg" />
                    </div>
                </div>

                <!-- Tercera columna (Indicaciones) -->
                <div class="col-lg-4">
                    <div class="indicaciones p-3">
                        <h2 class="text-center">INDICACIONES</h2>
                        <p>Encuentra todas las parejas de cartas antes de quedarte sin vidas.</p>
                        <p>Cada vez que falles, perderás una vida. Al perder todas, el juego reiniciará.</p>
                        <p>¡Buena suerte!</p>
                        <!-- Imagen interactiva que cambia al hacer clic -->
                        <img id="imagenIndicaciones" src="Images/rostronormal.png" alt="Indicaciones" onclick="cambiarImagen()" class="img-fluid">
                    </div>
                </div>
            </div>
        </div>
    </form>

    <script>
        let primeraCarta = null;
        let segundaCarta = null;
        let bloqueo = false;
        let vidas = 5;
              
         /* Voltea una carta seleccionada y gestiona la lógica de aciertos o fallos.*/
        function voltearCarta(elemento, indice) {
            if (bloqueo) return;
            if (elemento.classList.contains("descubierta")) return;

            let numeroCarta = elemento.getAttribute("data-numero");
            elemento.classList.add("descubierta");
            elemento.innerText = numeroCarta;

            if (!primeraCarta) {
                primeraCarta = { elemento, indice };
            } else {
                segundaCarta = { elemento, indice };
                bloqueo = true;

                setTimeout(() => {
                    if (primeraCarta.elemento.innerText === segundaCarta.elemento.innerText) {
                        primeraCarta = null;
                        segundaCarta = null;
                        verificarVictoria(); // Verifica si todas las cartas han sido descubiertas
                    } else {
                        primeraCarta.elemento.classList.remove("descubierta");
                        segundaCarta.elemento.classList.remove("descubierta");
                        primeraCarta.elemento.innerText = "";
                        segundaCarta.elemento.innerText = "";
                        reducirVidas();
                    }
                    bloqueo = false;
                    primeraCarta = null;
                    segundaCarta = null;
                }, 1000);
            }
        }

        /* Verifica si todas las cartas han sido descubiertas y muestra un mensaje de victoria.*/
        function verificarVictoria() {
            let cartas = document.querySelectorAll(".carta");
            let todasDescubiertas = true;

            cartas.forEach(carta => {
                if (!carta.classList.contains("descubierta")) {
                    todasDescubiertas = false;
                }
            });

            if (todasDescubiertas) {
                Swal.fire({
                    title: "¡Felicidades!",
                    text: "Has ganado el juego 🎉",
                    imageUrl: "Images/ganaste.png",
                    imageWidth: 300,
                    imageHeight: 200,
                    confirmButtonText: "Aceptar"
                });
            }
        }

        /* Reduce la cantidad de vidas cuando el jugador comete un error.*/
        function reducirVidas() {
            vidas--;

            let corazones = "";
            for (let i = 0; i < 5; i++) {
                if (i < vidas) {
                    corazones += "❤️ ";
                } else {
                    corazones += "<span class='corazon' style='color: red;'>❌</span> ";
                }
            }
            document.querySelector(".vidas").innerHTML = corazones;

            if (vidas === 0) {
                Swal.fire({
                    title: "¡Perdiste!",
                    text: "Se acabaron tus vidas, volverás a empezar.",
                    icon: "error",
                    confirmButtonText: "Aceptar"
                }).then((result) => {
                    if (result.isConfirmed) {
                        document.getElementById("btnReiniciar").click();
                    }
                });
            }
        }

        /* Cambia la imagen de indicaciones entre dos estados al hacer clic en ella.*/
        function cambiarImagen() {
            let imagen = document.getElementById("imagenIndicaciones");
            if (imagen.src.includes("Images/rostroalegre.png")) {
                imagen.src = "Images/rostronormal.png";
            } else {
                imagen.src = "Images/rostroalegre.png";
            }
        }

        /* Cambia la dificultad del juego y recarga la página con el nuevo tamaño de tablero.*/
        function cambiarDificultad(nivel) {
            window.location.href = `Default.aspx?dificultad=${nivel}`;
        }
    </script>

</body>
</html>
