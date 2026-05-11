/* ─────────────────────────────────────────
   Dados do fluxograma
   Substitua pelos passos reais do protocolo.
   Para vir do Django: const passos = {{ passos_fluxograma|safe }};
───────────────────────────────────────── */
const passos = [
    "Informações",
    "Informações",
    "Informações",
    "Informações",
];
 
const concluidos = new Array(passos.length).fill(false);
 
function renderizarFluxograma() {
    const lista = document.getElementById("lista-fluxograma");
    lista.innerHTML = "";
 
    passos.forEach((texto, i) => {
 
        /* Seta separadora (não aparece antes do primeiro card) */
        if (i > 0) {
            const seta = document.createElement("div");
            seta.className = "fluxo-seta";
            seta.textContent = "↓";
            lista.appendChild(seta);
        }
 
        /* Card clicável */
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
 
/* Inicializa o fluxograma na carga da página */
renderizarFluxograma();