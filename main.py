from flask import Flask,jsonify,request
app = Flask(__name__)
from agent import github_agent_query
@app.route("/chat",methods=["POST"])
def send_chat():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error":"Prompt required"}),400
    
    response = github_agent_query(prompt)
    return jsonify({"Response":response})


if __name__=="__main__":
    app.run(debug=True,port=5000)