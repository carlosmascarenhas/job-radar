
import os
from dotenv import load_dotenv

load_dotenv()

# Cargo forte: título que já é inequivocamente de BACKEND, sem precisar de
# qualificador junto. Perfil = Backend sênior com FOCO em PHP/Laravel.
# NÃO inclui "Desenvolvedor" sozinho de propósito (casava toda vaga de dev,
# inclusive React Native/frontend) nem títulos de frontend/mobile/fullstack
# — o foco é backend. Também sem outras linguagens (Node/Java/Python): pra
# ligar alguma, é só adicionar aqui.
KEYWORDS_CARGO_FORTE = [
    # --- Backend genérico (não cita a linguagem no título) ---
    "Desenvolvedor Backend",
    "Desenvolvedora Backend",
    "Desenvolvedor Back-end",
    "Desenvolvedora Back-end",
    "Backend Developer",
    "Back-end Developer",
    "Backend Engineer",
    "Back-end Engineer",
    "Engenheiro Backend",
    "Engenheira Backend",
    "Software Engineer",
    "Engenheiro de Software",
    "Engenheira de Software",
    # --- PHP / Laravel (foco) ---
    "Desenvolvedor PHP",
    "Desenvolvedora PHP",
    "PHP Developer",
    "Programador PHP",
    "Programadora PHP",
    "Desenvolvedor Laravel",
    "Desenvolvedora Laravel",
    "Laravel Developer",
    "Programador Laravel",
]

# Cargo ambíguo: título que também é usado fora de software (ex:
# "Engenheiro" existe em civil/mecânica/produção; "Analista de Sistemas/TI"
# pode ser suporte/infra). Só conta como match se o título TAMBÉM tiver um
# QUALIFICADORES_DADOS junto (uma stack/termo de software) — é o que permite
# pegar cargo adjacente sem cada um virar fonte de ruído sozinho.
KEYWORDS_CARGO_AMBIGUO = [
    "Engenheiro",
    "Engineer",
    "Analista de Sistemas",
    "Analista de TI",
    "Analista Desenvolvedor",
]

# Termo de software que precisa aparecer junto no título quando o cargo é
# ambíguo, pra confirmar que é vaga de desenvolvimento e não de outra área.
# (Nome da variável mantido por ser importado em vários módulos; o conteúdo
# agora é "vocabulário de software", não de dados.)
QUALIFICADORES_DADOS = [
    "software",
    "backend",
    "back-end",
    "back end",
    "desenvolvimento",
    "api",
    "php",
    "laravel",
]

# Stack que aparece como núcleo do título ("Especialista Laravel", "Node
# Engineer"). Só conta como match se o título TAMBÉM tiver uma palavra de
# cargo (QUALIFICADORES_CARGO) — espelho da regra de KEYWORDS_CARGO_AMBIGUO:
# lá o cargo é ambíguo e pede stack, aqui a stack é ambígua e pede cargo.
# Sem isso, "React" sozinho aprovaria "Recrutador React" ou "React Native
# Designer".
FERRAMENTAS_TITULO = [
    "Laravel",
    "PHP",
]

# Palavra de cargo que confirma que a vaga da stack é de desenvolvimento.
# Aqui é o INVERSO do perfil original de dados: "desenvolvedor"/"engenheiro"/
# "developer"/"programador" entram de propósito — são o alvo agora.
QUALIFICADORES_CARGO = [
    "desenvolvedor",
    "desenvolvedora",
    "developer",
    "engenheiro",
    "engenheira",
    "engineer",
    "programador",
    "programadora",
    "dev",
    # "especialista"/"specialist" só entram em jogo junto de uma stack de
    # FERRAMENTAS_TITULO (ex: "Especialista Node.js"), que já é dev — então
    # não abrem porta pra vaga de outra área.
    "especialista",
    "specialist",
]

KEYWORDS = KEYWORDS_CARGO_FORTE + KEYWORDS_CARGO_AMBIGUO

