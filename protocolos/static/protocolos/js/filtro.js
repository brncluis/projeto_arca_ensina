function buscarProtocolo(termo) {
    const t = termo.toLowerCase();
    document.querySelectorAll(".sub_header").forEach(card => {
        const nome = card.querySelector("h2")?.textContent.toLowerCase() || "";
        card.style.display = nome.includes(t) ? "" : "none";
    });
}