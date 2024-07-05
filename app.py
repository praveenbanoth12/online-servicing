from pymongo import MongoClient
from flask import Flask, render_template,url_for,redirect,request,jsonify

app = Flask(__name__) 

if __name__=="__main__":
    client = MongoClient('mongodb+srv://gajjeshivashankar:gajjeshivashankar@cluster1.yfx4emj.mongodb.net/')
    print(client)
    
    db = client['BikeService']
    details_collection = db['Details']
    bookings_collection = db['Bookings']
    feedback_collection = db['Feedback']
    cancel_collection = db['Cancellation']
   
    @app.route('/index.html')
    def index():
        return render_template('index.html')
     
    @app.route('/about.html')
    def about():
       return render_template('about.html')
   
    @app.route('/service.html')
    def service():
        return render_template('service.html')
     
    @app.route('/contact.html')
    def contact():
       return render_template('contact.html')
   
    @app.route('/feedback.html')
    def feedback():
        return render_template('feedback.html')
     
    @app.route('/bookingpage.html')
    def book():
       return render_template('bookingpage.html')
    
    @app.route('/cancellation.html')
    def cancellation():
       return render_template('cancellation.html')
    
    @app.route('/faq.html')
    def faq():
        return render_template('faq.html')
     
    @app.route('/termsandconditions.html')
    def terms():
       return render_template('termsandconditions.html')
    
    @app.route('/privacypolicy.html')
    def policy():
        return render_template('privacypolicy.html')

    @app.route('/userid.html')
    def userid():
        return render_template('userid.html')
    
    @app.route('/cancel.html') # cancel
    def cancel():
       return render_template('cancel.html')
   
    @app.route('/timeslot.html')  # timeslot
    def timeslot():
        return render_template('timeslot.html')


@app.route('/timeslot', methods=['POST'])
def timeslot1():
    
    date = request.form.get('date')
    time = request.form.get('time')
    plateno = request.form.get('plateno')
    # add uppercase to plateno 
    plateno = plateno.upper()
    
    
    details_data = details_collection.find_one({'plateno': plateno})
    
    if not details_data :
        details_collection.drop()
        sms = "please enter the correct vehicle REG no. "
        return render_template('bookingpage.html',sms=sms)
        
    plate_repeat = bookings_collection.find_one({'plateno':plateno},{'date':date})
    if plate_repeat :
        details_collection.drop()
        sms = "this vehicle is already booked on that day .."
        return render_template('bookingpage.html',sms=sms)            
    else:
        count1 = bookings_collection.count_documents({'time': "10:00 AM - 1:00 PM" ,
        'date': date })
        count2 = bookings_collection.count_documents({'time': "1:00 PM - 4:00 PM" ,
        'date': date })
        count3 = bookings_collection.count_documents({'time': "4:00 PM - 7:00 PM" ,
        'date': date })
        count4 = bookings_collection.count_documents({'time': "7:00 PM - 10:00 PM" ,
        'date': date })
        
        if time is not None and time != "" :
            if time == "10:00 AM - 1:00 PM": 
                count = count1 + 1
            elif time == "1:00 PM - 4:00 PM":
                count = count2 + 1
            elif time == "4:00 PM - 7:00 PM":
                count = count3 + 1
            elif time == "7:00 PM - 10:00 PM":
                count = count4 + 1
    
             # ID
            cleaned_date = date.replace("-", "").replace(" ", "")
            cleaned_time = time.replace("-", "").replace(" ", "").replace(":", "")
            countid = str(count)
            concat_datetime = cleaned_date + "" + cleaned_time + "" + countid
        
            booking_data = {
                'booking_id': concat_datetime,
                'name': details_data['name'],
                'vehicle_make': details_data['vehicle_make'],
                'plateno': plateno,
                'engine_cc': details_data['engine_cc'],
                'services': details_data['services'],
                'contact': details_data['contact'],
                'email': details_data['email'],
                'address': details_data['address'],
                'pincode': details_data['pincode'],
                'date': date,
                'time': time   
            }
                
            # Insert the data into details_collection
            bookings_collection.insert_one(booking_data)
            details_collection.drop()       
            return render_template('userid.html', booking_data=booking_data,id=concat_datetime)
        
        else :
            sms = "Your selected slot is full please select other slot ..! " 
            return render_template('timeslot.html',sms=sms)
        

@app.route('/time', methods=['POST'])
def timeslot2():
    
    date = request.form.get('innerFormInput')
    
    count1 = bookings_collection.count_documents({'time': "10:00 AM - 1:00 PM" ,
        'date': date })
    disable_select1 = count1 > 4
    count2 = bookings_collection.count_documents({'time': "1:00 PM - 4:00 PM" ,
        'date': date })
    disable_select2 = count2 > 4
    count3 = bookings_collection.count_documents({'time': "4:00 PM - 7:00 PM" ,
        'date': date })
    disable_select3 = count3 > 4
    count4 = bookings_collection.count_documents({'time': "7:00 PM - 10:00 PM" ,
        'date': date })
    disable_select4 = count4 > 4
    
    
    if date is not None and date != "":
        display = "display : block ;"
        return render_template('timeslot.html',date=date,disp=display,ds1=disable_select1,ds2=disable_select2,ds3=disable_select3,ds4=disable_select4)
    else :
        sms = "please select the date .."
        return render_template('timeslot.html',sms=sms)
    
@app.route('/feedback',methods=['POST'])
def feedback1():
    name=request.form.get('name')
    email=request.form.get('email')
    feed=request.form.get('feed')
    
    feedback_data = {
        'Name':name,
        'Email':email,
        'FeedBack':feed
        }

    feedback_collection.insert_one(feedback_data)
    return redirect(url_for('feedback'))


@app.route('/book', methods=['POST'])
def book1():
    # Extract form data
    vehicle_make = request.form.get('vehicle_make')
    engine_cc = request.form.get('engine_cc')
    plateno = request.form.get('plateno')
    services = request.form.getlist('services[]')
    name = request.form.get('name')
    contact = request.form.get('contact')
    email = request.form.get('email')
    address = request.form.get('address')
    pincode = request.form.get('pincode')
    # add upper case 
    plateno = plateno.upper()
    
    details_data = {
        'name': name,
        'vehicle_make': vehicle_make,
        'plateno': plateno,
        'engine_cc': engine_cc,
        'services': services,
        'contact': contact,
        'email': email,
        'address': address,
        'pincode': pincode
    }
    
    details_collection.insert_one(details_data)
    return redirect(url_for('timeslot'))
        
        
@app.route('/cancel', methods=['POST'])
def cancel1():
    
    id =request.form.get('reference')
    plateno=request.form.get('plateno')
    reason=request.form.get('reason')
    plateno = plateno.upper()
    
    booking_document = bookings_collection.find_one ({"booking_id": id},{"plateno":plateno})
    
    
    if booking_document:
        bookings_collection.delete_one({"booking_id":id})
    
        cancellation_data = {
            "Reference_Id": id,
            "vehicle_REG_no": plateno,
            "Reason": reason 
        }
       
        sms31 = " your slot is"
        sms32 = " cancelled .."
        cancel_collection.insert_one(cancellation_data)
        return render_template('cancel.html',sms31=sms31,sms32=sms32)
    else :
        sms3 = "please enter valid details or you are not booked .."
        return render_template('cancel.html',sms3=sms3)


if __name__ == '__main__':
    app.secret_key='gajjeshivashankar'
    app.run(debug=True)
