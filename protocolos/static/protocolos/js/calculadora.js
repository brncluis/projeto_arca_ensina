const lista_medicamentos = [
    {
        id: 'dipirona',
        nome: 'Dipirona',
        tipo: 'Analgésico / Antipirético',
        dose_min: 10,
        dose_max: 25,
        unidade: 'mg/kg/dose',
        efeito: 'Reduz febre e dor por inibição de prostaglandinas. Indicada em dor aguda e hipertermia de qualquer etiologia.'
    },
    {
        id: 'ibuprofeno',
        nome: 'Ibuprofeno',
        tipo: 'Anti-inflamatório / AINE',
        dose_min: 5,
        dose_max: 10,
        unidade: 'mg/kg/dose',
        efeito: 'Inibe COX-1 e COX-2, reduzindo prostaglandinas. Indicado em processos inflamatórios, dor leve a moderada e febre.'
    },
    {
        id: 'amoxicilina',
        nome: 'Amoxicilina',
        tipo: 'Antibiótico — Penicilina',
        dose_min: 25,
        dose_max: 45,
        unidade: 'mg/kg/dia',
        efeito: 'Bactericida de amplo espectro. Indicada em infecções de vias aéreas superiores, otite média e infecções de pele.'
    },
    {
        id: 'paracetamol',
        nome: 'Paracetamol',
        tipo: 'Analgésico / Antipirético',
        dose_min: 10,
        dose_max: 15,
        unidade: 'mg/kg/dose',
        efeito: 'Age centralmente inibindo síntese de prostaglandinas. Primeira escolha em febre e dor leve em crianças e adultos.'
    },
    {
        id: 'dexametasona',
        nome: 'Dexametasona',
        tipo: 'Corticosteroide',
        dose_min: 0.15,
        dose_max: 0.6,
        unidade: 'mg/kg/dose',
        efeito: 'Potente glicocorticoide sintético. Indicada em crupe, edema cerebral, reações alérgicas graves e processos inflamatórios intensos.'
    }
];

function abrir_calculadora() {
    document.getElementById('modal-calculadora').style.display = 'flex';
    preencher_select_medicamentos();
}

function fechar_calculadora() {
    document.getElementById('modal-calculadora').style.display = 'none';
}

const modal_calculadora = document.getElementById('modal-calculadora');
if (modal_calculadora) {
    modal_calculadora.addEventListener('click', function(evento) {
        if (evento.target === this) fechar_calculadora();
    });
}

function preencher_select_medicamentos() {
    const select = document.getElementById('medicacao');
    if (select.options.length > 1) return;
    lista_medicamentos.forEach(medicamento => {
        const opcao = document.createElement('option');
        opcao.value = medicamento.id;
        opcao.textContent = medicamento.nome;
        select.appendChild(opcao);
    });
}

function limpar() {
    document.getElementById('peso').value = '';
    document.getElementById('altura').value = '';
    document.getElementById('medicacao').value = '';
    esconder_resultado();
}

function calcular() {
    const peso = parseFloat(document.getElementById('peso').value);
    const id_medicamento = document.getElementById('medicacao').value;

    if (!peso || !id_medicamento) {
        alert('Preencha o peso e selecione uma medicação.');
        return;
    }

    const medicamento = lista_medicamentos.find(m => m.id === id_medicamento);
    if (!medicamento) return;

    const dose_minima = (medicamento.dose_min * peso).toFixed(2);
    const dose_maxima = (medicamento.dose_max * peso).toFixed(2);

    exibir_resultado(medicamento, dose_minima, dose_maxima);
}

function exibir_resultado(medicamento, dose_minima, dose_maxima) {
    document.getElementById('resultado-nome-farmaco').textContent = medicamento.nome;
    document.getElementById('resultado-tipo-farmaco').textContent = medicamento.tipo;
    document.getElementById('resultado-dose').textContent = `${dose_minima} – ${dose_maxima} ${medicamento.unidade}`;
    document.getElementById('resultado-efeito').textContent = medicamento.efeito;

    document.getElementById('calculadora-resultado').style.display = 'flex';
    document.getElementById('calculadora-placeholder').style.display = 'none';
}

function esconder_resultado() {
    document.getElementById('calculadora-resultado').style.display = 'none';
    document.getElementById('calculadora-placeholder').style.display = 'block';
}