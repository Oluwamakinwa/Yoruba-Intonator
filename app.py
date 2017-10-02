from flask import Flask, render_template 
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired
from wtforms.widgets import TextArea

from flask_bootstrap import Bootstrap
import viterbi

app = Flask(__name__)
app.config['SECRET_KEY']= 'THIS IS A SECRET!'
bootstrap = Bootstrap(app)


class LoginForm(FlaskForm):
	unmarked_yoruba = StringField('Unmarked Yoruba: ', validators=[InputRequired()],  widget=TextArea())

@app.route('/', methods=['GET', 'POST'])
def form():
	form = LoginForm()

	if form.validate_on_submit():
		translated_sentence = viterbi.get_most_likely_sentence_markings(form.unmarked_yoruba.data)
		unable_to_translate = form.unmarked_yoruba.data == translated_sentence
		if unable_to_translate:
			import os
			filename = 'untranslatable.txt'

			if os.path.exists(filename):
			    append_write = 'a' # append if already exists
			else:
			    append_write = 'w' # make a new file if not

			highscore = open(filename,append_write)
			highscore.write(translated_sentence + '\n')
			highscore.close()

		response = "<h1>Sorry, I was unable to translate:</h1>" if unable_to_translate else "<h1> The translated version is:</h1>"
		#log words you can't mark

		return '{}<br/> {} <a href=''><br/>Translate more </a>'.format(response, translated_sentence)

	return render_template('form.html', form=form)

@app.route('/untranslated', methods=['GET', 'POST'])
def untranslated():
	untranslated_sentences = open("untranslatable.txt",'r')
	result = ""
	for line in untranslated_sentences:
		result+=line
	return result

if __name__ == '__main__':
	app.run(debug=True)
