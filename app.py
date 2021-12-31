from flask import Flask,render_template,request
import os
import pandas 

import csv
import glob
import zipfile
#import pyrebase
from os.path import basename
from flask import jsonify 
app = Flask(__name__,template_folder='Templates')
app.static_url_path = app.config.get('STATIC_FOLDER')
from nltk import word_tokenize
from simplet5 import SimpleT5

app.static_folder = app.root_path + app.static_url_path






config={
  "apiKey": "AIzaSyD2Kc5Vu_ZvRq0wqffWfo7Y8QytJNTdnFA",
  "authDomain": "address-normalization-1979b.firebaseapp.com",
  "projectId": "address-normalization-1979b",
  "storageBucket": "address-normalization-1979b.appspot.com",
  "messagingSenderId": "58619810635",
  "appId": "1:58619810635:web:5265955af2a30fcf470ece",
  "measurementId": "${config.measurementId}",
  "databaseURL":""

}
firebase=pyrebase.initialize_app(config)
sotrage=firebase.storage()

@app.route("/upload_file",methods=["GET","POST"])
def upload_file():
    if request.method == 'POST':
        fi=[]
        for f in request.files.getlist('file_name'):
        
                

                folpath = 'static/'
                s = []

            
                hj1 = f.filename.split(".")[0]
                
                if f.filename[-3:] == "csv":
                    dg = []
                    data = pd.read_csv(f,index_col=None)
                    #print(data.head())
                    data = data.rename(columns={data.columns[0]: 'Standard Streets'})
                    conv1 = data['Standard Streets'].tolist()
                    c = []

                    for i in conv1:
                        model = SimpleT5()
                        model.from_pretrained(model_type="t5",model_name="t5-base")
                        model.load_model('t5','gs://address-normalization-1979b.appspot.com/static/rename12simplet5-epoch-0-train-loss-0.0698',use_gpu=False)
                        finalresult = model.predict(i)

                        
                        
                        #c.append(finalresult)
                        dg.append(finalresult)
                    df = pd.DataFrame(dg)
                    print(df,"ddfff")
                    df.to_csv(f.filename+"_finalresult.csv",index=False,header=False)
                    fi.append(f.filename+'_finalresult.csv')
                    # sotrage.child(f.filename).put()
                        
                   
                    
                elif f.filename[-4:]=="json":
                    cg = []
                    data = pd.read_json(f)
                    #print(data)
                    
                    data = data.rename(columns={data.columns[0]: 'Standard Streets'})
                    conv1 = data['Standard Streets'].tolist()
                    c= []
                    for i in conv1:
                        model = SimpleT5()
                        model.from_pretrained(model_type="t5",model_name="t5-base")
                        model.load_model('t5','gs://address-normalization-1979b.appspot.com/static/rename12simplet5-epoch-0-train-loss-0.0698',use_gpu=False)

                        finalresult = model.predict(i)
                        
                        
                        

                        cg.append(finalresult)
                    df = pd.DataFrame(cg)
                    
                    df.to_json(f.filename+"_finalresultjson.json",orient='records',lines=True)
                    fi.append(f.filename+"_finalresultjson.json")
                      
                    #print((cg))
                        

                    #print(data.head())
                elif f.filename[-3:] == "xml":
                    eg = []
                    data = pd.read_xml(f)
                    data = data.rename(columns={data.columns[0]: 'Standard Streets'})
                    conv1 = data['Standard Streets'].tolist()
                    c = []
                    
                    for i in conv1:
                        #print(i)
                        model = SimpleT5()
                        model.from_pretrained(model_type="t5",model_name="t5-base")
                        model.load_model('t5','static/outputs/simplet5-epoch-0-train-loss-0.1425',use_gpu=False)

                        finalresult = model.predict(i)

                        eg.append(finalresult)
                    df = pd.DataFrame(eg,columns=['x'])
                    
                    
                    df.to_xml(f.filename+"_finalresultxml.xml")
                    fi.append(f.filename+"_finalresultxml.xml")

                folspath = 'static/'
                sss=  []

                for fspath in glob.glob("{0}/*".format(folspath),recursive=True):
    
                    print(fspath,'hai')
                    sss.append(fspath)
                print(sss,'haiiii')

                with zipfile.ZipFile('rr.zip', 'w') as zipF:
                    for file in fi:
                        zipF.write(file,compress_type=zipfile.ZIP_DEFLATED)
                print(zipF,'hai')
                sotrage.child('files.zip').put('rr.zip')
                ll=sotrage.child('files.zip').get_url('')
                
                

                        
                    #print((eg))



    # write the header
    # writer.writerow(header)

    # write multiple rows
                #writer.writerow(finalresult)
        
        # print(sotrage.child('zip').get_url())
        return render_template("upload-files.html",msg="Files has been uploaded sucessfully",ll=ll)
    return render_template("upload-files.html",msg="Please Choose a files")
    #return jsonify({"msg":"Files has been uploaded sucessfully","ll":'static/final.zip'})



if __name__== '__main__':
    app.run(debug=True)


# apiKey: "AIzaSyD1R6J8eAFBZ59vmqC2HKsKJJoX_OaexJ4",
#   authDomain: "filestorage-2ff36.firebaseapp.com",
#   projectId: "filestorage-2ff36",
#   storageBucket: "filestorage-2ff36.appspot.com",
#   messagingSenderId: "593499132447",
#   appId: "1:593499132447:web:3e3bffab7d1ced08d57b2a",
#   measurementId: "${config.measurementId}"



app.route("/downloadfile/<path:filename>", methods = ['GET'])
def download_file(filename):
    print(filename)
    return render_template('files.html',value=filename)

if __name__== '__main__':
    app.run(debug=True)


