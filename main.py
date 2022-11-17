from flask import Flask,render_template,request
import http.client
import json


app=Flask(__name__)

conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

headers = {
        'X-RapidAPI-Key': "f44a051006msh4760537df13eceap164869jsnd1fc47d135ce",
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
    #return render_template('index.html')
    search=search.replace(" ","%20")
    conn.request("GET",f"/title/v2/find?title={search}&limit=20&sortArg=moviemeter%2Casc", headers=headers)
    res = conn.getresponse()
    data = res.read()
    datad =json.loads(data)
    print(data)
    respo=data.decode("utf-8")
    y = json.loads(respo)
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