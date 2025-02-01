using System;
using System.Collections.Generic;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace Memoria
{
    public partial class Default : Page
    {
        /// <summary>
        /// Método ejecutado al cargar la página.
        /// </summary>
        protected void Page_Load(object sender, EventArgs e)
        {
            if (!IsPostBack) // Se ejecuta solo en la primera carga de la página.
            {
                // Obtiene la dificultad desde la URL. Si no se especifica, usa 4 por defecto.
                int dificultad = Request.QueryString["dificultad"] != null ? int.Parse(Request.QueryString["dificultad"]) : 4;

                ViewState["Dificultad"] = dificultad;
                IniciarJuego(dificultad);
            }
        }

        /// <summary>
        /// Inicializa el juego generando las cartas, barajándolas y almacenándolas en el ViewState.
        /// </summary>
        /// <param name="dificultad">Tamaño del tablero (2x2 o 4x4).</param>
        private void IniciarJuego(int dificultad)
        {
            int totalCartas = dificultad * dificultad; // Calcula el número total de cartas según la dificultad.
            List<int> valoresCartas = new List<int>();

            // Se generan pares de cartas (cada número aparece dos veces).
            for (int i = 1; i <= totalCartas / 2; i++)
            {
                valoresCartas.Add(i);
                valoresCartas.Add(i);
            }

            // Baraja las cartas aleatoriamente usando GUID para mezclar.
            valoresCartas.Sort((a, b) => Guid.NewGuid().CompareTo(Guid.NewGuid()));

            // Almacena los datos en el ViewState para que se conserven entre recargas de página.
            ViewState["Cartas"] = valoresCartas;
            ViewState["Vidas"] = 5;
            ViewState["Aciertos"] = new List<int>();

            RenderizarTablero(dificultad);
            RenderizarVidas();
        }

        /// <summary>
        /// Renderiza el tablero de juego en función de la dificultad y las cartas almacenadas.
        /// </summary>
        /// <param name="dificultad">Tamaño del tablero (2x2 o 4x4).</param>
        private void RenderizarTablero(int dificultad)
        {
            List<int> cartas = (List<int>)ViewState["Cartas"];
            List<int> aciertos = (List<int>)ViewState["Aciertos"];
            tablero.Controls.Clear();

            // Define el estilo de CSS para establecer el tamaño de la cuadrícula del tablero.
            string gridTemplate = $"repeat({dificultad}, 100px)";
            tablero.Controls.Add(new Literal
            {
                Text = $"<style>.tablero {{ display: grid; grid-template-columns: {gridTemplate}; gap: 10px; justify-content: center; }}</style>"
            });

            // Genera las cartas dinámicamente en el tablero.
            for (int i = 0; i < cartas.Count; i++)
            {
                string claseCarta = aciertos.Contains(i) ? "descubierta" : "carta"; // Define si la carta ya fue acertada.
                string contenidoCarta = aciertos.Contains(i) ? cartas[i].ToString() : ""; // Solo muestra el número si ha sido descubierta.

                Literal carta = new Literal
                {
                    Text = $"<div class='{claseCarta}' onclick='voltearCarta(this, {i})' data-numero='{cartas[i]}'>{contenidoCarta}</div>"
                };
                tablero.Controls.Add(carta);
            }
        }

        /// <summary>
        /// Renderiza el contador de vidas en la interfaz gráfica.
        /// </summary>
        private void RenderizarVidas()
        {
            int vidas = (int)ViewState["Vidas"]; // Recupera la cantidad de vidas desde el ViewState.
            string corazones = "";

            // Genera los corazones en función del número de vidas restantes.
            for (int i = 0; i < 5; i++)
            {
                corazones += (i < vidas) ? "❤️ " : "<span class='corazon' style='color: red;'>❌</span> ";
            }

            // Actualiza el contador de vidas en la interfaz.
            contadorVidas.Text = corazones;
        }

        /// <summary>
        /// Reinicia el juego manteniendo la dificultad seleccionada.
        /// </summary>
        protected void ReiniciarJuego_Click(object sender, EventArgs e)
        {
            int dificultad = (int)ViewState["Dificultad"];
            IniciarJuego(dificultad);
        }
    }
}