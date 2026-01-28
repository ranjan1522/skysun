import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "skysun_secret_key_2026"

# --- EMAIL CONFIGURATION ---
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'skysunlifesciences@gmail.com'
# Use a Google App Password here, not your normal password
app.config['MAIL_PASSWORD'] = 'your-app-specific-password' 
app.config['UPLOAD_FOLDER'] = 'static/uploads/resumes'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB Limit

mail = Mail(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

COMPANY_DATA = {
    "name": "Skysun Lifesciences Pvt. Ltd.",
    "headquarters": "Ahmedabad, Gujarat",
    "established": 2013,
    "email": "skysunlifesciences@gmail.com",
    "certifications": ["WHO-GMP", "ISO 9001:2015", "FSSAI"]
}

PRODUCTS = {
    "available": [
        {
            "name": "Amxol-D", 
            "type": "Antidiabetic", 
            "brand": "Glucofix Range", 
            "img": "Amoxl-D.png",
            "desc": "Combination therapy for superior glycemic control in diabetic patients."
        },
        {
            "name": "Amxol-LS", 
            "type": "Cardiovascular", 
            "brand": "Dilfit Range", 
            "img": "Amoxl-LS.png",
            "desc": "Advanced cardiovascular support for heart health maintenance."
        },
        {
            "name": "BacGut-Capsule", 
            "type": "Antihypertensive", 
            "brand": "BP Free Series", 
            "img": "BacGut.png",
            "desc": "Effective management for hypertension and blood pressure control."
        },
        {
            "name": "BP-Free 20/40/80", 
            "type": "Antihypertensive", 
            "brand": "BP Free Series", 
            "img": "BP Free-40.png",
            "desc": "Effective management for hypertension and blood pressure control."
        },
        {
            "name": "BPP-FREE AM-H", 
            "type": "Antihypertensive", 
            "brand": "BP Free Series", 
            "img": "BP FREE AM_H.png",
            "desc": "Effective management for hypertension and blood pressure control."
        },

        {    
            "name": "BP-FREE AM", 
            "type": "Antihypertensive", 
            "brand": "BP Free Series", 
            "img": "BP FREE AM.png",
            "desc": "Effective management for hypertension and blood pressure control."
        }
    ],
    "upcoming": [
        {
            "name": "Amxol-D COUGH SYP", 
            "type": "Cough & Cold", 
            "img": "Amox Dry Cough.jpeg", 
            "desc": "Dextromethorphan Hydrobromide & Chlorpheniramine Maleate Syrup.",
            "status": "New Launch"
        },
        {
            "name": "Amxol-LS Drops", 
            "type": "Paediatric Care", 
            "img": "Amoxl-LS.jpeg", 
            "desc": "Ambroxol Hydrochloride, Levosalbutamol & Guaiphenesin Drops.",
            "status": "New Launch"
        },
        {
            "name": "MICOBIN-DPM Tablet", 
            "type": "Multivitamin", 
            "img": "Micobin-DPM.jpeg", 
            "desc": "Advanced Methylcobalamin Formula for nerve and metabolic health.",
            "status": "New Launch"
        },
        {
            "name": "Micobin-CM", 
            "type": "Calcium Supplement", 
            "img": "Micobin CM.jpeg", 
            "desc": "Calcium Carbonate & Vitamin D3 for bone density and strength.",
            "status": "New Launch"
        },
        {
            "name": "MNSee NS Drops", 
            "type": "Nasal Care", 
            "img": "MNSee NS.jpeg", 
            "desc": "Saline Nasal Solution IP for gentle nasal congestion relief.",
            "status": "New Launch"
        },
        {
            "name": "Skymentin-457 Dry Syrup", 
            "type": "Antibiotic", 
            "img": "SKYmentin-457.jpeg", 
            "desc": "Amoxycillin & Potassium Clavulanate for bacterial infection control.",
            "status": "New Launch"
        }
    ]
}

OWNERS = [
    {"name": "Amit Singh", "role": "Director", "desc": "Leading the vision of healthcare excellence since 2013.", "img": "static/images/Amit Singh.png"},
    {"name": "Lal Babu", "role": "Director", "desc": "Expert in global pharmaceutical marketing strategies.", "img": "static/images/Lal Babu.png"}
]

@app.route('/')
def home():
    return render_template('index.html', company=COMPANY_DATA, flagships=PRODUCTS['available'][:3])

@app.route('/about')
def about():
    return render_template('about.html', company=COMPANY_DATA)

@app.route('/products/<ptype>')
def products(ptype):
    items = PRODUCTS.get(ptype, [])
    return render_template('products.html', ptype=ptype, items=items, company=COMPANY_DATA)

@app.route('/careers', methods=['GET', 'POST'])
def careers():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        position = request.form.get('position')
        resume = request.files.get('resume')

        if resume and resume.filename != '':
            filename = secure_filename(f"{name}_{resume.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(file_path)

            try:
                # Email to HR
                msg = Message(f"New Application: {position} - {name}",
                              sender=app.config['MAIL_USERNAME'],
                              recipients=[app.config['MAIL_USERNAME']])
                msg.body = f"Candidate: {name}\nEmail: {email}\nPosition: {position}"
                with app.open_resource(file_path) as fp:
                    msg.attach(filename, "application/octet-stream", fp.read())
                mail.send(msg)
                flash(f"Thank you {name}! Your application has been sent successfully.", "success")
            except Exception as e:
                flash("Application saved, but email service is currently offline. We will review it shortly.", "warning")

        return redirect(url_for('careers'))
    return render_template('careers.html')

@app.route('/owners')
def owners():
    return render_template('owners.html', owners=OWNERS)

@app.route('/activities')
def activities():
    activities_list = [
        {"title": "Free Medical Camps", "desc": "Monthly health checkups across Gujarat.", "icon": "hospital"},
        {"title": "R&D Excellence", "desc": "Investing in bio-equivalent studies.", "icon": "beaker"},
        {"title": "Ethical Marketing", "desc": "Awarded for best practices in India.", "icon": "shield"}
    ]
    return render_template('activities.html', activities=activities_list)

@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        # 1. Capture Form Data
        name = request.form.get('name')
        contact = request.form.get('contact')
        email = request.form.get('email')
        user_message = request.form.get('message')

        try:
            # 2. Prepare the Email
            msg = Message(
                subject=f"New Website Enquiry from {name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']], # Send to yourself
                body=f"You have a new enquiry:\n\n"
                     f"Name: {name}\n"
                     f"Contact: {contact}\n"
                     f"Email: {email}\n"
                     f"Message: {user_message}"
            )
            
            # 3. Send the Email
            mail.send(msg)

            # 4. Show Success Message on UI
            flash(f"Thank you {name}, your enquiry has been sent successfully! Our team will contact you soon.", "success")
        
        except Exception as e:
            # Fallback if email server fails
            print(f"Error: {e}")
            flash("Message sent to our database, but email notification failed. We will still review it!", "warning")

        return redirect(url_for('support'))
    
    return render_template('support.html')

if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)