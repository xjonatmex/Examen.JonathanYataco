$(document).ready(function () {
    $(".carta").click(function () {
        let carta = $(this);
        carta.addClass("volteada");

        setTimeout(function () {
            carta.removeClass("volteada");
        }, 1000);
    });
});
