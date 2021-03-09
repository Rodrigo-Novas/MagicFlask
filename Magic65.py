from flask import Flask, render_template, redirect, request, flash, redirect, url_for, jsonify, send_file
from flask_wtf.csrf import CSRFProtect
from utils import text_to_base, base_to_text

#chatterbot librerias
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import dataset as ds
from chatterbot.response_selection import get_most_frequent_response


app = Flask(__name__)

app.secret_key = "4ec7612e3d25cf3163c902689de75cdb"

csrf = CSRFProtect(app)

#chatbot instanciacion
chatbot = ChatBot("Riuriuk",
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.65,
            'default_response': 'Perdon, no tengo una respuesta para eso'
        }
    ],
    response_selection_method=get_most_frequent_response,
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database="db.sqlite3")

# chatbot.storage.drop()

trainer = ListTrainer(chatbot)

# trainer.train(ds.conversationSaludo)
# trainer.train(ds.conversationHerramientas)
# trainer.train(ds.conversationSantito)
# trainer.train(ds.conversationAmor)
# trainer.train(ds.conversationCv)
# trainer.train(ds.conversationJsonCV)
# trainer.train(ds.conversationPdf)
# trainer.train(ds.conversationQuerer)
# trainer.train(ds.conversationHerramientasPuedo)
# trainer.train(ds.conversationHerramientasTotal)
# trainer.train(ds.conversationQuererMinus)
# trainer.train(ds.conversationAmorMayus)
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    app.logger.info("Pagina inicio")
    return render_template("Magic64.html")


@app.route("/", methods=["GET", "POST"])
@app.route("/Conversor", methods=["GET", "POST"])
def Conversor():
    app.logger.info("Go to Conversor")
    try:
        if request.method == "POST":
            base=request.form["input64"] #toma desde name
            app.logger.info(f"{base}")
            texto=request.form["inputText"] #toma desde name
            app.logger.info(f"{texto}")
            if base != "" and texto == "":
                convertido_Texto=base_to_text(base)
                return jsonify(Respuesta="Base64 convertido satisfactoriamente a texto", Texto=base, Base64=convertido_Texto)
            if texto != "" and base == "":
                convertido_base=text_to_base(texto)
                return jsonify(Respuesta="Texto satisfactoriamente convertido a base64", Texto=texto, Base64=convertido_base)
        return render_template("conversorMagic64.html")
    except Exception as e:
        return jsonify(Respuesta="No pudo convertirse")

@app.route("/portfolio", methods=["GET"])
def portfolio():
    return render_template("Portfolio.html")

@app.route('/download', methods=["GET", "POST"])
def download_file():
    filename = r"Flask Upload Files\Base64 Guia.pdf"
    return send_file(filename, as_attachment=True)

@app.route('/process',methods=['POST'])
def process():
    user_input=request.form['Input_field']
    bot_response=chatbot.get_response(user_input)
    bot_response=str(bot_response)
    app.logger.info("Riuriuk: "+bot_response)
    return render_template('Magic64.html',user_input=user_input,bot_response=bot_response)


if __name__ == "__main__":
    app.run(debug=True, port=5000)