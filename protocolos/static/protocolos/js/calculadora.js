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