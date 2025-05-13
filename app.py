from flask import Flask, render_template, request, redirect
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)

# Connect to DynamoDB using IAM role (recommended) or credentials
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')  # Update region if needed
table = dynamodb.Table('submissions')  # Your table name

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')

        if name and email:
            try:
                table.put_item(
                    Item={
                        'name': name,    # partition key
                        'email': email   # regular attribute
                    }
                )
                return redirect('/success')
            except ClientError as e:
                return f"Error: {e.response['Error']['Message']}"

    return render_template('form.html')

@app.route('/success')
def success():
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # host=0.0.0.0 makes it accessible from EC2 public IP
