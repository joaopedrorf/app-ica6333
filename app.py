import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request

app = Flask(__name__)

def validar_hora(hora_str):
    try:
        return datetime.strptime(hora_str, "%H:%M")
    except ValueError:
        return None

def verificar_pcrcc(inicio, fim):
    pcrcc_inicio = timedelta(hours=1, minutes=30)
    pcrcc_fim = timedelta(hours=5, minutes=29)
    
    atual = inicio
    passo = timedelta(minutes=1)
    
    while atual <= fim:
        tempo_atual = timedelta(hours=atual.hour, minutes=atual.minute)
        if pcrcc_inicio <= tempo_atual <= pcrcc_fim:
            return True
        atual += passo
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    monitoria = None
    repouso = None
    erro = None

    if request.method == "POST":
        aba = request.form.get("aba")

        if aba == "turno":
            hora_entrada_raw = request.form.get("hora_entrada", "").strip()
            dt_entrada = validar_hora(hora_entrada_raw)
            
            if not dt_entrada:
                erro = "Formato de hora inválido para a entrada do turno."
            else:
                dt_limite = dt_entrada + timedelta(hours=2)
                monitoria = {
                    "entrada": dt_entrada.strftime("%H:%M"),
                    "limite": dt_limite.strftime("%H:%M")
                }

        elif aba == "repouso":
            hora_termino_raw = request.form.get("hora_termino", "").strip()
            tipo_plantao = request.form.get("tipo_plantao", "")
            
            dt_termino = validar_hora(hora_termino_raw)
            
            if not dt_termino:
                erro = "Formato de hora inválido para o término do plantão."
            else:
                horas_descanso = 12
                if tipo_plantao == "noturno":
                    horas_descanso = 24
                
                dt_liberacao = dt_termino + timedelta(hours=horas_descanso)
                repouso = {
                    "termino": dt_termino.strftime("%H:%M"),
                    "liberacao": dt_liberacao.strftime("%H:%M"),
                    "horas": horas_descanso
                }

    return render_template("index.html", monitoria=monitoria, repouso=repouso, erro=erro)

if __name__ == "__main__":
    app.run(debug=False)