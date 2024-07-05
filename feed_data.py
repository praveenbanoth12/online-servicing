from flask import Flask,render_template,redirect,request,url_for
from pymongo import MongoClient

app=Flask(__name__)

if __name__=="__main__":
    print("this is feedback form data") 
    client=MongoClient('mongodb+srv://gajjeshivashankar:gajjeshivashankar@cluster1.yfx4emj.mongodb.net/')
    
    db=client['BikeService']
    collect=db['feedback']

    @app.route('/feedback.html')
    def feedback():
        return render_template('feedback.html')

@app.route('/feedback',methods=['POST'])
def feedback():
    name=request.form.get('name')
    email=request.form.get('email')
    feed=request.form.get('feed')
    
    feedback_data = {
        'Name':name,
        'Email':email,
        'FeedBack':feed
        }

    collect.insert_one(feedback_data)

    return redirect(url_for('feedback'))

if __name__ == '__main__':
    app.secret_key='gajjeshivashankar'
    app.run(debug=True)
