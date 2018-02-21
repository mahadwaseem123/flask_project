import re

import bleach
from chatterbot import ChatBot
from flask import Flask, request, jsonify

import url_marker

app = Flask(__name__)

chatbot = ChatBot(
    'Test ChatBot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# @app.route("/")
# def hello():
#     return render_template('chat.html')

@app.route("/train")
def train():
    chatbot.train(
        "chatterbot.corpus.english.Tickets_Chatbot",
        "chatterbot.corpus.english.conversations")
    return jsonify({'status': 'OK', 'message': 'Training Completed'})


@app.route("/ask", methods=['POST'])
def ask():
	message = request.args.get('message')
	# kernel now ready for use
	while True:
	    if message == "quit":
	        exit()
	    else:
		
		bot_response = str(chatbot.get_response(message))
		url = re.findall(url_marker.WEB_URL_REGEX,bot_response)
		if url:
			Response = bot_response.replace('(' + url[0] + ')','')
			url =  bleach.linkify(url[0])
			Response = Response.split('%%')
		
			final_response = Response[0] + '<br>' + ''.join(Response[1:]) + '<br>' + "For more information, checkout the link: " + url
		else:
			final_response = bot_response
                
	        # print bot_response
		
	        return jsonify({'status':'OK','answer':final_response})

if __name__ == "__main__":
    app.run()
