const fluxoDengue = {
    inicio: {
        titulo: "Classificação inicial",
        descricao: `
            Selecione o grupo do paciente conforme os sinais apresentados.
        `,
        opcoes: [
            {
                texto: "Grupo C - com sinais de alerta, sem sinais de gravidade",
                proxima: "grupo_c"
            },
            {
                texto: "Grupo D - com sinais de gravidade",
                proxima: "grupo_d"
            }
        ]
    },

    grupo_c: {
        titulo: "Dengue Grupo C",
        descricao: `
            Paciente com sinais de alerta, mas sem sinais de gravidade.

            Sinais de alerta:
            dor abdominal intensa, vômitos persistentes, acúmulo de líquidos cavitários,
            hipotensão postural, hepatomegalia maior que 2 cm, sangramento de mucosa,
            letargia ou irritabilidade e aumento progressivo do hematócrito.
        `,
        opcoes: [
            {
                texto: "Solicitar exames do Grupo C",
                proxima: "exames_grupo_c"
            }
        ]
    },

    exames_grupo_c: {
        titulo: "Exames - Grupo C",
        descricao: `
            Solicitar:
            hemograma, albumina, ionograma, AST, ALT e coagulograma.

            Recomendado de acordo com a clínica:
            RX de tórax e US abdominal.
        `,
        opcoes: [
            {
                texto: "Iniciar expansão com SF 0,9%",
                proxima: "expansao_grupo_c"
            }
        ]
    },

    expansao_grupo_c: {
        titulo: "Expansão - Grupo C",
        descricao: `
            SF 0,9% - 10 ml/kg em 1 hora.

            Reavaliar:
            se não houver congestão, repetir SF 0,9% - 10 ml/kg em 1 hora.

            Solicitar Hct/Hg em até 2 horas da expansão.
        `,
        opcoes: [
            {
                texto: "Sem queda do Hct ou sem melhora clínica",
                proxima: "repetir_expansao_c"
            },
            {
                texto: "Queda do Hct e melhora dos sinais vitais, PA e diurese",
                proxima: "manutencao_c"
            }
        ]
    },

    repetir_expansao_c: {
        titulo: "Repetir expansão - Grupo C",
        descricao: `
            Repetir a fase anterior até 3 vezes, sempre vigiando sinais de congestão.

            Após a expansão, realizar avaliação horária:
            PA, SSVV e Hct a cada 2 horas.
        `,
        opcoes: [
            {
                texto: "Diurese > 1 ml/kg/h, parâmetros estáveis e queda do Hct",
                proxima: "manutencao_c"
            },
            {
                texto: "Sem melhora",
                proxima: "conduzir_grupo_d"
            }
        ]
    },

    manutencao_c: {
        titulo: "Manutenção - Grupo C",
        descricao: `
            1ª fase em 6h:
            SF 0,9% - 25 ml/kg.

            2ª fase nas 8h seguintes:
            SF 0,9% - 25 ml/kg.

            Adicionar K se necessário.
            Controle Hct ao final de cada fase.

            Nessa fase, bolus adicionais de SF 0,9% podem ser necessários.
        `,
        opcoes: [
            {
                texto: "Finalizar conduta",
                proxima: null
            }
        ]
    },

    conduzir_grupo_d: {
        titulo: "Conduzir como Grupo D",
        descricao: `
            Caso não haja melhora após as expansões do Grupo C,
            conduzir o paciente conforme o fluxo do Grupo D.
        `,
        opcoes: [
            {
                texto: "Ir para Grupo D",
                proxima: "grupo_d"
            }
        ]
    },

    grupo_d: {
        titulo: "Dengue Grupo D",
        descricao: `
            Paciente com sinais de gravidade.

            Sinais de gravidade:
            extravasamento grave de plasma com sinais de choque,
            acúmulo líquido com insuficiência respiratória,
            sangramento grave ou comprometimento grave de órgãos.
        `,
        opcoes: [
            {
                texto: "Solicitar exames e iniciar expansão",
                proxima: "exames_grupo_d"
            }
        ]
    },

    exames_grupo_d: {
        titulo: "Exames - Grupo D",
        descricao: `
            Solicitar:
            hemograma, hemocultura, PCR, albumina, ionograma, AST, ALT,
            ureia, creatinina, coagulograma, gasometria e troponina.

            Avaliar necessidade de investigar miocardite.
            Considerar RX de tórax, US abdominal e ecocardiograma.
        `,
        opcoes: [
            {
                texto: "Iniciar expansão rápida",
                proxima: "expansao_grupo_d"
            }
        ]
    },

    expansao_grupo_d: {
        titulo: "Expansão - Grupo D",
        descricao: `
            SF 0,9% - 20 ml/kg em 20 minutos.

            Reavaliar clinicamente.
            Essa fase pode ser administrada até 3 vezes, totalizando 60 ml/kg,
            caso necessário e na ausência de sinais de congestão.

            Coletar Hct após avaliação clínica.
        `,
        opcoes: [
            {
                texto: "Melhora clínica e queda do Hct",
                proxima: "melhora_d"
            },
            {
                texto: "Persiste choque",
                proxima: "choque_persistente"
            },
            {
                texto: "Hct em elevação",
                proxima: "hct_elevacao"
            },
            {
                texto: "Hct em queda",
                proxima: "hct_queda"
            }
        ]
    },

    melhora_d: {
        titulo: "Melhora clínica - Grupo D",
        descricao: `
            Se houver melhora clínica e queda do hematócrito,
            conduzir o paciente conforme o Grupo C.
        `,
        opcoes: [
            {
                texto: "Conduzir como Grupo C",
                proxima: "manutencao_c"
            }
        ]
    },

    choque_persistente: {
        titulo: "Choque persistente",
        descricao: `
            Considerar reposição com albumina.

            Albumina 5%:
            0,5 a 1 g/kg.

            Albumina 20%:
            considerar volume conforme prescrição médica.

            Na falta, considerar coloide sintético conforme protocolo institucional.
        `,
        opcoes: [
            {
                texto: "Persistência do choque",
                proxima: "dva"
            }
        ]
    },

    dva: {
        titulo: "Iniciar droga vasoativa",
        descricao: `
            Iniciar DVA conforme avaliação médica.

            Dobutamina:
            5 a 20 mcg/kg/min.

            Se persistir hipotenso:
            associar noradrenalina 0,05 a 3 mcg/kg/min.

            Sempre iniciar com a menor dose.
        `,
        opcoes: [
            {
                texto: "Finalizar conduta",
                proxima: null
            }
        ]
    },

    hct_elevacao: {
        titulo: "Hct em elevação",
        descricao: `
            Hematócrito em elevação sugere manutenção do extravasamento plasmático.

            Reavaliar necessidade de nova expansão e acompanhar sinais de choque,
            congestão e resposta clínica.
        `,
        opcoes: [
            {
                texto: "Retornar para reavaliação da expansão",
                proxima: "expansao_grupo_d"
            }
        ]
    },

    hct_queda: {
        titulo: "Hct em queda",
        descricao: `
            Hematócrito em queda exige investigação de hemorragia e coagulopatia.

            Avaliar plaquetas, sangramento ativo e distúrbios de coagulação.
        `,
        opcoes: [
            {
                texto: "Plaquetopenia",
                proxima: "plaquetopenia"
            },
            {
                texto: "Coagulopatia",
                proxima: "coagulopatia"
            }
        ]
    },

    plaquetopenia: {
        titulo: "Plaquetopenia",
        descricao: `
            Considerar transfusão conforme indicação clínica.

            Atenção para hemorragia persistente não controlada após correção
            da coagulopatia e do choque com trombocitopenia.
        `,
        opcoes: [
            {
                texto: "Finalizar conduta",
                proxima: null
            }
        ]
    },

    coagulopatia: {
        titulo: "Coagulopatia",
        descricao: `
            Corrigir conforme indicação clínica.

            Possíveis condutas:
            vitamina K, crioprecipitado ou plasma, conforme avaliação médica
            e protocolo institucional.
        `,
        opcoes: [
            {
                texto: "Finalizar conduta",
                proxima: null
            }
        ]
    }
};

