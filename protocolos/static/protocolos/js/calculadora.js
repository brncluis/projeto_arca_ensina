const lista_medicamentos = [
    {
        id: 'dipirona',
        nome: 'Dipirona',
        tipo: 'Analgésico / Antipirético',
        dose_min: 10,
        dose_max: 20,
        unidade: 'mg/kg/dose',
        dose_maxima_absoluta: 1000,
        efeito: 'Reduz febre e dor por inibição de prostaglandinas. Dose a cada 6h. Indicada em dor aguda e hipertermia de qualquer etiologia.'
    },
    {
        id: 'ibuprofeno',
        nome: 'Ibuprofeno',
        tipo: 'Anti-inflamatório / AINE',
        dose_min: 5,
        dose_max: 10,
        unidade: 'mg/kg/dose',
        dose_maxima_absoluta: 400,
        efeito: 'Inibe COX-1 e COX-2. Dose a cada 6–8h. Indicado em febre, dor leve a moderada e processos inflamatórios. Não usar em < 3 meses.'
    },
    {
        id: 'amoxicilina',
        nome: 'Amoxicilina',
        tipo: 'Antibiótico — Penicilina',
        dose_min: 25,
        dose_max: 50,
        unidade: 'mg/kg/dia',
        dose_maxima_absoluta: 3000,
        efeito: 'Bactericida de amplo espectro. Dividir em 2–3 doses/dia. Indicada em otite média, faringite, pneumonia e infecções de pele.'
    },
    {
        id: 'paracetamol',
        nome: 'Paracetamol',
        tipo: 'Analgésico / Antipirético',
        dose_min: 10,
        dose_max: 15,
        unidade: 'mg/kg/dose',
        dose_maxima_absoluta: 750,
        efeito: 'Primeira escolha em febre e dor leve. Dose a cada 6h. Dose diária máxima: 60 mg/kg/dia ou 4g/dia em adolescentes.'
    },
    {
        id: 'dexametasona',
        nome: 'Dexametasona',
        tipo: 'Corticosteroide',
        dose_min: 0.15,
        dose_max: 0.6,
        unidade: 'mg/kg/dose',
        dose_maxima_absoluta: 10,
        efeito: 'Dose única. 0,15 mg/kg para crupe leve; 0,6 mg/kg para crupe moderada/grave (padrão-ouro SBP). Máximo 10 mg/dose.'
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
    alertBox.innerHTML = `<span></span> ${mensagem}`;
    alertBox.classList.add('mostrar');
    setTimeout(() => { alertBox.classList.remove('mostrar'); }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('medicacao');
    if (select) {
        lista_medicamentos.forEach(med => {
            const opcao = document.createElement('option');
            opcao.value = med.id;
            opcao.textContent = med.nome;
            select.appendChild(opcao);
        });
    }

    const btnCalcular = document.getElementById('btn-calcular');
    const btnPrescrever = document.getElementById('btn-prescrever');
    const btnSalvar = document.getElementById('btn-salvar');

    if (btnCalcular) btnCalcular.addEventListener('click', calcular);

    if (btnPrescrever) {
        btnPrescrever.addEventListener('click', () => {
            const dica = document.getElementById('bloco-dica');
            const prescricao = document.getElementById('bloco-prescricao');
            const ativo = prescricao.style.display !== 'none';
            if (ativo) {
                prescricao.style.display = 'none';
                dica.style.display = 'block';
            } else {
                dica.style.display = 'none';
                prescricao.style.display = 'block';
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

    const dose_minima = Math.min(medicamento.dose_min * peso, medicamento.dose_maxima_absoluta).toFixed(2);
    const dose_maxima = Math.min(medicamento.dose_max * peso, medicamento.dose_maxima_absoluta).toFixed(2);

    document.getElementById('resultado-nome-farmaco').textContent = medicamento.nome;
    document.getElementById('resultado-tipo-farmaco').textContent = medicamento.tipo;
    document.getElementById('resultado-dose').textContent = `${dose_minima} – ${dose_maxima} ${medicamento.unidade}`;
    document.getElementById('resultado-efeito').textContent = medicamento.efeito;

    document.getElementById('bloco-dica').style.display = 'block';
    document.getElementById('bloco-prescricao').style.display = 'none';

    mostrarAlerta('Cálculo realizado com sucesso!');
}

function abrirCalculadora() {
    const modal = document.getElementById('modal-calculadora');
    if (modal) modal.style.display = 'flex';

    const select = document.getElementById('medicacao');
    if (select && select.options.length <= 1) {
        lista_medicamentos.forEach(med => {
            const opcao = document.createElement('option');
            opcao.value = med.id;
            opcao.textContent = med.nome;
            select.appendChild(opcao);
        });
    }
}

function fecharCalculadora() {
    const modal = document.getElementById('modal-calculadora');
    if (modal) modal.style.display = 'none';
}