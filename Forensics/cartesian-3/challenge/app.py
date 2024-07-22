from flask import Flask, render_template, request

app = Flask(__name__)

FLAG = open("flag.txt").read().strip()

# Example questions and answers (replace with your actual questions and answers)
questions_answers = {
    "email": "terrencedescartes@gmail.com",
    "birthday": "2001-01-18",
    "pet": "Bonnie",
    "city_last_three_months": "San Diego",
    "city_grow_up": "Phoenix",
    "poet": "Robert Frost",
    "first_car": "Honda Civic",
    "father_birth_year": "1981",
    "mother_maiden_name": "Jackson",
    "company": "Cohort Calculations",
    "city_last_summer_vacation": "Saint Paul",
    "August_21_activity": "Drop off top secret information",
    "first_job_boss": "Farmer Johnson"
}

for n in questions_answers.keys():
  questions_answers[n] = questions_answers[n].lower()

@app.route('/', methods=['GET', 'POST'])
def password_reset():
    error_messages = {}
    
    if request.method == 'POST':
        request.form = dict(request.form)

        for n in request.form.keys():
                request.form[n] = request.form[n].lower().strip()

        # Retrieve form data
        email = request.form['email']
        birthday = request.form['birthday']
        pet = request.form['pet']
        city_last_three_months = request.form['city_last_three_months']
        city_grow_up = request.form['city_grow_up']
        poet = request.form['poet']
        first_car = request.form['first_car']
        father_birth_year = request.form['father_birth_year']
        mother_maiden_name = request.form['mother_maiden_name']
        company = request.form['company']
        city_last_summer_vacation = request.form['city_last_summer_vacation']
        August_21_activity = request.form['August_21_activity']
        first_job_boss = request.form['first_job_boss']

        # Check answers against stored answers and collect errors
        if email != questions_answers['email']:
            error_messages['email'] = 'Incorrect email.'
        if birthday != questions_answers['birthday']:
            error_messages['birthday'] = 'Incorrect birthday.'
        if pet != questions_answers['pet']:
            error_messages['pet'] = 'Incorrect pet name.'
        if city_last_three_months != questions_answers['city_last_three_months']:
            error_messages['city_last_three_months'] = 'Incorrect city last three months.'
        if city_grow_up != questions_answers['city_grow_up']:
            error_messages['city_grow_up'] = 'Incorrect city grown up in.'
        if poet != questions_answers['poet']:
            error_messages['poet'] = 'Incorrect favorite poet.'
        if first_car != questions_answers['first_car']:
            error_messages['first_car'] = 'Incorrect first car make.'
        if father_birth_year != questions_answers['father_birth_year']:
            error_messages['father_birth_year'] = 'Incorrect father birth year.'
        if mother_maiden_name != questions_answers['mother_maiden_name']:
            error_messages['mother_maiden_name'] = 'Incorrect mother maiden name.'
        if company != questions_answers['company']:
            error_messages['company'] = 'Incorrect company name.'
        if city_last_summer_vacation != questions_answers['city_last_summer_vacation']:
            error_messages['city_last_summer_vacation'] = 'Incorrect city last summer vacation.'
        if August_21_activity != questions_answers['August_21_activity']:
            error_messages['August_21_activity'] = 'Incorrect activity on August 21.'
        if first_job_boss != questions_answers['first_job_boss']:
            error_messages['first_job_boss'] = 'Incorrect first job boss.'

        # If there are no error messages, all answers are correct
        if not error_messages:
            return render_template('success.html', flag=FLAG)

    return render_template('password_reset.html', error_messages=error_messages)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
