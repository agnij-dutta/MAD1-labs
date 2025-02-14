from flask import Flask, render_template, request, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
# Read CSV with skipinitialspace to handle leading spaces in headers
df = pd.read_csv('data.csv', skipinitialspace=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'ID' not in request.form:
            return render_template('error.html', message='Please select Student ID or Course ID.')
        id_type = request.form['ID']
        id_value = request.form.get('id_value', '').strip()
        
        if not id_value:
            return render_template('error.html', message='ID value is required.')
        
        try:
            id_num = int(id_value)
        except ValueError:
            return render_template('error.html', message='Invalid ID. Must be a number.')
        
        if id_type == 'student_id':
            student_data = df[df['Student id'] == id_num]
            if student_data.empty:
                return render_template('error.html', message=f'Student ID {id_num} not found.')
            total = student_data['Marks'].sum()
            return render_template('student_details.html', student_id=id_num, details=student_data.to_dict('records'), total=total)
        
        elif id_type == 'course_id':
            course_data = df[df['Course id'] == id_num]
            if course_data.empty:
                return render_template('error.html', message=f'Course ID {id_num} not found.')
            average = round(course_data['Marks'].mean(), 2)
            maximum = course_data['Marks'].max()
            
            plt.figure()
            plt.hist(course_data['Marks'], bins=10, edgecolor='black')
            plt.xlabel('Marks')
            plt.ylabel('Frequency')
            plt.title(f'Histogram for Course {id_num}')
            
            static_dir = os.path.join(app.root_path, 'static')
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
            
            plot_filename = f'histogram_{id_num}.png'
            plt.savefig(os.path.join(static_dir, plot_filename))
            plt.close()
            
            return render_template('course_details.html', course_id=id_num, average=average, maximum=maximum, plot_filename=plot_filename)
        
        else:
            return render_template('error.html', message='Invalid ID type selected.')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run()