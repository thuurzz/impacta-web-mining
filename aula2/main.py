# Integrantes:
# Arthur Vinicius Santos Silva RA:1903365

from flask import Flask, jsonify
import pandas as pd 

app = Flask(__name__)

@app.route('/')
def hello_word():
    return {"status": "Py Tha On"}

@app.route('/jogo')
def lista_de_jogos():
    dados = pd.read_csv('./futebol.csv', sep=";")

    resposta = []

    for k,v in dados.iterrows(): 
        l = {
            "nome_time_casa" : v["home_team_name"],
            "nome_time_visitante" : v["away_team_name"],
            "placar": f'{v["home_team_goal_count"]} X {v["away_team_goal_count"]}',
            "data_da_partida": v["date_GMT"]
        }
        resposta.append(l)

    return jsonify(resposta)


@app.route('/casa')
def dados_time():
    dados = pd.read_csv('./futebol.csv', sep=";")

    def extrai_dados(dados, nomeTime):
        casa = dados.loc[(dados["home_team_name"] == nomeTime)]
        fora = dados.loc[(dados["away_team_name"] == nomeTime)]
        l = {
            "nome_time" : str(nomeTime),
            "quantidade_de_gols" : str(casa["home_team_goal_count"].sum() + fora["away_team_goal_count"].sum()),
            "quantidade_de_jogos": str(len(casa) + len(fora)),
        }
        return l
    
    resposta = {}
    resposta.update({"Sampdoria":extrai_dados(dados, "Sampdoria")})
    resposta.update({"Olimpia":extrai_dados(dados, "Olimpia")})
    resposta.update({"Millwall":extrai_dados(dados, "Millwall")})

    return jsonify(resposta)

@app.route('/juizes')
def lista_de_juizes():
    dados = pd.read_csv('./futebol.csv', sep=";")

    resposta = []
    dados_juiz = dados["referee"].value_counts()
    for k in dados_juiz.keys(): 
        juiz = {
            "nome_juiz" : str(k),
            "quantidade_de_jogos": str(dados_juiz[k])
        }
        resposta.append(juiz)

    return jsonify(resposta)

app.run()
