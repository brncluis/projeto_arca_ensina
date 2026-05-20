function abrirConsulta() {
    document.getElementById('modal-consulta').style.display = 'flex';
}

function irParaProtocolos() {
    window.location.href = URL_PROTOCOLOS;
}

function abrirCadastrar() {
    document.getElementById('modal-consulta').style.display = 'none';
    document.getElementById('modal-cadastrar').style.display = 'flex';
}

function fecharCadastrar() {
    document.getElementById('modal-cadastrar').style.display = 'none';
}

function fecharConsulta() {
    document.getElementById('modal-consulta').style.display = 'none';
}


function salvarPaciente() {
    const nome = document.getElementById('nome').value;
    const idade = document.getElementById('idade').value;
    const peso = document.getElementById('peso').value;
    const altura = document.getElementById('altura').value;

    console.log({ nome, idade, peso, altura });

    fecharCadastrar();
    window.location.href = URL_PROTOCOLOS;
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('modal-consulta').addEventListener('click', function (e) {
        if (e.target === this) irParaProtocolos();
    });

    document.getElementById('modal-cadastrar').addEventListener('click', function (e) {
        if (e.target === this) fecharCadastrar();
    });
});