import requests

# Sua chave da API já configurada
API_KEY = "fb20cf2aa07c35c1401da00272789add"

print("Bem-vindo ao App de Previsão do Tempo!")

while True:
    cidade = input("\nDigite o nome da cidade (ou 'sair' para fechar): ")

    if cidade.lower() == 'sair':
        print("Saindo do aplicativo... Até a próxima!")
        break

    # Montamos o link com a cidade que o usuário digitou
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&lang=pt_br&units=metric"

    # Fazemos a requisição para a internet
    requisicao = requests.get(link)
    dados = requisicao.json()

    # O código 200 significa que a resposta deu 100% certo na internet
    if requisicao.status_code == 200:
        nome = dados["name"]
        temperatura = dados["main"]["temp"]
        sensacao = dados["main"]["feels_like"] # Puxando a sensação térmica
        umidade = dados["main"]["humidity"]    # Puxando a umidade
        descricao = dados["weather"][0]["description"]

        print(f"\n--- Clima atual em {nome} ---")
        print(f"Temperatura: {temperatura} °C")
        print(f"Sensação Térmica: {sensacao} °C")
        print(f"Umidade: {umidade}%")
        print(f"Condição: {descricao.capitalize()}")
        
    # Tratando o erro 401 (Chave inválida ou não ativada)
    elif requisicao.status_code == 401:
        print("\n❌ Erro de Autenticação: Sua chave ainda não ativou ou está incorreta. Tente novamente mais tarde.")
        
    # Tratando o erro 404 (Cidade não encontrada pelo OpenWeatherMap)
    elif requisicao.status_code == 404:
        print("\n❌ Cidade não encontrada. Verifique se você digitou o nome corretamente.")
        
    # Tratando qualquer outro erro desconhecido
    else:
        print(f"\n❌ Ocorreu um erro desconhecido. Código do erro: {requisicao.status_code}")