from flask import Flask, jsonify, request
import crawler

app = Flask(__name__) 

@app.route("/crawl-all")
def events():
    print("service api receive airflow message !!!")

    try:
        crawler.crawl_all()
    except:
        print("crawl errr")

    return jsonify("done task")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
