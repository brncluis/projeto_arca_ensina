function getFavoritos() {
    return JSON.parse(localStorage.getItem("favoritos") || "[]");
}

function toggleFavorito(event, id, titulo) {
    event.preventDefault();
    event.stopPropagation();
    let favoritos = getFavoritos();
    const idx = favoritos.findIndex(f => f.id === id);
    if (idx === -1) { favoritos.push({ id, titulo }); }
    else { favoritos.splice(idx, 1); }
    localStorage.setItem("favoritos", JSON.stringify(favoritos));
    atualizarEstrelas();
    const tabAtiva = document.querySelector(".tab.ativo")?.textContent.trim();
    if (tabAtiva === "Favoritos") filtrarFavoritos();
}

function atualizarEstrelas() {
    const favoritos = getFavoritos();
    document.querySelectorAll(".sub_header").forEach(card => {
        const ehFav = favoritos.some(f => f.id === card.dataset.id);
        const svg = card.querySelector(".icone-estrela");
        if (svg) svg.setAttribute("fill", ehFav ? "#3b5fc0" : "none");
    });
}

function mudarTab(aba, botao) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("ativo"));
    botao.classList.add("ativo");
    document.getElementById("msg-favoritos-vazio").style.display = "none";
    document.getElementById("msg-recentes-vazio").style.display = "none";

    if (aba === "todos") {
        restaurarOrdem();
        document.querySelectorAll("a:has(.sub_header)").forEach(l => l.style.display = "");
    } else if (aba === "favoritos") {
        restaurarOrdem();
        filtrarFavoritos();
    } else if (aba === "recentes") {
        filtrarRecentes();
    }
}

function filtrarFavoritos() {
    const favoritos = getFavoritos();
    let algum = false;
    document.querySelectorAll("a:has(.sub_header)").forEach(link => {
        const card = link.querySelector(".sub_header");
        const ehFav = favoritos.some(f => f.id === card.dataset.id);
        link.style.display = ehFav ? "" : "none";
        if (ehFav) algum = true;
    });
    document.getElementById("msg-favoritos-vazio").style.display = algum ? "none" : "";
}

function filtrarRecentes() {
    const recentes = JSON.parse(localStorage.getItem("recentes") || "[]");
    const lista = document.getElementById("lista-protocolos");
    const msgRec = document.getElementById("msg-recentes-vazio");

    document.querySelectorAll("a:has(.sub_header)").forEach(link => link.style.display = "none");

    let algum = false;
    recentes.forEach(rec => {
        const card = document.querySelector(`.sub_header[data-id="${rec.id}"]`);
        if (card) {
            const link = card.closest("a") || card.parentElement;
            link.style.display = "";
            lista.insertBefore(link, msgRec);
            algum = true;
        }
    });

    msgRec.style.display = algum ? "none" : "";
}

document.addEventListener("DOMContentLoaded", () => {
    atualizarEstrelas();
    document.querySelectorAll("a:has(.sub_header)").forEach(link => {
        link.addEventListener("click", function() {
            const card = this.querySelector(".sub_header");
            let recentes = JSON.parse(localStorage.getItem("recentes") || "[]");
            recentes = recentes.filter(r => r.id !== card.dataset.id);
            recentes.unshift({ id: card.dataset.id, titulo: card.dataset.titulo });
            localStorage.setItem("recentes", JSON.stringify(recentes.slice(0, 10)));
        });
    });
});

function restaurarOrdem() {
    const lista = document.getElementById("lista-protocolos");
    const msgFav = document.getElementById("msg-favoritos-vazio");
    const ordemOriginal = [...lista.querySelectorAll("a:has(.sub_header)")]
        .sort((a, b) => {
            const idA = a.querySelector(".sub_header").dataset.id;
            const idB = b.querySelector(".sub_header").dataset.id;
            return idA - idB;
        });
    ordemOriginal.forEach(link => lista.insertBefore(link, msgFav));
}