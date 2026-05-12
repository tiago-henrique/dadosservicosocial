# =========================
# Demandas resolvidas
# =========================

finalizados_map = {
    1: "Sim",
    0: "Não"
}

admissao_clean['demanda_resolvida'] = admissao_clean[
    'demanda_resolvida'
].replace(finalizados_map)

finalizados = admissao_clean[
    'demanda_resolvida'
].value_counts()

st.subheader("Demandas resolvidas")

st.dataframe(finalizados)

# =========================
# Assistentes sociais
# =========================

assistentes_map = {
    1: "Ana Carolina Pereira dos Santos",
    2: "Ana Lúcia Barbosa Santos Silva",
    3: "Ana Maria R. Cuzziol",
    4: "Adriana Ferreira Guilherme Simentoni",
    5: "Adriana Mara Benatti",
    6: "Aline Aparecida Ernesto Oliveira",
    7: "Bruna Lopes dos Santos Lemos",
    8: "Camila de Oliveira",
    9: "Camila Meza dos Santos",
    10: "Caroline Bauermann",
    11: "Carla C. Santos",
    12: "Daniela Cristina Covre Santos",
    13: "Daniele Lúcia C. Santos",
    14: "Débora José Caceano",
    15: "Deise de Jesus Carvalho",
    16: "Elisangela F. Dias",
    17: "Ederson Ferreira Camargo",
    18: "Edilucia Pereira",
    19: "Erica A. Bertacini",
    20: "Francine de Lima Taino Viegas",
    21: "Gabriela de Araújo Coimbra",
    22: "Graziani Gonçalves Ribeiro",
    23: "Hilda Manoela de Lima",
    24: "Ivã Ap. J. Pereira",
    25: "Jaqueline dos Reis",
    26: "Juliana Yuri Kawata",
    27: "Laís Yonezawa Leão",
    28: "Lilian Andreia C. Dias",
    29: "Marcia Cabulon",
    30: "Mariana Lisboa Martins de Paula",
    31: "Meiriane Rodrigues",
    32: "Miguel M. Demétrio",
    33: "Nathália Braz dos Reis",
    34: "Nuria Tatiani Domingos Silva",
    35: "Rayana Costa Parro",
    36: "Rodriani Vian",
    37: "Silvia Letícia Morabito Porto",
    38: "Sonia Maria Cancela",
    39: "Stella G. Rodrigues",
    40: "Suelene Aparecida Botelho",
    41: "Tainá da Silva Miguel",
    42: "Vanessa C. Rodrigues",
    43: "Vilma Lucia Vieira",
    44: "Aperfeiçoandos / as",
    45: "Vitor Tomazine da Silva",
    46: "Regiane Junqueira Jamal",
}

admissao_clean['assistente_social'] = admissao_clean[
    'assistente_social'
].replace(assistentes_map)

# =========================
# Não finalizados
# =========================

nao_finalizados = admissao_clean[
    admissao_clean['demanda_resolvida'] == 'Não'
]

motivo_nao_finalizados = nao_finalizados.groupby(
    'demanda_resolvida'
)[
    ['assistente_social', 'unidade_internacao_alta', 'record_id']
].value_counts()

# =========================
# Unidade internação
# =========================

unidade_map = {
    1: "Emergência",
    2: "2° Andar enfermaria",
    3: "3° Andar enfermaria",
    4: "4° Andar enfermaria",
    5: "5° Andar enfermaria",
    6: "6° Andar enfermaria",
    7: "8° Andar enfermaria",
    8: "Unidade de AVC",
    9: "UICC",
    10: "UTIs",
    11: "Outro",
}

df_motivo_nao_finalizados = motivo_nao_finalizados.reset_index()

df_motivo_nao_finalizados['unidade_internacao_alta'] = (
    df_motivo_nao_finalizados['unidade_internacao_alta']
    .replace(unidade_map)
)

st.subheader("Demandas não finalizadas")

st.dataframe(df_motivo_nao_finalizados)

# =========================
# Motivos pendência social
# =========================

rename_map_for_sum = {
    'motivo_pendenciasocial___1':
        'Ausência de cuidador ou recusa familiar',

    'motivo_pendenciasocial___2':
        'Reorganização familiar pendente',

    'motivo_pendenciasocial___3':
        'Treinamento do cuidador não concluído',

    'motivo_pendenciasocial___4':
        'Adequação domiciliar não concluída',

    'motivo_pendenciasocial___5':
        'Ausência de local seguro para retorno',

    'motivo_pendenciasocial___6':
        'Vaga em ILPI/Hospital-Lar pendente',

    'motivo_pendenciasocial___7':
        'Vaga em UCP pendente',

    'motivo_pendenciasocial___8':
        'Treinamento profissionais da rede',

    'motivo_pendenciasocial___9':
        'Oxigênio domiciliar pendente',

    'motivo_pendenciasocial___10':
        'Ventilador mecânico portátil pendente',

    'motivo_pendenciasocial___11':
        'Aspirador de vias aéreas pendente',

    'motivo_pendenciasocial___12':
        'Fornecimento de medicamentos',

    'motivo_pendenciasocial___13':
        'Fornecimento de insumos assistenciais',

    'motivo_pendenciasocial___14':
        'Órgão de proteção pendente',

    'motivo_pendenciasocial___15':
        'Outros'
}

colunas_pendencia = list(rename_map_for_sum.keys())

# Verifica se todas existem
colunas_existentes = [
    col for col in colunas_pendencia
    if col in nao_finalizados.columns
]

dados_motivo = nao_finalizados[colunas_existentes].sum()

dados_motivo = dados_motivo.rename(index=rename_map_for_sum)

dados_motivo = dados_motivo.sort_values(ascending=False)

st.subheader("Motivos de pendência social")

st.dataframe(dados_motivo)
