# Extrair informações do formulário de casa de apoio
# TH - 07-05-2026

import streamlit as st
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

pd.options.display.max_rows = None
pd.options.display.max_columns = None

st.set_page_config(
    page_title="Análise Casa de Apoio",
    layout="wide"
)

st.title("Análise Casa de Apoio")

# =====================================================
# Upload principal - Casa de apoio
# =====================================================

uploaded_file = st.file_uploader(
    "Selecione o arquivo CSV da casa de apoio",
    type=["csv"],
    key="casa_apoio"
)

if uploaded_file is not None:

    dataset = pd.read_csv(uploaded_file)

    # =====================================================
    # Conversão de data
    # =====================================================

    if 'data_solicitacao' in dataset.columns:

        dataset['data_solicitacao'] = pd.to_datetime(
            dataset['data_solicitacao'],
            errors='coerce'
        )

        # =====================================================
        # Filtro de datas
        # =====================================================

        col1, col2 = st.columns(2)

        with col1:
            data_inicio = st.date_input(
                "Data inicial",
                key="inicio_cr"
            )

        with col2:
            data_final = st.date_input(
                "Data final",
                key="fim_cr"
            )

        dataset_filtrado = dataset[
            (dataset['data_solicitacao'] >= pd.to_datetime(data_inicio)) &
            (dataset['data_solicitacao'] <= pd.to_datetime(data_final))
        ].copy()

        # =====================================================
        # Indicadores gerais
        # =====================================================

        total_vagas = dataset_filtrado[
            'total_tentativas'
        ].sum() if 'total_tentativas' in dataset_filtrado.columns else 0

        total_tentativas_aceitas = dataset_filtrado[
            'total_tentativa_aceitas'
        ].sum() if 'total_tentativa_aceitas' in dataset_filtrado.columns else 0

        total_tentativas_negadas = dataset_filtrado[
            'total_tentativa_negadas'
        ].sum() if 'total_tentativa_negadas' in dataset_filtrado.columns else 0

        st.subheader("Indicadores Gerais")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total de solicitações", int(total_vagas))
        col2.metric("Solicitações aceitas", int(total_tentativas_aceitas))
        col3.metric("Solicitações negadas", int(total_tentativas_negadas))

        # =====================================================
        # Negativas
        # =====================================================

        if 'vagas_fornecidas' in dataset_filtrado.columns:
            dataset_filtrado['vagas_fornecidas'] = dataset_filtrado[
                'vagas_fornecidas'
            ].fillna(0)

        if 'total_tentativa_negadas' in dataset_filtrado.columns:

            vagas_n = dataset_filtrado['total_tentativa_negadas'] > 0

            st.subheader("Pacientes com negativa")

            colunas_negativa = [
                col for col in [
                    'record_id',
                    'total_tentativa_negadas',
                    'total_tentativa_aceitas',
                    'quantidade_vagas',
                    'vagas_fornecidas'
                ]
                if col in dataset_filtrado.columns
            ]

            st.dataframe(
                dataset_filtrado.loc[vagas_n, colunas_negativa],
                use_container_width=True
            )

        # =====================================================
        # Motivos de negativa
        # =====================================================

        map_motivos = {
            1: "Capacidade da instituição",
            2: "Perfil incompatível",
            3: "Administrativos/logísticos",
            4: "Sociais/decisão usuário",
            5: "Outros",
        }

        colunas_motivos = [
            'motivo_negativa',
            'motivo_negativa_2',
            'motivo_negativa_3',
            'motivo_negativa_4',
            'motivo_negativa_5',
            'motivo_negativa_6',
            'motivo_negativa_7'
        ]

        colunas_existentes = [
            col for col in colunas_motivos
            if col in dataset_filtrado.columns
        ]

        if len(colunas_existentes) > 0:

            for coluna in colunas_existentes:
                dataset_filtrado[coluna] = dataset_filtrado[
                    coluna
                ].replace(map_motivos)

            motivos = dataset_filtrado[colunas_existentes]

            motivos_long = motivos.melt(value_name='Motivo')
            motivos_long = motivos_long.dropna(subset=['Motivo'])

            frequencia = motivos_long[
                'Motivo'
            ].value_counts().reset_index()

            frequencia.columns = ['Motivo', 'Quantidade']

            st.subheader("Frequência dos motivos de negativa")

            st.dataframe(
                frequencia,
                use_container_width=True
            )

        # =====================================================
        # Complexos
        # =====================================================

        complexo_map = {
            1: 'Ambulatório',
            2: 'ICA',
            3: 'HB',
            4: 'HCM'
        }

        if 'complexo_funfarme' in dataset_filtrado.columns:

            dataset_filtrado['complexo_funfarme'] = dataset_filtrado[
                'complexo_funfarme'
            ].replace(complexo_map)

            total_vagas_fornecidas = dataset_filtrado.groupby(
                'complexo_funfarme'
            )['vagas_fornecidas'].sum()

            total_vagas_solicitadas = dataset_filtrado.groupby(
                'complexo_funfarme'
            )['quantidade_vagas'].sum()

            st.subheader("Vagas por complexo")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Vagas solicitadas")
                st.dataframe(
                    total_vagas_solicitadas,
                    use_container_width=True
                )

            with col2:
                st.write("Vagas fornecidas")
                st.dataframe(
                    total_vagas_fornecidas,
                    use_container_width=True
                )

        # =====================================================
        # Destino usuário
        # =====================================================

        destino_map = {
            1: "Permaneceu internado",
            2: "Hotel",
            3: "Aluguel",
            4: "Casa familiar",
            5: "Retorno município",
            6: "Outro"
        }

        if 'destino_usuario' in dataset_filtrado.columns:

            dataset_filtrado['destino_usuario'] = dataset_filtrado[
                'destino_usuario'
            ].replace(destino_map)

            st.subheader("Destino do usuário")

            st.dataframe(
                dataset_filtrado[
                    'destino_usuario'
                ].value_counts(),
                use_container_width=True
            )

        # =====================================================
        # Casas de apoio
        # =====================================================

        casa_map = {
            1: "AMICC",
            2: "CAPACC",
            3: "PÃO DA VIDA",
            4: "JOÃO PAULO II",
            5: "THALES",
            6: "MUNICÍPIOS"
        }

        if 'casa_apoio' in dataset_filtrado.columns:

            dataset_filtrado['casa_apoio'] = dataset_filtrado[
                'casa_apoio'
            ].replace(casa_map)

            st.subheader("Casas de apoio")

            st.dataframe(
                dataset_filtrado[
                    'casa_apoio'
                ].value_counts(),
                use_container_width=True
            )

