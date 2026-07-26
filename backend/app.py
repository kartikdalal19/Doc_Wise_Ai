from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os


from core.pipeline import RAGPipeline
from agents.graph import RAGGraph


# --------------------------------------------------
# Flask Setup
# --------------------------------------------------

from flask import Flask, send_from_directory

# app = Flask(
#     __name__,
#     static_folder="../frontend",
#     static_url_path=""
# )

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)


app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)


app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# @app.route("/")
# def home():

#     return send_from_directory(
#         "../frontend",
#         "index.html"
#     )




@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )




# @app.route("/chat")
# def chat_page():

#     return send_from_directory(
#         "../frontend",
#         "index1.html"
#     )


@app.route("/chat")
def chat_page():

    return send_from_directory(
        FRONTEND_DIR,
        "index1.html"
    )


CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



# --------------------------------------------------
# Global RAG Objects
# --------------------------------------------------

rag = None
graph = None


@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "document_loaded": graph is not None
    })



# --------------------------------------------------
# Upload PDF
# --------------------------------------------------

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():


    global rag, graph


    if "file" not in request.files:

        return jsonify({
          "success": False,
          "message": "No file uploaded"
        }), 400



    file = request.files["file"]


    if file.filename == "":

        return jsonify({

            "success":False,

            "message":"Invalid file"

        }), 400 



    filename = secure_filename(
        file.filename
    )


    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        filename

    )


    file.save(filepath)



    print("\nLoading Document...\n")


    # ----------------------------
    # Build RAG Pipeline
    # ----------------------------
    rag = None
    graph = None
    
    try:

       
        rag = RAGPipeline()



        rag.ingest(
            filepath
        )

        try:
            os.remove(filepath)
        except OSError:
            pass


        rag._load_chain()



        graph = RAGGraph(

            rag.retriever,

            rag.chain

        )


        print("Document Ready")

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

    }), 500

    return jsonify({
        "success": True,
        "message": "Document indexed successfully"
    }), 200




# --------------------------------------------------
# Ask Question
# --------------------------------------------------

@app.route("/chat", methods=["POST"])

def chat():


    global graph



    if graph is None:


       return jsonify({
         "error": "Please upload document first"
       }), 400



    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid JSON"
        }), 400

    question = data.get("question")


    if not question:


       return jsonify({
            "success": False,
            "message": "Empty question"
       }), 400



    print(
        "\nQUESTION:",
        question
    )


    try:
        response = graph.invoke(question)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500



    # Send only required fields

    result = {


        "question":
        response["question"],



        "answer":
        response["answer"],



        "answer_source":
        response["answer_source"],



        "retrieval_score":
        response["retrieval_score"],



        "verified":
        response["verified"],



        "confidence":
        response["confidence"],



        "verification":
        response["verification"],



        # document evidence

        "document":
        response.get(
            "context",
            ""
        ),



        "thoughts":
        response.get(
        "thoughts",
        []
        ),


        "routing":
        response.get(
        "routing_decision",
        ""
        ),


        "tools":
        response.get(
        "tools_used",
        []
        ),



        # tools

       "wikipedia":
        response.get(
            "wiki_result",
            ""
        ),



        "tavily":
        response.get(
            "tavily_result",
            ""
        )

    }



    return jsonify(result)





# --------------------------------------------------
# Run
# --------------------------------------------------
if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            7860
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