let historicoFluxo = [
    {
        chave: "inicio",
        tempo: 0,
        concluido: false,
        escolha: null
    }
];

let etapaAtiva = null;
let timerAtual = null;
let fluxoFinalizado = false;

function formatarTempo(segundos) {
    const minutos = String(Math.floor(segundos / 60)).padStart(2, "0");
    const seg = String(segundos % 60).padStart(2, "0");

    return `${minutos}:${seg}`;
}

function obterEtapaAtual() {
    if (historicoFluxo.length === 0) {
        return null;
    }

    return historicoFluxo[historicoFluxo.length - 1];
}

function iniciarTimerEtapa(indice) {
    const etapa = historicoFluxo[indice];

    if (!etapa || etapa.concluido || fluxoFinalizado) {
        return;
    }

    if (etapaAtiva !== null && etapaAtiva !== indice) {
        pararTimerAtual();
    }

    etapaAtiva = indice;

    if (timerAtual !== null) {
        return;
    }

    timerAtual = setInterval(() => {
        historicoFluxo[indice].tempo++;

        const elemento = document.getElementById(`timer-etapa-${indice}`);

        if (elemento) {
            elemento.textContent = formatarTempo(historicoFluxo[indice].tempo);
        }
    }, 1000);

    renderizarFluxograma();
}