# Termos de busca enviados a cada site. Ficam separados das KEYWORDS de
# propósito: TERMOS_BUSCA é a rede ampla (o que é pesquisado em cada site,
# incluindo termos de ferramenta/stack pra achar vaga com título atípico),
# enquanto KEYWORDS é o filtro final e só olha o título da vaga já
# encontrada. Um termo de ferramenta (ex: "dax") só resulta em notificação
# se o TÍTULO da vaga também bater com uma keyword de cargo — isso evita
# falso positivo de vaga que só cita a ferramenta como diferencial.
#
# TERMOS_CARGO é derivado direto de KEYWORDS (em vez de mantido à mão em
# lista separada) — antes as duas listas divergiam: metade das KEYWORDS
# (ex: "Desenvolvedor BI", "BI Analyst", "Analista de Negócios") nunca era
# buscada de verdade, só existia como filtro, então só pegava essas vagas
# por sorte via outro termo. Com a derivação automática isso não pode mais
# acontecer — toda keyword nova em KEYWORDS já vira busca também.
TERMOS_CARGO_EXTRA = [
    # termos mais amplos que a keyword exata, mantidos por dar rede mais
    # larga na busca (a keyword em si é mais restrita, de propósito, pra
    # não gerar falso positivo no filtro de título).
    "desenvolvedor backend",
    "desenvolvedor back-end",
    "backend",
    "desenvolvedor php",
    "desenvolvedor laravel",
    "programador php",
]

TERMOS_CARGO = sorted(set(k.lower() for k in KEYWORDS) | set(TERMOS_CARGO_EXTRA))

# Stacks buscadas nos sites (rede ampla). A vaga só vira notificação se o
# TÍTULO também bater no filtro de cargo — então buscar por "laravel" não
# notifica toda vaga que cita Laravel, só as que têm cargo de dev no título.
# Foco total em PHP/Laravel (sem Node/TS/React de propósito).
TERMOS_FERRAMENTA = [
    "php",
    "laravel",
]

TERMOS_BUSCA = TERMOS_CARGO + TERMOS_FERRAMENTA

# Medido: os TERMOS_BUSCA inteiros (hoje 42) rodando em TODO ciclo é o que
# gera as centenas de sessões de navegador por execução — o custo cresce
# linear com o tamanho da lista, e a lista só cresce (mais ainda com a
# expansão internacional puxando mais termos no radar). TERMOS_POR_CICLO é
# o tamanho do BLOCO usado por ciclo, não o total de termos — main.py roda
# um bloco por vez em rodízio (ver _proximo_bloco_termos) e avança pro
# próximo bloco no ciclo seguinte, salvando a posição no jobs.db. Isso
# desacopla custo por ciclo de tamanho da lista: dobrar TERMOS_BUSCA dobra
# quantos ciclos até cobrir tudo de novo, não o custo de cada ciclo.
TERMOS_POR_CICLO = 10

# Perfil do Carlos: só vaga REMOTA. Com a lista contendo apenas "Remoto",
# o filtro (job.py:combina_com) só aprova vaga com modalidade=Remoto — o
# ramo de cidade presencial fica vazio de propósito. Pra aceitar também
# presencial/híbrido numa cidade (ex: "Campo Grande"), basta adicionar o
# nome aqui.
CIDADES = [
    "Remoto",
]

# MEDIDO: "Data Analyst @ Lisboa" e "Analista de Datos @ Madrid" reprovavam
# na localização, não no cargo — CIDADES acima é whitelist só de cidade
# brasileira, e a expansão de LOCATIONS_LINKEDIN pra Argentina/Chile (ver
# abaixo) passou a trazer vaga presencial/híbrida em Portugal/Espanha de
# vez em quando junto. Lista SEPARADA (não misturada em CIDADES, que
# continua só-Brasil de propósito — ver decisão registrada na criação do
# config_intl.py) com toggle próprio, pra dar pra ligar/desligar esse eixo
# sem mexer no resto do filtro. Canônica aqui porque config_intl.py já
# importa de config.py (não o contrário) — o pipeline internacional reusa
# essa mesma lista em vez de manter uma cópia (risco de divergir, mesmo
# motivo da unificação de _contem_termo/_tem_termo).
CIDADES_EUROPA_IBERICA = [
    "Portugal",
    "Lisboa",
    "Porto",
    "Braga",
    "Espanha",
    "España",
    "Spain",
    "Madrid",
    "Barcelona",
    "Valencia",
]

# Toggle independente do ATIVAR_EIXO_IBERICO de config_intl.py — são dois
# eixos diferentes (esse aqui é do pipeline BR/main.py, aquele é do
# pipeline internacional/main_intl.py), cada um com seu próprio liga/
# desliga, mesmo compartilhando a mesma lista de cidades acima.
#
# DESLIGADO: do mercado internacional, só interessa vaga remota — vaga
# presencial/híbrida em Lisboa/Madrid (o que esse eixo notifica, marcada
# "exploratória") não é o que o usuário quer. CIDADES_EUROPA_IBERICA
# continua definida (não precisa apagar) pra caso o eixo volte a ser
# ligado depois — só o toggle muda.
ATIVAR_EIXO_IBERICO_BR = False