else:
    st.warning("Envie o arquivo CSV da casa de apoio.")

# =====================================================
# Upload admissões
# =====================================================

st.divider()

uploaded_file_ar = st.file_uploader(
    "Selecione o arquivo CSV de admissões",
    type=["csv"],
    key="admissao"
)

if uploaded_file_ar is not None:

    admissao = pd.read_csv(uploaded_file_ar)

    # =====================================================
    # Conversão data
    # =====================================================

    if 'data_prevista_alta' in admissao.columns:

        admissao['data_prevista_alta'] = pd.to_datetime(
            admissao['data_prevista_alta'],
            errors='coerce'
        )

        # =====================================================
        # Filtro datas admissões
        # =====================================================

        col1, col2 = st.columns(2)

        with col1:
            data_abertura_inicio = st.date_input(
                "Data inicial admissões",
                key="inicio_adm"
            )

        with col2:
            data_abertura_final = st.date_input(
                "Data final admissões",
                key="fim_adm"
            )

        admissao_clean = admissao[
            (
                admissao['data_prevista_alta']
                >= pd.to_datetime(data_abertura_inicio)
            ) &
            (
                admissao['data_prevista_alta']
                <= pd.to_datetime(data_abertura_final)
            )
        ].copy()

        total_admissao = admissao_clean.shape[0]

        st.subheader("Admissões")

        st.metric(
            "Total de atendimentos",
            total_admissao
        )

        # =====================================================
        # Falha processo
        # =====================================================

        falha_map = {
            1: "Sim",
            0: "Não"
        }

        if 'houve_falha_processo' in admissao_clean.columns:

            admissao_clean['houve_falha_processo'] = admissao_clean[
                'houve_falha_processo'
            ].replace(falha_map)

            st.subheader("Falha no processo")

            st.dataframe(
                admissao_clean[
                    'houve_falha_processo'
                ].value_counts(),
                use_container_width=True
            )

        # =====================================================
        # Demandas resolvidas
        # =====================================================

        finalizados_map = {
            1: "Sim",
            0: "Não"
        }

        if 'demanda_resolvida' in admissao_clean.columns:

            admissao_clean['demanda_resolvida'] = admissao_clean[
                'demanda_resolvida'
            ].replace(finalizados_map)

            finalizados = admissao_clean[
                'demanda_resolvida'
            ].value_counts()

            st.subheader("Demandas resolvidas")

            st.dataframe(
                finalizados,
                use_container_width=True
            )

        # =====================================================
        # Assistentes sociais
        # =====================================================

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

        if 'assistente_social' in admissao_clean.columns:

            admissao_clean['assistente_social'] = admissao_clean[
                'assistente_social'
            ].replace(assistentes_map)

        # =====================================================
        # Não finalizados
        # =====================================================

        if 'demanda_resolvida' in admissao_clean.columns:

            nao_finalizados = admissao_clean[
                admissao_clean['demanda_resolvida'] == 'Não'
            ]

            # =====================================================
            # Unidade internação
            # =====================================================

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

            if 'unidade_internacao_alta' in nao_finalizados.columns:

                nao_finalizados['unidade_internacao_alta'] = (
                    nao_finalizados['unidade_internacao_alta']
                    .replace(unidade_map)
                )

            colunas_analise = [
                col for col in [
                    'assistente_social',
                    'unidade_internacao_alta',
                    'record_id'
                ]
                if col in nao_finalizados.columns
            ]

            if len(colunas_analise) > 0:

                motivo_nao_finalizados = nao_finalizados[
                    colunas_analise
                ].value_counts().reset_index()

                st.subheader("Demandas não finalizadas")

                st.dataframe(
                    motivo_nao_finalizados,
                    use_container_width=True
                )

            # =====================================================
            # Motivos pendência social
            # =====================================================

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

            colunas_existentes = [
                col for col in colunas_pendencia
                if col in nao_finalizados.columns
            ]

            if len(colunas_existentes) > 0:

                dados_motivo = nao_finalizados[
                    colunas_existentes
                ].sum()

                dados_motivo = dados_motivo.rename(
                    index=rename_map_for_sum
                )

                dados_motivo = dados_motivo.sort_values(
                    ascending=False
                )

                st.subheader("Motivos de pendência social")

                st.dataframe(
                    dados_motivo,
                    use_container_width=True
                )

else:
    st.warning("Envie o arquivo CSV de admissões.")
