from flask import Flask,render_template,request
import requests
import http.client
import json
import ast



app=Flask(__name__)                 

conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

# print(conn)
# exit()
headers = {
        'X-RapidAPI-Key': "6f91d524dbmsh4299d3e3f862357p1cfce2jsnaed2bfed6cf8",
        'X-RapidAPI-Host': "imdb8.p.rapidapi.com"
        }

def getDetails(full_data):
    lis=[]
    print("coming")
    full_data = json.loads(full_data)
    for x in full_data:
        conn.request("GET", "/title/get-details?tconst="+x['id'], headers=headers)
        resd = conn.getresponse()
        datad = resd.read()
        lis.append(json.loads(datad))

    return lis

@app.route('/',methods=['GET','POST'])
def home():
    search=request.args.get('search')
    #return f"d/title/v2/find?title={search}&limit=20&sortArg=moviemeter%2Casc"
    #return "/title/v2/find?title="+search+"&limit=20&sortArg=moviemeter%2Casc"
    
    search=search.replace(" ","%20")
    conn.request("GET",f"/title/v2/find?title={search}&limit=20&sortArg=moviemeter%2Casc", headers=headers)
    res = conn.getresponse()
    data = res.read()
    #print(type(datad))
    datad =json.loads(data)
    
    #print(type(respo))
    #y = json.loads(respo)
    try:
        return render_template('index.html',data=datad["results"],search=search)
    except KeyError:
        return render_template('index.html')
    
        


@app.route('/reg',methods=['GET','POST'])
def reg():
    us=request.form['da']
    return render_template('index.html',data=range(int(us)))


if __name__=='__main__':
    app.run(debug=True)