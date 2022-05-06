from flask import Flask, render_template, request, redirect, url_for, session
import boolean_model as n
import Extended_boolean as ex
import VSMmodel as v
import boolean_model_arabic as an 
import extended_boolean_arabic as aex
import VSM_arabic as av 
import sqlite3
import pandas as pd

app = Flask(__name__)
app.secret_key = "#$%#$%^%^BFGBFGBSFGNSGJTNADFHH@#%$%#T#FFWF$^F@$F#$FW"


@app.route("/")
def index():
	
	return render_template("index.html")



@app.route("/search", methods=["POST", "GET"])
def searchr():
	global df
	global different_words
	if request.method == "POST":
		query = request.form["query"]
		mod= request.form["models"]
		lan= request.form["lang"]
		q1= []
		q1.append(query)
		q1= q1[0].split()
		print(q1)
		if str(mod).lower()== "boolean" and str(lan).lower()=='english':
			results = n.srch(query)
		elif str(mod).lower()== "exbool" and str(lan).lower()=='english':
			results = ex.srch(query)
		elif str(mod).lower()== "vsm" and str(lan).lower()=='english':
			results = v.vsearch(query)
		if str(mod).lower()== "boolean" and str(lan).lower()=='arabic':
			results = an.srch(query)
		elif str(mod).lower()== "exbool" and str(lan).lower()=='arabic':
			results = aex.srch(query)
		elif str(mod).lower()== "vsm" and str(lan).lower()=='arabic':
			results = av.vsearch(query)
		
		conn= sqlite3.connect("C:\sqllite\gui\SQLiteStudio\QandA")
		data=[]
		rows=[]
		for i in results:
			cnt=1
			print(i)
			conn.row_factory= sqlite3.Row
			cur=conn.cursor()
			if str(lan).lower()=='english':
				rows.append(cur.execute("select id,answer from English where id=?",(int(i),))) 
				rows= cur.fetchall()
			elif str(lan).lower()=='arabic':
				rows.append(cur.execute("select id,aswer from arabic where id=?",(int(i),))) 
				rows= cur.fetchall()
			for row in rows:
				data.append(list(row))
			cnt= cnt+1
		print(data)	
		print('len of q1 is '+str(len(q1)))	
		df= pd.DataFrame(data,columns=['id','answer'])
		def h(row):
			text= row
			#ext= row['existing']
			
			for idx, word in enumerate(q1):
				color={
					word: 'red'
				}
				for k,v in color.items():
					text = text.replace(k, word.upper())
					print(text)
					
			
			return text
		df['answer']= df['answer'].apply(h)
		print("done")
		session["data"] = data
		session["query"] = query
		
		return redirect(url_for("searchr"))
	return render_template("search.html", column_names=df.columns.values, row_data=list(df.values.tolist()),
                           link_column="id", zip=zip, query=session["query"])
@app.route('/add',methods=['POST','GET'])
def add():
	if request.method=='POST':
		question= str(request.form["question"])
		answer= str(request.form["answer"])
		lan= request.form["lang"]
		conn= sqlite3.connect("C:\sqllite\gui\SQLiteStudio\QandA")
		
		if str(lan).lower()=='english':
			c= conn.cursor()
			c.execute("INSERT INTO English (question,answer) VALUES (?,?)" ,(question,answer,))
			conn.commit()
			print("done")
		if str(lan).lower()=='arabic':
			c= conn.cursor()
			c.execute("INSERT INTO arabic (question,aswer) VALUES (?,?)", (question,answer,))
			conn.commit()
			print("done")
		return redirect(url_for('add'))
	return render_template('add.html')


if __name__ == '__main__':
	app.run(debug=True)