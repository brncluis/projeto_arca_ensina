const lista_medicamentos = [
    {
        id: 'dipirona',
        nome: 'Dipirona',
        tipo: 'Analgésico / Antipirético',
        dose_min: 10,
        dose_max: 25,
        unidade: 'mg/dose',
        efeito: 'Reduz febre e dor por inibição de prostaglandinas. Indicada em dor aguda e hipertermia de qualquer etiologia.'
    },
    {
        id: 'ibuprofeno',
        nome: 'Ibuprofeno',
        tipo: 'Anti-inflamatório / AINE',
        dose_min: 5,
        dose_max: 10,
        unidade: 'mg/dose',
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
        unidade: 'mg/dose',
        efeito: 'Age centralmente inibindo síntese de prostaglandinas. Primeira escolha em febre e dor leve em crianças e adultos.'
    },
    {
        id: 'dexametasona',
        nome: 'Dexametasona',
        tipo: 'Corticosteroide',
        dose_min: 0.15,
        dose_max: 0.6,
        unidade: 'mg/dose',
        efeito: 'Potente glicocorticoide sintético. Indicada em crupe, edema cerebral, reações alérgicas graves e processos inflamatórios intensos.'
    }
];

function mostrarAlerta(mensagem) {
    let alertBox = document.getElementById('alerta-sucesso-flutuante');

    if (!alertBox) {
        alertBox = document.createElement('div');
        alertBox.id = 'alerta-sucesso-flutuante';
        alertBox.className = 'alerta-confirmacao';
        document.body.appendChild(alertBox);
    }

    alertBox.innerHTML = `<span>✅</span> ${mensagem}`;
    alertBox.classList.add('mostrar');

    setTimeout(() => {
        alertBox.classList.remove('mostrar');
    }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    // Preencher select de medicamentos
    const select = document.getElementById('medicacao');
    lista_medicamentos.forEach(med => {
        const opcao = document.createElement('option');
        opcao.value = med.id;
        opcao.textContent = med.nome;
        select.appendChild(opcao);
    });

    const btnCalcular = document.getElementById('btn-calcular');
    const btnPrescrever = document.getElementById('btn-prescrever');
    const btnSalvar = document.getElementById('btn-salvar');

    if (btnCalcular) {
        btnCalcular.addEventListener('click', () => {
            calcular();
        });
    }

    if (btnPrescrever) {
        btnPrescrever.addEventListener('click', () => {
            const resultado = document.getElementById('calculadora-resultado');
            if (resultado.style.display === 'none') return;

            const dica = document.getElementById('bloco-dica');
            const prescricao = document.getElementById('bloco-prescricao');
            const ativo = prescricao.style.display !== 'none';

            if (ativo) {
                prescricao.style.display = 'none';
                dica.style.display = 'block';
                btnPrescrever.className = 'calc-btn calc-btn-secundario';
                btnCalcular.className = 'calc-btn calc-btn-primario';
            } else {
                dica.style.display = 'none';
                prescricao.style.display = 'block';
                btnPrescrever.className = 'calc-btn calc-btn-primario';
                btnCalcular.className = 'calc-btn calc-btn-secundario';
            }
        });
    }

    if (btnSalvar) {
        btnSalvar.addEventListener('click', () => {
            mostrarAlerta('Prescrição salva com sucesso no sistema!');
        });
    }
});

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

    document.getElementById('resultado-nome-farmaco').textContent = medicamento.nome;
    document.getElementById('resultado-tipo-farmaco').textContent = medicamento.tipo;
    document.getElementById('resultado-dose').textContent = `${dose_minima} – ${dose_maxima} ${medicamento.unidade}`;
    document.getElementById('resultado-efeito').textContent = medicamento.efeito;

    document.getElementById('calculadora-resultado').style.display = 'flex';
    document.getElementById('calculadora-placeholder').style.display = 'none';

    document.getElementById('bloco-dica').style.display = 'block';
    document.getElementById('bloco-prescricao').style.display = 'none';
    document.getElementById('btn-prescrever').className = 'calc-btn calc-btn-secundario';
    document.getElementById('btn-calcular').className = 'calc-btn calc-btn-primario';

    mostrarAlerta('Cálculo realizado com sucesso!');
}