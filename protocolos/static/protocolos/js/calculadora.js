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


function preencherSelectMedicamentos() {
    const selectMedicamentos = document.getElementById('medicacao');
    if (selectMedicamentos.options.length > 1) return; 
    listaMedicamentos.forEach(medicamento => {
        const opcaoMedicamento = document.createElement('option');
        opcaoMedicamento.value = medicamento.id;
        opcaoMedicamento.textContent = medicamento.nome;
        selectMedicamentos.appendChild(opcaoMedicamento);
    });
}


function limpar() {
    document.getElementById('peso').value = '';
    document.getElementById('altura').value = '';
    document.getElementById('medicacao').value = '';
    esconderResultado();
}

function calcular() {
    const pesoPaciente = parseFloat(document.getElementById('peso').value);
    const idMedicamentoSelecionado = document.getElementById('medicacao').value;

    if (!pesoPaciente || !idMedicamentoSelecionado) {
        alert('Preencha o peso e selecione uma medicação.');
        return;
    }

    const medicamentoSelecionado = listaMedicamentos.find(
        medicamentoAtual => medicamentoAtual.id === idMedicamentoSelecionado
    );
    if (!medicamentoSelecionado) return;

    const doseMinimaCalculada = (medicamentoSelecionado.doseMin * pesoPaciente).toFixed(2);
    const doseMaximaCalculada = (medicamentoSelecionado.doseMax * pesoPaciente).toFixed(2);


    exibirResultado(medicamentoSelecionado, doseMinimaCalculada, doseMaximaCalculada);
}

function exibirResultado(medicamentoSelecionado, doseMinimaCalculada, doseMaximaCalculada) {
    document.getElementById('resultado-nome-farmaco').textContent = medicamentoSelecionado.nome;
    document.getElementById('resultado-tipo-farmaco').textContent = medicamentoSelecionado.tipo;
    document.getElementById('resultado-dose').textContent = `${doseMinimaCalculada} – ${doseMaximaCalculada} ${medicamentoSelecionado.unidade}`;
    document.getElementById('resultado-efeito').textContent = medicamentoSelecionado.efeito;

    document.getElementById('calculadora-resultado').style.display = 'flex';
    document.getElementById('calculadora-placeholder').style.display = 'none';
}

function esconderResultado() {
    document.getElementById('calculadora-resultado').style.display = 'none';
    document.getElementById('calculadora-placeholder').style.display = 'block';
}