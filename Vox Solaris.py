import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import math

def calcular_rendimento_e_necessidade(consumo, potencia_modelo_w, irradiacao_diaria, perdas_percentual, custo_por_placa):
    if not all(isinstance(val, (int, float)) for val in [consumo, potencia_modelo_w, irradiacao_diaria, custo_por_placa]):
        return "Erro: Todos os valores numéricos devem ser números."
    if consumo <= 0:
        return "Erro: O consumo deve ser um número positivo."
    if potencia_modelo_w <= 0:
        return "Erro: A potência do modelo da placa solar deve ser um número positivo."
    if irradiacao_diaria <= 0:
        return "Erro: A irradiação solar média deve ser um número positivo."
    if custo_por_placa < 0:
        return "Erro: O custo por placa não pode ser negativo."

    perdas = perdas_percentual / 100.0
    potencia_kw = potencia_modelo_w / 1000
    energia_dia_por_placa = potencia_kw * irradiacao_diaria * (1 - perdas)
    energia_mes_por_placa = energia_dia_por_placa * 30

    if energia_mes_por_placa <= 0:
        return "Erro: Com os dados fornecidos, uma placa não geraria energia positiva. Verifique irradiação e perdas."

    numero_placas = math.ceil(consumo / energia_mes_por_placa)
    custo_total_estimado = numero_placas * custo_por_placa

    return {
        "energia_mes_por_placa": energia_mes_por_placa,
        "numero_placas": numero_placas,
        "custo_total_estimado": custo_total_estimado
    }

# Funções da Interface Gráfica
def mostrar_tela_calculo():
    frame_inicial.pack_forget()
    frame_calculo.pack(padx=20, pady=20, fill="both", expand=True)
    label_resultado_energia.config(text="")
    label_resultado_numero.config(text="")
    label_resultado_custo.config(text="")

def executar_calculo():
    try:
        consumo_val = float(entry_consumo.get())
        modelo_val = float(entry_modelo.get())
        irradiacao_val = float(entry_irradiacao.get())
        custo_placa_val = float(entry_custo_placa.get())
        perdas_val = 20 # Mantendo fixo

        resultados = calcular_rendimento_e_necessidade(
            consumo_val, modelo_val, irradiacao_val, perdas_val, custo_placa_val
        )

        if isinstance(resultados, str):
            messagebox.showerror("Erro de Validação", resultados)
            label_resultado_energia.config(text="")
            label_resultado_numero.config(text="")
            label_resultado_custo.config(text="")
        else:
            label_resultado_energia.config(
                text=f"Energia por placa/mês: {resultados['energia_mes_por_placa']:.2f} kWh"
            )
            label_resultado_numero.config(
                text=f"Placas necessárias: {resultados['numero_placas']}"
            )
            label_resultado_custo.config(
                text=f"Investimento estimado: R$ {resultados['custo_total_estimado']:.2f}"
            )

    except ValueError:
        messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        label_resultado_energia.config(text="")
        label_resultado_numero.config(text="")
        label_resultado_custo.config(text="")

#Configuração da Janela Principal

root = tb.Window(themename="superhero") # Experimente: "cyborg", "darkly", "vapor"
root.title("VOX SOLARIS")
root.geometry("550x650")

# Tela inicial
frame_inicial = tb.Frame(root, padding="50")
frame_inicial.pack(expand=True)

label_titulo_inicial = tb.Label( 
    frame_inicial,
    text="Vox Solaris",
    font=("Arial", 20, "bold"), 
    bootstyle=PRIMARY 
)
label_titulo_inicial.pack(pady=30)

botao_entrar = tb.Button( 
    frame_inicial,
    text="Entrar",
    command=mostrar_tela_calculo,
    bootstyle=(SUCCESS, OUTLINE)
)
botao_entrar.pack(pady=20, ipady=10, ipadx=30) 
#Tela de Cálculo
frame_calculo = tb.Frame(root, padding="20") 

# Consumo
tb.Label(frame_calculo, text="Consumo médio da casa (kWh/mês):").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_consumo = tb.Entry(frame_calculo, width=25, bootstyle=INFO) # Adicionar bootstyle ao Entry
entry_consumo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

# Modelo da Placa
tb.Label(frame_calculo, text="Potência do modelo da placa (W):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_modelo = tb.Entry(frame_calculo, width=25, bootstyle=INFO)
entry_modelo.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

# Irradiação
tb.Label(frame_calculo, text="Irradiação solar média DIÁRIA (kWh/m²/dia ou HSP):").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_irradiacao = tb.Entry(frame_calculo, width=25, bootstyle=INFO)
entry_irradiacao.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
tb.Label(frame_calculo, text="(Ex: 4.5 para 4.5 kWh/m²/dia)", font=("Arial", 9), bootstyle=SECONDARY).grid(row=3, column=0, columnspan=2, padx=10, pady=2, sticky="w")

# Custo por Placa
tb.Label(frame_calculo, text="Custo por placa solar (R$):").grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_custo_placa = tb.Entry(frame_calculo, width=25, bootstyle=INFO)
entry_custo_placa.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

# Botão Calcular
botao_calcular = tb.Button(frame_calculo, text="Calcular", command=executar_calculo, bootstyle=PRIMARY)
botao_calcular.grid(row=5, column=0, columnspan=2, pady=25, ipady=8)

# --- Área de Resultados ---
tb.Separator(frame_calculo, orient='horizontal', bootstyle=SECONDARY).grid(row=6, column=0, columnspan=2, sticky='ew', pady=15)

label_resultados_titulo = tb.Label(frame_calculo, text="Resultados Estimados:", font=("Arial", 14, "bold"), bootstyle=INFO)
label_resultados_titulo.grid(row=7, column=0, columnspan=2, pady=(10, 10))

label_resultado_energia = tb.Label(frame_calculo, text="", font=("Arial", 11))
label_resultado_energia.grid(row=8, column=0, columnspan=2, pady=5, sticky="w")

label_resultado_numero = tb.Label(frame_calculo, text="", font=("Arial", 11))
label_resultado_numero.grid(row=9, column=0, columnspan=2, pady=5, sticky="w")

label_resultado_custo = tb.Label(frame_calculo, text="", font=("Arial", 11))
label_resultado_custo.grid(row=10, column=0, columnspan=2, pady=5, sticky="w")

frame_calculo.columnconfigure(1, weight=1)

root.mainloop()