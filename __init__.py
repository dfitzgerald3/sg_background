from flask import Flask, render_template
import MySQLdb
import mysqldb as connection
import datetime



app = Flask(__name__)



@app.route('/')
def homepage():
    c, conn = connection.connection()
    
    c.execute("SELECT * FROM sentiment WHERE symbol = 'xom'")
    
    data = c.fetchall()
    
    sentiment = []
    
    for i in data:
        array = []
        array.append(i[0])
        array.append(i[1])
        array.append(datetime.datetime.fromtimestamp(int(i[2])).strftime('%Y-%m-%d %H:%M'))
        
        sentiment.append(array)
        
#    return jsonify(str(sent))
    return render_template("main.html", 
                           sentiment=sentiment)

if __name__ == "__main__":
    app.run()