const listaMedicamentos = [
    {
        id: 'dipirona',
        nome: 'Dipirona',
        tipo: 'Analgésico / Antipirético',
        doseMin: 10,
        doseMax: 25,
        unidade: 'mg/kg/dose',
        efeito: 'Reduz febre e dor por inibição de prostaglandinas. Indicada em dor aguda e hipertermia de qualquer etiologia.'
    },
    {
        id: 'ibuprofeno',
        nome: 'Ibuprofeno',
        tipo: 'Anti-inflamatório / AINE',
        doseMin: 5,
        doseMax: 10,
        unidade: 'mg/kg/dose',
        efeito: 'Inibe COX-1 e COX-2, reduzindo prostaglandinas. Indicado em processos inflamatórios, dor leve a moderada e febre.'
    },
    {
        id: 'amoxicilina',
        nome: 'Amoxicilina',
        tipo: 'Antibiótico — Penicilina',
        doseMin: 25,
        doseMax: 45,
        unidade: 'mg/kg/dia',
        efeito: 'Bactericida de amplo espectro. Indicada em infecções de vias aéreas superiores, otite média e infecções de pele.'
    },
    {
        id: 'paracetamol',
        nome: 'Paracetamol',
        tipo: 'Analgésico / Antipirético',
        doseMin: 10,
        doseMax: 15,
        unidade: 'mg/kg/dose',
        efeito: 'Age centralmente inibindo síntese de prostaglandinas. Primeira escolha em febre e dor leve em crianças e adultos.'
    },
    {
        id: 'dexametasona',
        nome: 'Dexametasona',
        tipo: 'Corticosteroide',
        doseMin: 0.15,
        doseMax: 0.6,
        unidade: 'mg/kg/dose',
        efeito: 'Potente glicocorticoide sintético. Indicada em crupe, edema cerebral, reações alérgicas graves e processos inflamatórios intensos.'
    }
];

function abrirCalculadora() {
    const elementoModalCalculadora = document.getElementById('modal-calculadora');
    elementoModalCalculadora.style.display = 'flex';
    preencherSelectMedicamentos();
}

function fecharCalculadora() {
    document.getElementById('modal-calculadora').style.display = 'none';
}

const elementoModalCalculadora = document.getElementById('modal-calculadora');
if (elementoModalCalculadora) {
    elementoModalCalculadora.addEventListener('click', function (eventoClique) {
        if (eventoClique.target === this) fecharCalculadora();
    });
}


