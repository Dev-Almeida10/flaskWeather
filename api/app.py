from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/weather", methods=['POST'])
def api_clima():

    api_chave = '885c0cf1895ad0adb880824d152d27b6'
    cidade_user = request.form['cidade']

    api_link = f'https://api.openweathermap.org/data/2.5/weather?q={cidade_user}&appid={api_chave}&lang=pt_br'
    
    try:

        requisicao = requests.get(api_link)
        dic_requisicao = requisicao.json()


        informacoes_clima = {

            "condicoes_ceu": dic_requisicao['weather'][0]['description'],
            "temperatura": dic_requisicao['main']['temp'] - 273.15,
            "estado": dic_requisicao['name'],
            "pais": dic_requisicao['sys']['country'],
            "umidade": dic_requisicao['main']['humidity'],
            "velocidade_vento": dic_requisicao['wind']['speed'],
            "icon": dic_requisicao['weather'][0]['icon'],

         }

        
        # formatação dos números
        informacoes_clima["temperatura"] = '{:.0f}'.format(informacoes_clima["temperatura"])
        informacoes_clima["velocidade_vento"] = '{:.0f}'.format(informacoes_clima["velocidade_vento"])
      
        erro = False

        return render_template('index.html', informacoes_clima=informacoes_clima)
    
    except requests.exceptions.RequestException as e:

        # erro de requisição
        erro = "Erro ao buscar a cidade."
        return render_template('index.html', erro=erro)
    
    except KeyError as e:
        
        # Erro chave não encontrada
        erro = "Cidade não encontrada"
        return render_template('index.html', erro=erro)
    
    except Exception as e:

        # outros possiveis erros
        erro = "Erro desconhecido. Tente novamente mais tarde =)"
        return render_template('index.html', erro=erro)


if __name__ == "__main__": 
    app.run(debug=True) 