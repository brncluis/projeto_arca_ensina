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
      alert('Erro: ' + (data.erro || 'Tente novamente.'));
    }
  })
  .catch(() => alert('Erro de conexão.'));
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