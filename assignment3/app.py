import sys
import csv
from jinja2 import Template
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) != 3:
        generate_error_html()
        return

    option = sys.argv[1]
    identifier = sys.argv[2]

    data = []
    try:
        with open('data.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stripped_row = {k.strip(): v.strip() for k, v in row.items()}
                data.append(stripped_row)
    except FileNotFoundError:
        generate_error_html()
        return

    if option == '-s':
        student_id = identifier
        student_rows = [row for row in data if row.get('Student id') == student_id]
        if not student_rows:
            generate_error_html()
        else:
            try:
                total_marks = sum(int(row['Marks']) for row in student_rows)
            except ValueError:
                generate_error_html()
                return
            generate_student_html(student_rows, total_marks)
    elif option == '-c':
        course_id = identifier
        course_rows = [row for row in data if row.get('Course id') == course_id]
        if not course_rows:
            generate_error_html()
        else:
            try:
                marks = [int(row['Marks']) for row in course_rows]
            except ValueError:
                generate_error_html()
                return
            average = round(sum(marks) / len(marks), 1)
            maximum = max(marks)
            generate_course_html(average, maximum)
            generate_histogram(marks)
    else:
        generate_error_html()

def generate_error_html():
    template = Template('''<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
</head>
<body>
    <h1>Something went wrong</h1>
</body>
</html>''')
    with open('output.html', 'w') as f:
        f.write(template.render())

def generate_student_html(rows, total):
    template = Template('''<!DOCTYPE html>
<html>
<head>
    <title>Student Details</title>
</head>
<body>
    <h1>Student Details</h1>
    <table border="1">
        <tr>
            <th>Student ID</th>
            <th>Course ID</th>
            <th>Marks</th>
        </tr>
        {% for row in rows %}
        <tr>
            <td>{{ row['Student id'] }}</td>
            <td>{{ row['Course id'] }}</td>
            <td>{{ row['Marks'] }}</td>
        </tr>
        {% endfor %}
        <tr>
            <td><strong>Total Marks</strong></td>
            <td></td>
            <td><strong>{{ total }}</strong></td>
        </tr>
    </table>
</body>
</html>''')
    html = template.render(rows=rows, total=total)
    with open('output.html', 'w') as f:
        f.write(html)

def generate_course_html(average, maximum):
    template = Template('''<!DOCTYPE html>
<html>
<head>
    <title>Course Details</title>
</head>
<body>
    <h1>Course Details</h1>
    <table border="1">
        <tr>
            <th>Average Marks</th>
            <th>Maximum Marks</th>
        </tr>
        <tr>
            <td>{{ average }}</td>
            <td>{{ maximum }}</td>
        </tr>
    </table>
    <img src="histogram.png" alt="Marks Histogram">
</body>
</html>''')
    html = template.render(average=average, maximum=maximum)
    with open('output.html', 'w') as f:
        f.write(html)

def generate_histogram(marks):
    plt.clf()
    plt.hist(marks, bins=10, edgecolor='black', range=(0, 100))
    plt.xlabel('Marks')
    plt.ylabel('Number of Students')
    plt.title('Marks Distribution')
    plt.savefig('histogram.png')
    plt.close()

if __name__ == '__main__':
    main()