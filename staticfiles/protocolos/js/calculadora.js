    function abrirCalculadora() {
        document.getElementById('modal-calculadora').style.display = 'flex';
    }

    function fecharCalculadora() {
        document.getElementById('modal-calculadora').style.display = 'none';
    }

    function limpar() {
        document.getElementById('peso').value = '';
        document.getElementById('altura').value = '';
        document.getElementById('medicacao').value = '';
    }

    function calcular() {
        const peso = document.getElementById('peso').value;
        const medicacao = document.getElementById('medicacao').value;

        if (!peso || !medicacao) {
            alert('Preencha todos os campos obrigatórios.');
            return;
        }

        
        alert('calculo para peso jaja ${peso}kg ');
    }

    
    const modalCalc = document.getElementById('modal-calculadora');

    if (modalCalc) {
        modalCalc.addEventListener('click', function(e) {
            if (e.target === this) fecharCalculadora();
        });
    }

document.addEventListener('DOMContentLoaded', () => {
    
    const btnCalcular = document.getElementById('btn-calcular');
    const btnPrescrever = document.getElementById('btn-prescrever');
    
    const inputsFormulario = [
        document.getElementById('peso'),
        document.getElementById('altura'),
        document.getElementById('medicacao')
    ];
    
    const cardAlerta = document.getElementById('card-dinamico-alerta');
    const blocoDica = document.getElementById('bloco-dica');
    const blocoPrescricao = document.getElementById('bloco-prescricao');

    if(btnCalcular) {
        btnCalcular.addEventListener('click', () => {
            btnCalcular.className = 'btn-acao btn-primario';
            btnPrescrever.className = 'btn-acao btn-secundario';

            inputsFormulario.forEach(input => {
                input.classList.remove('input-estado-inativo');
                input.classList.add('input-estado-ativo');
            });

            
            cardAlerta.classList.remove('card-estado-amarelo');
            cardAlerta.classList.add('card-estado-branco');
            blocoDica.style.display = 'block';
            blocoPrescricao.style.display = 'none';

        });
    }

    if(btnPrescrever) {
        btnPrescrever.addEventListener('click', () => {
            // Alterna os botões
            btnCalcular.className = 'btn-acao btn-secundario';
            btnPrescrever.className = 'btn-acao btn-primario';

            inputsFormulario.forEach(input => {
                input.classList.remove('input-estado-ativo');
                input.classList.add('input-estado-inativo');
            });

            cardAlerta.classList.remove('card-estado-branco');
            cardAlerta.classList.add('card-estado-amarelo');
            blocoDica.style.display = 'none';
            blocoPrescricao.style.display = 'block';
        });
    }
});