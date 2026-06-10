function buscarSugestoes(termo) {
    const dropdown = document.getElementById("dropdown-sugestoes");
    if (!termo.trim()) { dropdown.style.display = "none"; return; }

    const t = termo.toLowerCase();
    const resultados = protocolos.filter(p => p.nome.toLowerCase().includes(t));

    dropdown.innerHTML = "";

    if (resultados.length === 0) {
        dropdown.innerHTML = `<div class="sugestao-item sugestao-vazio">Protocolo não encontrado</div>`;
    } else {
        resultados.forEach(p => {
            const item = document.createElement("div");
            item.className = "sugestao-item";
            item.textContent = p.nome;
            item.onclick = () => window.location.href = p.url;
            dropdown.appendChild(item);
        });
    }

    dropdown.style.display = "block";
}

document.addEventListener("click", (e) => {
    if (!e.target.closest(".busca2-wrapper")) {
        document.getElementById("dropdown-sugestoes").style.display = "none";
    }
});