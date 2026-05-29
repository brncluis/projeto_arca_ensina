let medicoSelecionadoId = null;
let medicoSelecionadoNome = null;

function abrirModalExportar() {
  document.getElementById('modalExportar').style.display = 'flex';
  document.getElementById('campoPesquisaMedico').value = '';
  filtrarMedicos();
}

function fecharModalExportar() {
  document.getElementById('modalExportar').style.display = 'none';
  medicoSelecionadoId = null;
  medicoSelecionadoNome = null;
  document.querySelectorAll('.medico-item').forEach(el => el.classList.remove('selecionado'));
}

function filtrarMedicos() {
  const termo = document.getElementById('campoPesquisaMedico').value.toLowerCase().trim();
  const itens = document.querySelectorAll('#listaMedicos .medico-item');
  const semRes = document.getElementById('nenhumResultado');
  let algumVisivel = false;

  itens.forEach(item => {
    if (item.dataset.nome.includes(termo)) {
      item.style.display = 'block';
      algumVisivel = true;
    } else {
      item.style.display = 'none';
    }
  });

  semRes.style.display = algumVisivel ? 'none' : 'block';
}

function selecionarMedico(el, id, nome) {
  document.querySelectorAll('.medico-item').forEach(i => i.classList.remove('selecionado'));
  el.classList.add('selecionado');
  medicoSelecionadoId = id;
  medicoSelecionadoNome = nome;
}

function confirmarExportacao() {
  if (!medicoSelecionadoId) {
    alert('Selecione um médico antes de confirmar.');
    return;
  }

  fetch(EXPORTAR_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF_TOKEN },
    body: JSON.stringify({ medico_id: medicoSelecionadoId }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.sucesso) {
      fecharModalExportar();
      mostrarToast('Paciente foi exportado!');
    } else {
      mostrarErro(data.erro || 'Tente novamente.');
    }
  })
  .catch(() => mostrarErro('Erro de conexão.'));
}

function mostrarErro(mensagem) {
  const erroExistente = document.getElementById('toastErro');
  if (erroExistente) erroExistente.remove();

  const erro = document.createElement('div');
  erro.id = 'toastErro';
  erro.textContent = mensagem;
  erro.style.cssText = `
    position: fixed;
    bottom: 32px;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: #1a3a5c;
    color: #fff;
    padding: 13px 30px;
    border-radius: 30px;
    font-size: 15px;
    font-weight: 600;
    z-index: 2000;
    box-shadow: 0 4px 24px rgba(0,0,0,0.18);
    opacity: 0;
    transition: opacity 0.3s, transform 0.3s;
    font-family: 'Creato Display', 'Segoe UI', sans-serif;
  `;
  document.body.appendChild(erro);

  void erro.offsetWidth;
  erro.style.opacity = '1';
  erro.style.transform = 'translateX(-50%) translateY(0)';

  setTimeout(() => {
    erro.style.opacity = '0';
    erro.style.transform = 'translateX(-50%) translateY(20px)';
    setTimeout(() => erro.remove(), 350);
  }, 3500);
}

function mostrarToast(mensagem) {
  const toast = document.getElementById('toastConfirmacao');
  toast.textContent = mensagem;
  toast.style.display = 'block';
  void toast.offsetWidth;
  toast.classList.add('visivel');
  setTimeout(() => {
    toast.classList.remove('visivel');
    setTimeout(() => { toast.style.display = 'none'; }, 350);
  }, 3000);
}