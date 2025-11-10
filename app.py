from flask import Flask, render_template, request
import math

app = Flask(__name__)

def calcular_rendimento_e_necessidade(consumo, potencia_modelo_w, irradiacao_diaria, perdas_percentual, custo_por_placa):
    try:
        consumo = float(str(consumo).replace(',', '.'))
        potencia_modelo_w = float(str(potencia_modelo_w).replace(',', '.'))
        irradiacao_diaria = float(str(irradiacao_diaria).replace(',', '.'))
        custo_por_placa = float(str(custo_por_placa).replace(',', '.'))
    except (ValueError, TypeError):
        return {"erro": "Por favor, insira valores numéricos válidos."}

    if consumo <= 0 or potencia_modelo_w <= 0 or irradiacao_diaria <= 0 or custo_por_placa < 0:
        return {"erro": "Todos os valores devem ser positivos, exceto o custo por placa, que não pode ser negativo."}

    perdas = perdas_percentual / 100.0
    potencia_kw = potencia_modelo_w / 1000
    energia_dia_por_placa = potencia_kw * irradiacao_diaria * (1 - perdas)
    energia_mes_por_placa = energia_dia_por_placa * 30

    if energia_mes_por_placa <= 0:
        return {"erro": "Com os dados fornecidos, uma placa não geraria energia. Verifique irradiação e perdas."}

    numero_placas = math.ceil(consumo / energia_mes_por_placa)
    custo_total_estimado = numero_placas * custo_por_placa

    return {
        "energia_mes_por_placa": f"{energia_mes_por_placa:.2f}",
        "numero_placas": numero_placas,
        "custo_total_estimado": f"{custo_total_estimado:.2f}"
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    if request.method == 'POST':
        consumo = request.form.get('consumo')
        potencia = request.form.get('potencia')
        irradiacao = request.form.get('irradiacao')
        custo = request.form.get('custo')
        perdas = 20  # Fixo

        resultados = calcular_rendimento_e_necessidade(consumo, potencia, irradiacao, perdas, custo)
        return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=False)
