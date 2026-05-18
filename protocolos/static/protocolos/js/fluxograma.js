const passos = [
    "Informações",
    "Informações",
    "Informações",
    "Informações",
    "Informações",
    "Informações",
    "Informações",
    "Informações",
    "Informações",
    "Informações"
];

const concluidos = new Array(passos.length).fill(false);


function abrirAvisoPulado(etapaFaltante) {

    const numero = document.getElementById("aviso-etapa-numero");

    if (numero) {
        numero.textContent = etapaFaltante + 1;
    }

    document.getElementById("modal-etapa-pulada").style.display = "flex";
}


function fecharAvisoPulado() {
    document.getElementById("modal-etapa-pulada").style.display = "none";
}


function primeiraEtapaPendente(ate) {
    for (let i = 0; i < ate; i++) {
        if (!concluidos[i]) return i;
    }
    return -1;
}


function renderizarFluxograma() {
    const lista = document.getElementById("lista-fluxograma");
    lista.innerHTML = "";

    passos.forEach((texto, i) => {

        if (i > 0) {
            const seta = document.createElement("div");
            seta.className = "fluxo-seta";
            seta.textContent = "↓";
            lista.appendChild(seta);
        }

        const wrap = document.createElement("div");
        wrap.className = "card-fluxo-wrap" + (concluidos[i] ? " concluido" : "");
        wrap.setAttribute("role", "checkbox");
        wrap.setAttribute("aria-checked", String(concluidos[i]));
        wrap.setAttribute("tabindex", "0");

        wrap.innerHTML = `
            <div class="card-fluxo-interno">
                <span>${texto}</span>
                <span class="card-check">${concluidos[i] ? "✓" : ""}</span>
            </div>
        `;

        const toggle = () => {
            const estaAtivando = !concluidos[i];

            if (estaAtivando) {
                const pendente = primeiraEtapaPendente(i);
                if (pendente !== -1) {
                    abrirAvisoPulado(pendente);
                    return; /* interrompe — não muda nada */
                }
            }

            concluidos[i] = !concluidos[i];
            atualizarProgresso();
            renderizarFluxograma();
        };

        wrap.addEventListener("click", toggle);
        wrap.addEventListener("keydown", e => {
            if (e.key === " " || e.key === "Enter") { e.preventDefault(); toggle(); }
        });

        lista.appendChild(wrap);
    });
}

function atualizarProgresso() {
    const feitos = concluidos.filter(Boolean).length;
    document.getElementById("texto-progresso").textContent =
        `${feitos} / ${passos.length} concluídos`;
}

function resetarFluxograma() {
    concluidos.fill(false);
    atualizarProgresso();
    renderizarFluxograma();
}

function mudarAba(aba) {
    document.querySelectorAll(".tab-content").forEach(el => el.classList.remove("ativo"));
    document.getElementById("conteudo-" + aba).classList.add("ativo");

    document.querySelectorAll(".tab").forEach(el => el.classList.remove("ativo"));
    document.getElementById("tab-" + aba).classList.add("ativo");
}

renderizarFluxograma();
mudarAba('fluxograma');