function pararTimerAtual() {
    if (timerAtual !== null) {
        clearInterval(timerAtual);
        timerAtual = null;
    }

    etapaAtiva = null;
}

function concluirEtapa(indice) {
    const etapa = historicoFluxo[indice];

    if (!etapa || etapa.concluido || fluxoFinalizado) {
        return;
    }

    etapa.concluido = true;

    if (etapaAtiva === indice) {
        pararTimerAtual();
    }

    atualizarProgresso();
    renderizarFluxograma();
}

function selecionarOpcao(indice, proxima, textoOpcao) {
    const etapa = historicoFluxo[indice];

    if (!etapa || fluxoFinalizado) {
        return;
    }

    if (!etapa.concluido) {
        alert("Conclua a etapa atual antes de seguir para a próxima decisão.");
        return;
    }

    etapa.escolha = textoOpcao;

    if (proxima === null) {
        fluxoFinalizado = true;
        pararTimerAtual();
        atualizarProgresso();
        renderizarFluxograma();
        return;
    }

    historicoFluxo.push({
        chave: proxima,
        tempo: 0,
        concluido: false,
        escolha: null
    });

    atualizarProgresso();
    renderizarFluxograma();
}

function voltarEtapa(indice) {
    if (indice < 0 || indice >= historicoFluxo.length) {
        return;
    }

    pararTimerAtual();

    historicoFluxo = historicoFluxo.slice(0, indice + 1);

    const etapa = historicoFluxo[indice];

    etapa.concluido = false;
    etapa.escolha = null;

    fluxoFinalizado = false;

    atualizarProgresso();
    renderizarFluxograma();
}

function atualizarProgresso() {
    const concluidas = historicoFluxo.filter(etapa => etapa.concluido).length;
    const total = historicoFluxo.length;

    const texto = document.getElementById("texto-progresso");

    if (texto) {
        texto.textContent = `${concluidas} / ${total} etapas concluídas`;
    }
}

