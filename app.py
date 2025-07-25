from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))
tfidf_vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))

def detect(input_text):
    vectorized_text = tfidf_vectorizer.transform([input_text])
    result = model.predict(vectorized_text)
    return "Plagiarism Detected" if result[0] == 1 else "No Plagiarism Detected"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    status = None
    if request.method == 'POST':
        input_text = request.form['text']
        result = detect(input_text)
        status = 'plagiarism' if result == "Plagiarism Detected" else 'no_plagiarism'
    return render_template('index.html', result=result, status=status)

if __name__ == "__main__":
    app.run(debug=True)
