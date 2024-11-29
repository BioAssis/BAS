import pandas as pd
import numpy as np
import copy
import streamlit as st # type: ignore
import funcoes.funcoes_gerais as fn


def iniciar_ver_mais():

    # Sobre o Projeto
    st.write("""
    A construção e desenvolvimento do **BAS** ocorreu durante todo o 2° semestre do ano de 2024, como um projeto da matéria de Iniciação à Pesquisa III,
    da Ilum - Escola de Ciências, institucionalizada pelo Centro Nacional de Pesquisa em Energia e Materiais (CNPEM), no qual os alunos receberam 
    a proposta de criar um aplicativo voltado para impulsionar pequisas na área de bioprecessos através de análise cinética de perfis de 
    crescimento microbiano. Além disso, mais informaçãoes sobre a construção e estrutura de dados do software pode ser encontrada acessando o 
    [GitHub](https://github.com/BioAssis/BAS) do site.
    """)


    # Criadores e Idealizadores
    st.header("Criadores e Idealizadores")

    # Estudantes
    st.subheader("Estudantes")
    st.markdown("""
    - **Beatriz Borges Ribeiro**  
    Email: [beatriz23028@ilum.cnpem.br](mailto:beatriz23028@ilum.cnpem.br)  
    Aluna do 4° Semestre do Curso de Bacharel em Ciência e Tecnologia, Ilum - Escola de Ciências.  
    [LinkedIn](https://www.linkedin.com/in/beatriz-borges-ribeiro-5545971a0/) | [GitHub](https://github.com/beatrizborgesr)

    - **Daniel Bravin Martins**  
    Email: [daniel23020@ilum.cnpem.br](mailto:daniel23020@ilum.cnpem.br)  
    Aluno do 4° Semestre do Curso de Bacharel em Ciência e Tecnologia, Ilum - Escola de Ciências.  
    [LinkedIn](https://www.linkedin.com/in/daniel-bravin-a52355312/) | [GitHub](https://github.com/MrBravin)
    """,unsafe_allow_html=True)

    # Pesquisadores
    st.subheader("Pesquisadores Responsáveis")
    st.markdown("""
    - **Isabella Lobos de Mesquita Sampaio**  
    Email: [isabelle.sampaio@lnbr.cnpem.br](mailto:isabelle.sampaio@lnbr.cnpem.br)  
    Graduada em Engenharia Química, Doutora em Bioenergia pela Unicamp e atualmente pesquisadora do Laboratório Nacional de Biorrenováveis.

    - **João H. Colombelli Manfrão Netto**  
    Email: [joao.netto@lnbr.cnpem.br](mailto:joao.netto@lnbr.cnpem.br)  
    Doutor e Mestre em Biologia Molecualar pela Universidade de Brasilía e atualmente pesquisador do Laboratório Nacional de Biorrenováveis.
    """)

    # Contribuição Importante
    st.subheader("Contribuição Inicial:")
    st.write("""
    Uma versão teste de conceito foi inicialmente desenvolvida por **Micael Montauvani Baruch**, ex-estagiário do LNBr. 
    Essa versão foi fundamental para a conclusão e síntese deste projeto.
    """)

    # Agradecimentos
    st.header("Agradecimentos")
    st.write("""
    Gostaríamos de expressar nossa gratidão:

    - Aos pesquisadores mencionados acima, pelo suporte e orientação durante o desenvolvimento do projeto.
    - Ao **LNBr**, pela estrutura e receptividade.
    - A todos que contribuíram, direta ou indiretamente, para a concepção do BAS.

    Muito obrigado e aproveitem o BAS!
    """)

    st.markdown("<br>" * 4, unsafe_allow_html=True)
    colunas = st.columns(4)

    
    with colunas[3]: 
        if st.button("Página Inicial"):
            st.switch_page("Pagina_Inicial.py")

