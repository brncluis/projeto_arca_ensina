document.addEventListener("DOMContentLoaded", () => {

    const abrir = document.getElementById("abrirFiltro");
    const fechar = document.getElementById("fecharFiltro");
    const modal = document.getElementById("modal-filtro");

    if (abrir && modal) {
        abrir.addEventListener("click", () => {
            modal.classList.add("ativo");
        });
    }

    if (fechar && modal) {
        fechar.addEventListener("click", () => {
            modal.classList.remove("ativo");
        });
    }

    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) {
                modal.classList.remove("ativo");
            }
        });
    }

});

function fecharFiltro() {
    document.getElementById("modal-filtro").classList.remove("ativo");
}

function filtrarSintomas(termo) {
    const t = termo.toLowerCase();

    document.querySelectorAll(".grupo").forEach(grupo => {
        let temVisivel = false;

        grupo.querySelectorAll("label").forEach(label => {
            const texto = label.textContent.toLowerCase();

            if (texto.includes(t)) {
                label.style.display = "block";
                temVisivel = true;
            } else {
                label.style.display = "none";
            }
        });

        // esconde categoria inteira se nada aparecer
        grupo.style.display = temVisivel ? "block" : "none";
    });
}

function limparFiltros() {
    document.querySelectorAll('input[name="sintomas"]').forEach(cb => {
        cb.checked = false;
    });
}

function aplicarFiltros() {
    const marcados = document.querySelectorAll('input[name="sintomas"]:checked');
    if (marcados.length === 0) {
        return;
    }
    document.querySelector('#modal-filtro form').submit();
}