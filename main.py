from flask import Flask, request, jsonify
import openai
openai.api_key = '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'

def listing(title):
    response1 = openai.Completion.create(
        model="text-davinci-003",
        prompt='''Given the image caption as: {}.\n\nCan you generate a product title for me?'''.format(title),
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6)
    
    response2 = openai.Completion.create(
        model="text-davinci-003",
        prompt='''Given the product title: {}.\n\nCan you create an Amazon product listing with bullet points and description.'''.format(response1.choices[0].text),
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6)
    
    return response1.choices[0].text, response2.choices[0].text

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            text = request.args.get('name')
            t1, t2 = listing(text)
            data = {"prediction": t1 + '\n\n' + t2}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    app.run(debug=True)