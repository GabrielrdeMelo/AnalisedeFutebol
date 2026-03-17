import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import pandas as pd
import time

print('Iniciando o Robo ...')

chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=chrome_options)

dicionario_ligas = {
    'la liga': 'https://fbref.com/en/comps/12/La-Liga-Stats',
    'premier league': 'https://fbref.com/en/comps/9/Premier-League-Stats',
    'serie a': 'https://fbref.com/en/comps/11/Serie-A-Stats',
    'bundesliga': 'https://fbref.com/en/comps/20/Bundesliga-Stats',
    'ligue 1': 'https://fbref.com/en/comps/13/Ligue-1-Stats',
}

dicionario_tabelas = {
    'La Liga': "https://fbref.com/en/comps/12/schedule/La-Liga-Scores-and-Fixtures",
    'Premier League': "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures",
    'Serie A': "https://fbref.com/en/comps/11/schedule/Serie-A-Scores-and-Fixtures",
    'Bundesliga': "https://fbref.com/en/comps/20/schedule/Bundesliga-Scores-and-Fixtures",
    'Ligue 1': "https://fbref.com/en/comps/13/schedule/Ligue-1-Scores-and-Fixtures"
}

dicionario_performance_individual = {
    'La Liga': "https://fbref.com/en/comps/12/stats/La-Liga-Stats",
    'Premier League': "https://fbref.com/en/comps/9/stats/Premier-League-Stats",
    'Serie A': "https://fbref.com/en/comps/11/stats/Serie-A-Stats",
    'Bundesliga': "https://fbref.com/en/comps/20/stats/Bundesliga-Stats",
    'Ligue 1': "https://fbref.com/en/comps/13/stats/Ligue-1-Stats"
}

for liga in dicionario_ligas:
    with pd.ExcelWriter(f'{liga}.xlsx', engine='xlsxwriter') as writer:
        driver.get(dicionario_ligas[liga])
        time.sleep(random.uniform(5,10))

        linhas = driver.find_elements(By.XPATH, "//table//tr")

        # ------------------- CLASSIFICAÇÃO -------------------
        dados_classificacao = []
        classificacao = linhas[:70]

        for linha in classificacao:
            celulas = [c.text for c in linha.find_elements(By.TAG_NAME, "td")]
            if any(celulas):
                dados_classificacao.append(celulas)

        cabecalho_classificacao = [
            'Time', 'Jogos', 'Vitórias', 'Empates', 'Derrotas', 'Gols Pró', 'Gols Contra',
            'Saldo de Gols', 'Pontos', 'Pts/MP',
            'Últimos Resultados', 'Público', 'Artilheiro', 'Goleiro'
        ]

        dados_classificacao = [linha[:len(cabecalho_classificacao)] for linha in dados_classificacao]

        for linha in dados_classificacao:
            while len(linha) < len(cabecalho_classificacao):
                linha.append(None)

        df_classificacao = pd.DataFrame(dados_classificacao, columns=cabecalho_classificacao)
        df_classificacao.to_excel(writer, sheet_name=f"{liga}", index=False)

        # ------------------- PERFORMANCE -------------------
        dados_performance = []
        performance = linhas[71:141]

        for linha in performance:
            times = [t.text for t in linha.find_elements(By.TAG_NAME, "th")]
            celulas = [c.text for c in linha.find_elements(By.TAG_NAME, "td")]
            if any(celulas):
                dados_performance.append(times + celulas)

        cabecalho_performance = [
            "Times", "Plantel", "Idade", "Posse", "Partidas", "Starts", "Min", "90s", "Gols", "Assist", "G+A",
            "Gol sem penâlti", "Gols de penâlti", "Penâltis", "Amarelo", "Vermelho", "xG", "xG sem penâlti", "xAssist",
            "npxG+xAssist",
            "npxG+xAG/90"
        ]

        dados_performance = [linha[:len(cabecalho_performance)] for linha in dados_performance]

        for linha in dados_performance:
            while len(linha) < len(cabecalho_performance):
                linha.append(None)

        df_performance = pd.DataFrame(dados_performance, columns=cabecalho_performance)
        df_performance.to_excel(writer, sheet_name=f"{liga}_performance", index=False)

# ------------------- TABELAS -------------------
liga = None

for liga in dicionario_tabelas:
    with pd.ExcelWriter(f'{liga}.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:

        driver.get(dicionario_tabelas[liga])
        time.sleep(2)

        linhas = driver.find_elements(By.XPATH, "//table//tr")

        dados_tabela = []
        tabela = linhas[:390]

        for linha in tabela:
            semana = [t.text for t in linha.find_elements(By.TAG_NAME, "th")]
            celulas = [c.text for c in linha.find_elements(By.TAG_NAME, "td")]
            if any(celulas):
                dados_tabela.append(semana + celulas)

        cabecalho_tabela = [
            'Semana', 'Dia', 'Data', 'Hora', 'Casa', 'Placar',
            'Fora', 'Público', 'Estádio', 'Juiz', 'Informe da partida'
        ]

        dados_tabela = [linha[:len(cabecalho_tabela)] for linha in dados_tabela]

        for linha in dados_tabela:
            while len(linha) < len(cabecalho_tabela):
                linha.append(None)

        df_tabelas = pd.DataFrame(dados_tabela, columns=cabecalho_tabela)
        df_tabelas.to_excel(writer, sheet_name=f"{liga}_tabela", index=False)

# ------------------- Performance Individual -------------------
liga = None

for liga in dicionario_performance_individual:
    with pd.ExcelWriter(f'{liga}.xlsx', engine='openpyxl', mode='a', if_sheet_exists='new') as writer:

        driver.get(dicionario_performance_individual[liga])
        time.sleep(2)

        linhas = driver.find_elements(By.XPATH, "//table//tr")

        dados_performance = []
        performance = linhas[71:600]

        for linha in performance:
            times = [t.text for t in linha.find_elements(By.TAG_NAME, "th")]
            celulas = [c.text for c in linha.find_elements(By.TAG_NAME, "td")]
            if any(celulas):
                dados_performance.append(times + celulas)

        cabecalho_performance = [
            "Rank", "Jogador", "Nacionalidade", "Posição", "Time", "Idade", "Nascimento", "Partidas Jogadas",
            "Titular", "Minutos", "90s", "Gols", "Assists", "G+A", "Gols sem penâlti","Gols de penâlti",
            "Penâtis Batidos", "Amarelo", "Vermelho", "G/90", "G sem penâlti/90", "Assist/90", "npxG+xAssist/90", "Partidas"
        ]

        dados_performance = [linha[:len(cabecalho_performance)] for linha in dados_performance]

        for linha in dados_performance:
            while len(linha) < len(cabecalho_performance):
                linha.append(None)

        df_performance = pd.DataFrame(dados_performance, columns=cabecalho_performance)
        df_performance.to_excel(writer, sheet_name=f"{liga}_jogadores", index=False)

        print(f'Dados da {liga} salvos no Excel com sucesso!')

driver.quit()