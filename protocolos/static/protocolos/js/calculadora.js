const lista_medicamentos = [
    { id: 'dipirona',     nome: 'Dipirona',     tipo: 'Analgésico / Antipirético', dose_min: 10,   dose_max: 20,  unidade: 'mg/kg/dose', dose_maxima_absoluta: 1000, efeito: 'Reduz febre e dor por inibição de prostaglandinas. Dose a cada 6h.' },
    { id: 'ibuprofeno',   nome: 'Ibuprofeno',   tipo: 'Anti-inflamatório / AINE',  dose_min: 5,    dose_max: 10,  unidade: 'mg/kg/dose', dose_maxima_absoluta: 400,  efeito: 'Inibe COX-1 e COX-2. Dose a cada 6–8h. Não usar em < 3 meses.' },
    { id: 'amoxicilina',  nome: 'Amoxicilina',  tipo: 'Antibiótico — Penicilina',  dose_min: 25,   dose_max: 50,  unidade: 'mg/kg/dia',  dose_maxima_absoluta: 3000, efeito: 'Bactericida de amplo espectro. Dividir em 2–3 doses/dia.' },
    { id: 'paracetamol',  nome: 'Paracetamol',  tipo: 'Analgésico / Antipirético', dose_min: 10,   dose_max: 15,  unidade: 'mg/kg/dose', dose_maxima_absoluta: 750,  efeito: 'Primeira escolha em febre e dor leve. Dose a cada 6h.' },
    { id: 'dexametasona', nome: 'Dexametasona', tipo: 'Corticosteroide',            dose_min: 0.15, dose_max: 0.6, unidade: 'mg/kg/dose', dose_maxima_absoluta: 10,   efeito: '0,15 mg/kg crupe leve; 0,6 mg/kg crupe grave. Máx 10 mg/dose.' },
];

let pacienteAtual = null;
let ultimoCalculo = null;

function mostrarAlerta(mensagem, tipo = 'sucesso') {
    let box = document.getElementById('alerta-flutuante');
    if (!box) {
        box = document.createElement('div');
        box.id = 'alerta-flutuante';
        box.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;padding:.8rem 1.4rem;border-radius:10px;font-size:.9rem;font-weight:500;opacity:0;transform:translateY(12px);transition:opacity .3s,transform .3s;z-index:2000;pointer-events:none;max-width:380px;color:#fff;';
        document.body.appendChild(box);
    }
    box.textContent          = mensagem;
    box.style.background     = tipo === 'erro' ? '#c0392b' : '#1a1a1a';
    box.style.opacity        = '1';
    box.style.transform      = 'translateY(0)';
    clearTimeout(box._timer);
    box._timer = setTimeout(() => { box.style.opacity = '0'; box.style.transform = 'translateY(12px)'; }, 4000);
}

function getCookie(name) {
    const parts = `; ${document.cookie}`.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}

function onPacienteChange() {
    const id = document.getElementById('select-paciente').value;
    if (!id) { pacienteAtual = null; limparResultado(); return; }

    fetch(`/dashboard/paciente/${id}/dados/`)
        .then(r => r.json())
        .then(data => {
            pacienteAtual = { id: parseInt(id), ...data };
            document.getElementById('info-peso').textContent   = `${data.peso} kg`;
            document.getElementById('info-altura').textContent = `${data.altura} cm`;
            document.getElementById('bloco-info-paciente').style.display = 'flex';
            calcular();
        })
        .catch(() => mostrarAlerta('Erro ao buscar dados do paciente.', 'erro'));
}

function onMedicamentoChange() {
    if (pacienteAtual) calcular();
}

function calcular() {
    const id_med = document.getElementById('medicacao').value;
    if (!pacienteAtual || !id_med) return;

    const med      = lista_medicamentos.find(m => m.id === id_med);
    const peso     = pacienteAtual.peso;
    const dose_min = Math.min(med.dose_min * peso, med.dose_maxima_absoluta).toFixed(2);
    const dose_max = Math.min(med.dose_max * peso, med.dose_maxima_absoluta).toFixed(2);

    ultimoCalculo = {
        nome_medicamento: med.nome,
        tipo_medicamento: med.tipo,
        dose_calculada:   `${dose_min} – ${dose_max}`,
        unidade:          med.unidade,
        peso_utilizado:   peso,
        paciente_id:      pacienteAtual.id,
    };

    document.getElementById('resultado-nome-farmaco').textContent = med.nome;
    document.getElementById('resultado-tipo-farmaco').textContent = med.tipo;
    document.getElementById('resultado-dose').textContent         = `${dose_min} – ${dose_max} ${med.unidade}`;
    document.getElementById('resultado-efeito').textContent       = med.efeito;
    document.getElementById('bloco-dica').style.display           = 'block';
    document.getElementById('bloco-prescricao').style.display     = 'none';
    document.getElementById('calculadora-placeholder').style.display = 'none';
    document.getElementById('calculadora-resultado').style.display   = 'block';
}

function limparResultado() {
    document.getElementById('bloco-info-paciente').style.display     = 'none';
    document.getElementById('calculadora-placeholder').style.display = 'block';
    document.getElementById('calculadora-resultado').style.display   = 'none';
    ultimoCalculo = null;
}

function prescrever() {
    if (!ultimoCalculo) { mostrarAlerta('Selecione um paciente e uma medicação primeiro.', 'erro'); return; }

    const btn = document.getElementById('btn-prescrever');
    btn.disabled    = true;
    btn.textContent = 'Salvando…';

    fetch('/dashboard/prescrever/', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
        body:    JSON.stringify(ultimoCalculo),
    })
    .then(r => r.json())
    .then(data => {
        btn.disabled    = false;
        btn.textContent = 'Prescrever';
        if (data.sucesso) {
            mostrarAlerta(`✅ ${data.mensagem}`);
            const bloco = document.getElementById('bloco-prescricao');
            bloco.innerHTML     = `<p><strong>✅ Prescrição registrada</strong></p><p>${data.mensagem}</p>`;
            bloco.style.display = 'block';
            document.getElementById('bloco-dica').style.display = 'none';
        } else {
            mostrarAlerta(`Erro: ${data.erro}`, 'erro');
        }
    })
    .catch(() => {
        btn.disabled    = false;
        btn.textContent = 'Prescrever';
        mostrarAlerta('Erro ao comunicar com o servidor.', 'erro');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const selectMed = document.getElementById('medicacao');
    lista_medicamentos.forEach(med => {
        const opt       = document.createElement('option');
        opt.value       = med.id;
        opt.textContent = med.nome;
        selectMed.appendChild(opt);
    });

    document.getElementById('select-paciente').addEventListener('change', onPacienteChange);
    document.getElementById('medicacao').addEventListener('change', onMedicamentoChange);
    document.getElementById('btn-prescrever').addEventListener('click', prescrever);
});

function abrirCalculadora() {
    const modal = document.getElementById('modal-calculadora');
    if (modal) modal.style.display = 'flex';

    const select = document.getElementById('medicacao');
    if (select && select.options.length <= 1) {
        lista_medicamentos.forEach(med => {
            const opt = document.createElement('option');
            opt.value       = med.id;
            opt.textContent = med.nome;
            select.appendChild(opt);
        });
    }
}

function fecharCalculadora() {
    const modal = document.getElementById('modal-calculadora');
    if (modal) modal.style.display = 'none';
}