# LinkedInScraper é a única fonte do pipeline BR que também alcança vaga
# fora do Brasil (as outras são portais brasileiros) — mas até aqui rodava
# só com location=Brasil fixo no código (scrapers/linkedin.py:88), então
# essa "porta pra fora" nunca era usada.
#
# Mercado "casa": busca modalidade completa (presencial/híbrida + remoto),
# porque o usuário mora aqui e vaga local de verdade interessa.
LOCATIONS_LINKEDIN = ["Brasil"]

# Mercados adicionais de busca no LinkedIn. VAZIO no perfil do Carlos: ele
# só quer vaga remota do mercado brasileiro, então não faz sentido gastar
# ciclo buscando em outros países (o filtro de mercado abaixo derrubaria
# quase tudo mesmo). O scraper simplesmente pula a lista vazia. Pra reativar
# busca noutros mercados, colocar os países aqui (usar grafia já testada no
# endpoint, ex: "Argentina", "Portugal").
LOCATIONS_LINKEDIN_REMOTO_APENAS = []

# Mercado que a vaga remota precisa aceitar pra contar, quando o texto de
# local DECLARA um escopo geográfico ("Remote — US only", "Remote — India").
# Ver Job.escopo_remoto/RegrasFiltro.mercados_remoto_aceitos em job.py — sem
# isso, uma vaga remota só pra outro país passava igual a uma remota de
# verdade pro Brasil. Vaga remota SEM escopo declarado no texto (a grande
# maioria) continua batendo normalmente, isso só filtra quando a fonte
# EXPLICITA um mercado incompatível.
#
# MEDIDO: Argentina/Chile/México/Colômbia ENTRAM nominalmente agora — a
# suposição de que "LATAM" cobria os quatro como guarda-chuva só valia
# enquanto extrair_escopo_remoto resolvia o texto pra "LATAM" literal.
# Depois que passou a reconhecer cidade (Buenos Aires/Santiago/Cidade do
# México/Bogotá — ver _CIDADES_MERCADO em job.py), o escopo passou a
# resolver pro PAÍS específico, não mais pro guarda-chuva — e o país
# específico nunca esteve nessa lista. Resultado: LOCATIONS_LINKEDIN_
# REMOTO_APENAS pagava o custo de buscar nesses 4 países e o filtro
# descartava tudo que a busca trazia de lá. "LATAM" continua na lista pra
# quando o texto disser isso literalmente (guarda-chuva de verdade, não
# substituto de nome de país). Portugal e Espanha entraram nominalmente
# pelo mesmo motivo, desde antes.
MERCADOS_REMOTO_ACEITOS = ["Brasil", "LATAM"]

INTERVALO_MINUTOS = int(os.getenv("INTERVALO_MINUTOS", 180))

# Digest ranqueado (item 08): vaga com Job.pontuar_relevancia() >= este
# limiar notifica na hora (como sempre foi); abaixo disso, fica na fila do
# digest diário — ver _enviar_digest_diario em main.py.
#
# MEDIDO: rodei o score contra as ~305 vagas do jobs.db real que ainda
# batem as regras atuais. Distribuição: score 4 (2%), 5 (24%), 6 (67%),
# 7 (5%), 8 (2%) — nada em 9-10 na amostra (exige acertar praticamente
# todo sinal ao mesmo tempo: cargo forte + ferramenta + senioridade alvo +
# mercado confirmado). Limiar 7 deixa ~7% imediata e ~93% no digest — bate
# com o pedido ("vaga de score alto na hora, resto agrupado"); 6 deixava
# 74% imediata (pouca redução de ruído); 8 deixava só 2% (digest com
# praticamente tudo, quase nenhuma vaga "excelente" se destacando na hora).
LIMIAR_DIGEST_IMEDIATO = 7

# Hora UTC em que o digest diário dispara (uma vez por perfil, por dia —
# ver _enviar_digest_diario). 0 = meia-noite UTC = 21h em Brasília (UTC-3).
# O cron do workflow (0 */3 * * *) já passa por essa hora exata todo dia,
# então não precisa de agendamento à parte.
DIGEST_HORA_UTC = 0

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "jobs.db")