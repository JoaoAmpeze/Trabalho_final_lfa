import os
import tempfile
from flask import Flask, request, send_file, jsonify
from main import (
    carregar_gramatica,
    converter_afn_para_afd,
    minimizar_afd,
    salvar_csv,
)


app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    return response


@app.route("/converter", methods=["POST", "OPTIONS"])
def converter():
    if request.method == "OPTIONS":
        return ("", 204)

    arquivo = request.files.get("file")
    texto = request.form.get("text")

    if not arquivo and not texto:
        return jsonify({"erro": "Envie um arquivo ('file') ou texto ('text')."}), 400

    entrada_path = None
    saida_path = None

    try:

        entrada_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        saida_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        entrada_path = entrada_tmp.name
        saida_path = saida_tmp.name
        entrada_tmp.close()
        saida_tmp.close()

        if arquivo:
            arquivo.save(entrada_path)
        else:
            with open(entrada_path, "w", encoding="utf-8") as f:
                f.write(texto or "")

        afn = carregar_gramatica(entrada_path)
        afd = converter_afn_para_afd(afn)
        afd_min = minimizar_afd(afd)
        salvar_csv(afd_min, saida_path)


        if arquivo and arquivo.filename:
            base, _ = os.path.splitext(arquivo.filename)
            download_name = f"{base}_saida.csv"
        else:
            download_name = "saida_afd.csv"

        return send_file(
            saida_path,
            mimetype="text/csv",
            as_attachment=True,
            download_name=download_name,
        )
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 400
    except Exception as exc:  
        return jsonify({"erro": f"Falha ao processar a gramática: {exc}"}), 500
    finally:

        for path in (entrada_path, saida_path):
            if path:
                try:
                    os.remove(path)
                except OSError:
                    pass


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000, debug=True)