function renderizarFluxograma() {
    const lista = document.getElementById("lista-fluxograma");

    if (!lista) {
        return;
    }

    lista.innerHTML = "";

    historicoFluxo.forEach((item, indice) => {
        const dados = fluxoDengue[item.chave];

        if (!dados) {
            return;
        }

        if (indice > 0) {
            const seta = document.createElement("div");
            seta.className = "fluxo-seta";
            seta.textContent = "↓";
            lista.appendChild(seta);
        }

        const wrap = document.createElement("div");

        let classes = "card-fluxo-wrap";

        if (item.concluido) {
            classes += " concluido";
        }

        if (etapaAtiva === indice) {
            classes += " ativa";
        }

        wrap.className = classes;
        wrap.setAttribute("role", "button");
        wrap.setAttribute("tabindex", "0");

        wrap.innerHTML = `
            <div class="card-fluxo-interno">

                <div class="fluxo-card-topo">
                    <span class="fluxo-etapa-titulo">
                        ${dados.titulo}
                    </span>

                    <span class="timer-etapa">
                        <img
                            src="/static/protocolos/icons/Timer.svg"
                            alt="Tempo"
                            class="icone-timer"
                        >

                        <span id="timer-etapa-${indice}">
                            ${formatarTempo(item.tempo)}
                        </span>
                    </span>
                </div>

                <p class="fluxo-descricao">
                    ${dados.descricao}
                </p>

                ${
                    item.escolha
                    ? `
                        <div class="fluxo-escolha">
                            Escolha realizada: ${item.escolha}
                        </div>
                    `
                    : ""
                }

                <div class="fluxo-card-rodape">
                    ${
                        item.concluido
                        ? `
                            <button
                                type="button"
                                class="btn-concluir-etapa"
                                disabled
                            >
                                ✓ Concluída
                            </button>
                        `
                        : `
                            <button
                                type="button"
                                class="btn-concluir-etapa"
                                onclick="event.stopPropagation(); concluirEtapa(${indice})"
                            >
                                ✓ Concluir
                            </button>
                        `
                    }
                </div>

                ${
                    item.concluido && !item.escolha && !fluxoFinalizado
                    ? `
                        <div class="fluxo-opcoes">
                            ${dados.opcoes.map(opcao => `
                                <button
                                    type="button"
                                    class="btn-opcao-fluxo"
                                    onclick="event.stopPropagation(); selecionarOpcao(${indice}, ${opcao.proxima === null ? "null" : `'${opcao.proxima}'`}, '${opcao.texto.replace(/'/g, "\\'")}')"
                                >
                                    ${opcao.texto}
                                </button>
                            `).join("")}
                        </div>
                    `
                    : ""
                }

                ${
                    indice < historicoFluxo.length - 1
                    ? `
                        <button
                            type="button"
                            class="btn-voltar-etapa"
                            onclick="event.stopPropagation(); voltarEtapa(${indice})"
                        >
                            Voltar para esta etapa
                        </button>
                    `
                    : ""
                }

            </div>
        `;

        wrap.addEventListener("click", () => {
            iniciarTimerEtapa(indice);
        });

        wrap.addEventListener("keydown", event => {
            if (event.key === " " || event.key === "Enter") {
                event.preventDefault();
                iniciarTimerEtapa(indice);
            }
        });

        lista.appendChild(wrap);
    });

    if (fluxoFinalizado) {
        const fim = document.createElement("div");

        fim.className = "fluxo-finalizado";

        fim.innerHTML = `
            <strong>Fluxograma finalizado.</strong>
            <span>Conduta registrada conforme caminho selecionado.</span>
        `;

        lista.appendChild(fim);
    }
}

function resetarFluxograma() {
    pararTimerAtual();

    historicoFluxo = [
        {
            chave: "inicio",
            tempo: 0,
            concluido: false,
            escolha: null
        }
    ];

    fluxoFinalizado = false;

    atualizarProgresso();
    renderizarFluxograma();
}

function mudarAba(aba) {
    document.querySelectorAll(".tab-content").forEach(elemento => {
        elemento.classList.remove("ativo");
    });

    const conteudo = document.getElementById("conteudo-" + aba);

    if (conteudo) {
        conteudo.classList.add("ativo");
    }

    document.querySelectorAll(".tab").forEach(elemento => {
        elemento.classList.remove("ativo");
    });

    const tab = document.getElementById("tab-" + aba);

    if (tab) {
        tab.classList.add("ativo");
    }
}

renderizarFluxograma();
atualizarProgresso();
mudarAba("fluxograma");