const fluxoDengue = {
    inicio: {
        titulo: "Classificação inicial",
        descricao: `
            Selecione o grupo do paciente conforme os sinais apresentados.
        `,
        opcoes: [
            {
                texto: "Grupo C — com sinais de alerta, sem sinais de gravidade",
                proxima: "grupo_c"
            },
            {
                texto: "Grupo D — com sinais de gravidade",
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
        titulo: "Exames — Grupo C",
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
        titulo: "Expansão — Grupo C",
        descricao: `
            SF 0,9% — 10 ml/kg em 1h.
 
            Reavaliar: se sem congestão, repetir SF 0,9% — 10 ml/kg em 1h.
 
            Solicitar Hct/Hg em até 2h da expansão.
        `,
        opcoes: [
            {
                texto: "Sem queda do Hct OU sem melhora dos SSVV, PA e diurese (<1 ml/kg/h)",
                proxima: "repetir_expansao_c"
            },
            {
                texto: "Queda do Hct E melhora dos SSVV, PA e diurese (>1 ml/kg/h)",
                proxima: "manutencao_c"
            }
        ]
    },
 
    repetir_expansao_c: {
        titulo: "Repetir expansão — Grupo C",
        descricao: `
            Repetir a fase anterior até 3 vezes se necessário (+30 ml/kg total),
            sempre vigiando sinais de congestão.
 
            Avaliação horária: DU, PA e SSVV e Hct a cada 2h.
        `,
        opcoes: [
            {
                texto: "DU >1 ml/kg/h, parâmetros estáveis e queda do Hct",
                proxima: "manutencao_c"
            },
            {
                texto: "Sem melhora",
                proxima: "conduzir_grupo_d"
            }
        ]
    },
 
    manutencao_c: {
        titulo: "Manutenção — Grupo C",
        descricao: `
            1ª fase em 6h:
            SF 0,9% — 25 ml/kg (4 ml/kg/h).
 
            Se melhora e Hct estável ou em queda:
            2ª fase nas 8h seguintes:
            SF 0,9% — 25 ml/kg (3 ml/kg/h).
 
            Obs.:
            1. Adicionar K se necessário.
            2. Controle Hct ao término de cada fase.
            3. Nessa fase, bolus adicionais de SF 0,9% (10 ml/kg) podem ser necessários.
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
            Sem melhora após as expansões do Grupo C.
            Conduzir o paciente conforme o fluxo do Grupo D,
            a partir do item "persiste choque".
        `,
        opcoes: [
            {
                texto: "Ir para Grupo D — persiste choque",
                proxima: "choque_persistente"
            }
        ]
    },
 
    grupo_d: {
        titulo: "Dengue Grupo D",
        descricao: `
            Paciente com sinais de gravidade.
 
            Sinais de gravidade:
            extravasamento grave de plasma com sinais de choque,
            acúmulo de líquido com insuficiência respiratória aguda,
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
        titulo: "Exames — Grupo D",
        descricao: `
            Solicitar:
            hemograma, hemocultura, PCR, albumina, ionograma, AST, ALT,
            ureia, creatinina, coagulograma, gasometria e troponina (na suspeita de miocardite).
 
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
        titulo: "Expansão — Grupo D",
        descricao: `
            SF 0,9% — 20 ml/kg em 20 min, seguida de avaliação clínica.
 
            Essa fase pode ser administrada até 3 vezes (60 ml/kg total),
            caso necessário e na ausência de sinais de congestão.
 
            Coletar Hct após as expansões.
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
        titulo: "Melhora clínica — Grupo D",
        descricao: `
            Se houver melhora clínica e queda do hematócrito,
            conduzir o paciente conforme o Grupo C.
        `,
        opcoes: [
            {
                texto: "Conduzir como Grupo C — manutenção",
                proxima: "manutencao_c"
            }
        ]
    },
 
    choque_persistente: {
        titulo: "Choque persistente — albumina",
        descricao: `
            Albumina 5% (0,5–1 g/kg):
            5% = 25 ml de albumina 20% + 75 ml de SF 0,9%.
            Volume: 10–20 ml/kg da albumina 5%.
 
            Na falta: coloide sintético — 10 ml/kg conforme protocolo institucional.
        `,
        opcoes: [
            {
                texto: "Persiste choque após albumina",
                proxima: "dva"
            }
        ]
    },
 
    dva: {
        titulo: "Droga vasoativa (DVA)",
        descricao: `
            Dobutamina (30–40% do Grupo D pode cursar com miocardite):
            5–10 mcg/kg/min  ou  adrenalina 0,05–0,3 mcg/kg/min.
 
            Persiste hipotenso: associar noradrenalina 0,05–1 mcg/kg/min.
 
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
 
            Reavaliar necessidade de nova expansão e acompanhar
            sinais de choque, congestão e resposta clínica.
        `,
        opcoes: [
            {
                texto: "Retornar para reavaliação da expansão",
                proxima: "expansao_grupo_d"
            }
        ]
    },
 
    hct_queda: {
        titulo: "Hct em queda — investigar hemorragia e coagulopatia",
        descricao: `
            Queda do Hct exige investigação de hemorragia e coagulopatia.
 
            Avaliar plaquetas, sangramento ativo e distúrbios de coagulação.
        `,
        opcoes: [
            {
                texto: "Hemorragia ativa",
                proxima: "hemorragia"
            },
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
 
    hemorragia: {
        titulo: "Hemorragia ativa",
        descricao: `
            Concentrado de hemácias (CH): 10 ml/kg.
 
            Corrigir coagulopatia associada conforme indicação clínica.
        `,
        opcoes: [
            {
                texto: "Finalizar conduta",
                proxima: null
            }
        ]
    },
 
    plaquetopenia: {
        titulo: "Plaquetopenia",
        descricao: `
            Transfusão (1U/5–10 kg): APENAS se hemorragia persistente não controlada,
            após correção da coagulopatia e do choque,
            com trombocitopenia e INR >1,5× VN.
 
            Não há indicação de transfusão profilática de plaquetas.
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
            Corrigir conforme indicação clínica:
 
            Vitamina K: 5 ou 10 mg.
            Crioprecipitado: 1U/5–10 kg.
            Plasma: 10 ml/kg.
        `,
        opcoes: [
            {
                texto: "Finalizar conduta",
                proxima: null
            }
        ]
    }
};

const fluxoSedacao = {
    inicio: {
        titulo: "Conversão de sedativos/analgésicos — UTIP",
        descricao: `
            Selecione a droga atualmente em uso contínuo para iniciar a conversão.
        `,
        opcoes: [
            {
                texto: "Midazolam contínuo",
                proxima: "midazolam_para_diazepam"
            },
            {
                texto: "Morfina contínua → Morfina enteral",
                proxima: "morfina_para_morfina_enteral"
            },
            {
                texto: "Morfina contínua → Metadona oral",
                proxima: "morfina_para_metadona"
            },
            {
                texto: "Fentanil contínuo → Morfina enteral",
                proxima: "fentanil_para_morfina_enteral"
            },
            {
                texto: "Fentanil contínuo → Morfina contínua (×5)",
                proxima: "fentanil_para_morfina_continua"
            },
            {
                texto: "Clonidina contínua",
                proxima: "clonidina_continua_para_enteral"
            },
            {
                texto: "Dexmedetomidina",
                proxima: "dexmedetomidina_para_clonidina"
            },
            {
                texto: "Lorazepam",
                proxima: "lorazepam_para_diazepam"
            }
        ]
    },
 
    midazolam_para_diazepam: {
        titulo: "Midazolam contínuo → Diazepam enteral",
        descricao: `
            Equivalência:
            1 mg de midazolam IV = 2,5–5 mg de diazepam VO.
 
            Cálculo da dose de diazepam/24h:
            DZP/24h = dose MDZ (mcg/kg/min) × peso × 0,6
 
            Exemplo:
            Paciente de 10 kg em uso de 2,5 mcg/kg/min:
            10 × 2,5 × 0,6 = 15 mg/dia.
 
            Fracionar 6/6h (dose máxima por tomada: 10 mg).
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    },
 
    morfina_para_morfina_enteral: {
        titulo: "Morfina contínua → Morfina enteral",
        descricao: `
            Equivalência:
            10 mg de morfina IV = 30 mg de morfina VO (referência: UpToDate).
 
            Cálculo da dose enteral/24h:
            Dose enteral/24h = dose morfina contínua (mcg/kg/h) × peso × 0,072
 
            Exemplo:
            Paciente de 15 kg em uso de 12 mcg/kg/h:
            15 × 12 × 0,072 = 13 mg/dia.
 
            Iniciar fracionando 4/4h.
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    },
 
    morfina_para_metadona: {
        titulo: "Morfina contínua → Metadona oral",
        descricao: `
            Equivalências:
            10 mg de morfina SC/IV = 20 mg de metadona VO.
            10 mg de morfina VO = 6,7 mg de metadona VO.
 
            Cálculo da dose de metadona/24h:
            Dose metadona/24h = dose morfina contínua (mcg/kg/h) × peso × 0,048
 
            Exemplo:
            Paciente de 12 kg em uso de 14 mcg/kg/h:
            12 × 14 × 0,048 = 8 mg/dia.
        `,
        opcoes: [
            {
                texto: "Calcular e iniciar desmame",
                proxima: "metadona_desmame"
            }
        ]
    },
 
    metadona_desmame: {
        titulo: "Desmame — Metadona oral",
        descricao: `
            D1: 50% da dose em metadona, sem reduzir a morfina contínua.
            D2: 100% da dose em metadona, suspender morfina contínua.
 
            Reduzir metadona 10–20% a cada 1–2 dias conforme tolerância.
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    },
 
    fentanil_para_morfina_enteral: {
        titulo: "Fentanil contínuo → Morfina enteral",
        descricao: `
            Equivalência:
            1 mcg/kg/h de fentanil = 0,05 mg/kg/dia de morfina.
 
            Cálculo da dose de morfina enteral/24h:
            Dose enteral/24h = dose fentanil (mcg/kg/h) × peso × 1,8
 
            Exemplo:
            Paciente de 10 kg em uso de 1 mcg/kg/h:
            1 × 10 × 1,8 = 18 mg/dia.
 
            Iniciar fracionando 4/4h.
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    },
 
    fentanil_para_morfina_continua: {
        titulo: "Fentanil contínuo → Morfina contínua (×5)",
        descricao: `
            Equivalência:
            Fentanil contínuo × 5 = morfina contínua equivalente.
 
            Exemplo:
            Fentanil 2 mcg/kg/h equivale a 10 mcg/kg/h de morfina contínua.
 
            Obs.: sufentanil converte para metadona;
            fentanil converte para remifentanil conforme protocolo.
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    },
 
    clonidina_continua_para_enteral: {
        titulo: "Clonidina contínua → Clonidina enteral",
        descricao: `
            Desmame do contínuo:
            Reduzir 1 mcg/kg/h a cada 12h até atingir 1 mcg/kg/h,
            mantendo essa dose por 12h.
        `,
        opcoes: [
            {
                texto: "Iniciar clonidina oral",
                proxima: "clonidina_oral_desmame"
            }
        ]
    },
 
    clonidina_oral_desmame: {
        titulo: "Clonidina oral — desmame",
        descricao: `
            Após 12h na dose de 1 mcg/kg/h:
            Iniciar clonidina oral 5 mcg/kg/dose 6/6h.
 
            Após a 1ª dose oral: suspender o contínuo.
 
            Desmame oral:
            Reduzir 1 mcg/kg/dose a cada 24h até 1 mcg/kg/dose 6/6h.
            Após: reduzir periodicidade (8/8h → 12/12h → 24/24h → suspender).
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    },
 
    dexmedetomidina_para_clonidina: {
        titulo: "Dexmedetomidina → Clonidina enteral",
        descricao: `
            Cálculo da dose de clonidina:
            5 × dose dexmedetomidina (mcg/kg/h) = dose clonidina 6/6h (mcg/kg/dose).
 
            Dose máxima enteral de clonidina: 200 mcg/dose.
 
            Exemplo:
            Uso de 0,7 mcg/kg/h de dexmedetomidina:
            5 × 0,7 = 3,5 mcg/kg/dose de clonidina 6/6h.
        `,
        opcoes: [
            {
                texto: "Iniciar clonidina e reduzir dexmedetomidina",
                proxima: "dexmedetomidina_desmame"
            }
        ]
    },
 
    dexmedetomidina_desmame: {
        titulo: "Desmame — Dexmedetomidina",
        descricao: `
            Após a 2ª dose de clonidina oral:
            Reduzir dexmedetomidina em 50%.
 
            Após a 3ª dose de clonidina oral:
            Suspender dexmedetomidina.
 
            Iniciar desmame da clonidina oral:
            Reduzir 1 mcg/kg/dose a cada 24h → reduzir periodicidade → suspender.
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    },
 
    lorazepam_para_diazepam: {
        titulo: "Lorazepam → Diazepam enteral",
        descricao: `
            Equivalência:
            1 mg de lorazepam = 2,5–10 mg de diazepam.
            Iniciar com 1 mg de LRZ = 5 mg de diazepam.
 
            Doses máximas:
            Lorazepam: 4 mg/dose.
            Diazepam: 10 mg/dose.
        `,
        opcoes: [
            {
                texto: "Finalizar conversão",
                proxima: null
            }
        ]
    }
};

const fluxoAtivo = window.location.href.includes("sedacao") ? fluxoSedacao : fluxoDengue;

let historicoFluxo = [
    {
        chave: "inicio",
        tempo: 0,
        concluido: false,
        escolha: null
    }
];

let timerAtual = null;
let fluxoFinalizado = false;
let etapaAtiva = null;

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
        pararTimerEtapa(etapaAtiva);
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
    concluirEAvancar(indice);
}

function selecionarOpcao(indice, proxima, textoOpcao) {
    const etapa = historicoFluxo[indice];

    if (!etapa || fluxoFinalizado) {
        return;
    }

    // Apenas marca a escolha — não avança ainda
    etapa.escolhaPendente = textoOpcao;
    etapa.proximaPendente = proxima;

    renderizarFluxograma();
}

function concluirEAvancar(indice) {
    const etapa = historicoFluxo[indice];

    if (!etapa || fluxoFinalizado) {
        return;
    }

    etapa.concluido = true;

    if (etapaAtiva === indice) {
        pararTimerAtual();
    }

    // Se há uma escolha pendente, agora avança
    if (etapa.escolhaPendente !== undefined) {
        etapa.escolha = etapa.escolhaPendente;
        const proxima = etapa.proximaPendente;

        delete etapa.escolhaPendente;
        delete etapa.proximaPendente;

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
    }

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
    delete etapa.escolhaPendente;
    delete etapa.proximaPendente;

    fluxoFinalizado = false;

    atualizarProgresso();
    renderizarFluxograma();
}

function atualizarProgresso() {
    const concluidas = historicoFluxo.filter(etapa => etapa.concluido).length;
    const totalEtapas = Object.keys(fluxoAtivo).length;
    const percentual = (concluidas / totalEtapas) * 100;

    const texto = document.getElementById("texto-progresso");
    if (texto) texto.textContent = `${concluidas} / ${totalEtapas}`;
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

function renderizarFluxograma() {
    const lista = document.getElementById("lista-fluxograma");

    if (!lista) {
        return;
    }

    lista.innerHTML = "";

    historicoFluxo.forEach((item, indice) => {
        const dados = fluxoAtivo[item.chave];

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

                ${
                    !item.concluido && !item.escolha && !fluxoFinalizado
                    ? `
                        <div class="fluxo-opcoes">
                            ${dados.opcoes.map(opcao => `
                                <button
                                    type="button"
                                    class="btn-opcao-fluxo${item.escolhaPendente === opcao.texto ? ' selecionada' : ''}"
                                    onclick="event.stopPropagation(); selecionarOpcao(${indice}, ${opcao.proxima === null ? "null" : `'${opcao.proxima}'`}, '${opcao.texto.replace(/'/g, "\\'")}')"
                                >
                                    ${opcao.texto}
                                </button>
                            `).join("")}
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
                                ${dados.opcoes.length > 0 && !item.escolhaPendente ? 'disabled title="Selecione uma opção antes de concluir"' : ''}
                                onclick="event.stopPropagation(); concluirEtapa(${indice})"
                            >
                                ✓ Concluir
                            </button>
                        `
                    }
                </div>

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

    // Footer de progresso
    const concluidas = historicoFluxo.filter(e => e.concluido).length;
    const totalEtapas = Object.keys(fluxoAtivo).length;

    const footer = document.createElement("div");
    footer.className = "fluxograma-footer";
    footer.innerHTML = `
        <div class="card-fluxo-wrap progresso-wrap">
            ${fluxoFinalizado ? `<button class="btn-protocolo-concluido" style="display:flex;" onclick="window.location.href = typeof URL_PROTOCOLOS !== 'undefined' ? URL_PROTOCOLOS : '/'">✔ Protocolo concluído</button>` : ""}
            <button class="btn-reiniciar-protocolo" onclick="resetarFluxograma()">↺ Reiniciar protocolo</button>
        </div>
    `;

    lista.appendChild(footer);
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


mudarAba("fluxograma");
renderizarFluxograma();
atualizarProgresso();