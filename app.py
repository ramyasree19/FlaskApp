from flask import Flask
import os
from redis import Redis
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)
redisDb = Redis(host=os.getenv('HOST') , port=os.getenv('PORT'))

#visitor_count = 0

@app.route('/')

def welcome():
	redisDb.incr('visitor_count')
	visitor_count= str(redisDb.get('visitor_count'), 'utf-8')
	return "Welcome, Hello World! Visitor Count: "+ visitor_count


if __name__ == '__main__':
	app.run(host="0.0.0.0" , port=8000, debug=True)

