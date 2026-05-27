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
const tempos = new Array(passos.length).fill(0);
const timers = new Array(passos.length).fill(null);

let etapaAtiva = null;

function formatarTempo(segundos) {
    const minutos = String(Math.floor(segundos / 60)).padStart(2, "0");
    const seg = String(segundos % 60).padStart(2, "0");

    return `${minutos}:${seg}`;
}

function iniciarTimerEtapa(indice) {
    if (concluidos[indice]) {
        return;
    }

    if (etapaAtiva !== null && etapaAtiva !== indice) {
        pararTimerEtapa(etapaAtiva);
    }

    etapaAtiva = indice;

    if (timers[indice] !== null) {
        return;
    }

    timers[indice] = setInterval(() => {
        tempos[indice]++;

        const elemento = document.getElementById(`timer-etapa-${indice}`);

        if (elemento) {
            elemento.textContent = formatarTempo(tempos[indice]);
        }
    }, 1000);

    renderizarFluxograma();
}

function pararTimerEtapa(indice) {
    if (timers[indice] !== null) {
        clearInterval(timers[indice]);
        timers[indice] = null;
    }

    if (etapaAtiva === indice) {
        etapaAtiva = null;
    }
}

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
        if (!concluidos[i]) {
            return i;
        }
    }

    return -1;
}

function concluirEtapa(indice) {
    if (concluidos[indice]) {
        return;
    }

    const pendente = primeiraEtapaPendente(indice);

    if (pendente !== -1) {
        abrirAvisoPulado(pendente);
        return;
    }

    concluidos[indice] = true;

    pararTimerEtapa(indice);

    atualizarProgresso();
    renderizarFluxograma();
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

        let classes = "card-fluxo-wrap";

        if (concluidos[i]) {
            classes += " concluido";
        }

        if (etapaAtiva === i) {
            classes += " ativa";
        }

        wrap.className = classes;
        wrap.setAttribute("role", "button");
        wrap.setAttribute("tabindex", "0");

        wrap.innerHTML = `
            <div class="card-fluxo-interno">

                <div class="fluxo-card-topo">

                    <span class="fluxo-etapa-titulo">
                        ${texto}
                    </span>

                    <span class="timer-etapa">
                        <img
                            src="/static/protocolos/icons/Timer.svg"
                            alt="Tempo"
                            class="icone-timer"
                        >

                        <span id="timer-etapa-${i}">
                            ${formatarTempo(tempos[i])}
                        </span>
                    </span>

                </div>

                <div class="fluxo-card-rodape">
                    <button
                        type="button"
                        class="btn-concluir-etapa"
                        ${concluidos[i] ? "disabled" : ""}
                        onclick="event.stopPropagation(); concluirEtapa(${i})"
                    >
                        ${concluidos[i] ? "✓ Concluída" : "✓ Concluir"}
                    </button>
                </div>

            </div>
        `;

        wrap.addEventListener("click", () => {
            iniciarTimerEtapa(i);
        });

        wrap.addEventListener("keydown", e => {
            if (e.key === " " || e.key === "Enter") {
                e.preventDefault();
                iniciarTimerEtapa(i);
            }
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
    timers.forEach((timer, i) => {
        if (timer !== null) {
            clearInterval(timer);
            timers[i] = null;
        }
    });

    concluidos.fill(false);
    tempos.fill(0);
    etapaAtiva = null;

    atualizarProgresso();
    renderizarFluxograma();
}

function mudarAba(aba) {
    document.querySelectorAll(".tab-content").forEach(el => {
        el.classList.remove("ativo");
    });

    document.getElementById("conteudo-" + aba).classList.add("ativo");

    document.querySelectorAll(".tab").forEach(el => {
        el.classList.remove("ativo");
    });

    document.getElementById("tab-" + aba).classList.add("ativo");
}

renderizarFluxograma();
mudarAba("fluxograma");