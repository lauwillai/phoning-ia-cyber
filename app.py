from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    response.play('https://YOUR_AUDIO_LINK.mp3')  # <<< Mets ici ton lien ElevenLabs MP3
    gather = Gather(input='speech', action='/analyze', timeout=5)
    gather.say('Si vous êtes intéressé, dites oui après le bip.')
    response.append(gather)
    return Response(str(response), mimetype='application/xml')

@app.route("/analyze", methods=['GET', 'POST'])
def analyze():
    transcription = request.values.get('SpeechResult')
    print(f"Réponse prospect: {transcription}")

    prompt = f"Analyse cette réponse: '{transcription}'. Est-ce que la personne est intéressée par un rendez-vous en cybersécurité ? Réponds uniquement par OUI ou NON."
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    decision = completion['choices'][0]['message']['content']
    print(f"Décision IA: {decision}")

    response = VoiceResponse()
    if "OUI" in decision.upper():
        response.say("Merci beaucoup, nous allons organiser un rendez-vous.")
    else:
        response.say("Merci pour votre temps, excellente journée.")

    return Response(str(response), mimetype='application/xml')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
