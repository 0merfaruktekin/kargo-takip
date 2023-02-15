from flask import Flask, render_template, url_for,request,url_for,redirect
import sqlite3
app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def index():
   if request.method=='POST':
      kargo_id=request.form['id']
      try:
         db=sqlite3.connect("kargo.db")
         imlec=db.cursor()
         imlec.execute("SELECT * FROM kargo WHERE id = "+kargo_id+";")
         veriler=imlec.fetchall()
         return render_template('table.html' , veriler=veriler)
      except:
         return("Yanlış id girdiniz<br><a href='/'>Ana sayfa</a>")
   else:
      return render_template('index.html')

@app.route("/musteri", methods=["POST","GET"])
def musteri_login():
   if request.method=='POST':
      m_id=request.form['musteri_id']
      m_pass=request.form['musteri_pass']
      try:
         db=sqlite3.connect("kargo.db")
         imlec=db.cursor()
         komut="SELECT id,sifre FROM musteri WHERE id= "+m_id+";"
         imlec.execute(komut)
         sifre=imlec.fetchall()[0][1]
         imlec.execute("SELECT * FROM kargo WHERE gonderen= "+m_id+";")
         veriler=imlec.fetchall()
         if sifre==m_pass:
            return render_template('musteri_tablo.html',veriler=veriler)
         else:
            return redirect("/")
      except:
         return "hata oldu"
   else:
      return render_template("musteri_giris.html")

@app.route("/kurye", methods=["POST","GET"])
def kurye_login():
   if request.method=='POST':
      k_id=request.form['kurye_id']
      k_pass=request.form['kurye_pass']
      try:
         db=sqlite3.connect("kargo.db")
         imlec=db.cursor()
         komut="SELECT id,sifre FROM kurye WHERE id= "+k_id+";"
         imlec.execute(komut)
         sifre=imlec.fetchall()[0][1]
         imlec.execute("SELECT * FROM kargo WHERE kurye= "+k_id+";")
         veriler=imlec.fetchall()
         if sifre==k_pass:
            return render_template("kurye_panel.html",veriler=veriler)
         else:
            return redirect("/")
      except:
         return "hata oldu"
   else:
      return render_template('kurye_giris.html')
@app.route("/kurye/<int:id>")
def teslim(id):
   db=sqlite3.connect("kargo.db")
   imlec=db.cursor()
   komut="UPDATE kargo SET durum = 'Teslim Edildi' WHERE kurye = "+ str(id)+";"
   imlec.execute(komut)
   db.commit()
   return redirect("/kurye")
   
@app.route("/yonetici", methods=["POST","GET"])
def yonetici_login():
   if request.method=='POST':
      y_id=request.form['yonetici_id']
      y_pass=request.form['yonetici_pass']
      try:
         db=sqlite3.connect("kargo.db")
         imlec=db.cursor()
         imlec.execute("SELECT id,sifre,sube FROM yonetici WHERE id= "+y_id+";")
         asd=imlec.fetchall()
         sifre=asd[0][1]
         sube=asd[0][2]
         imlec.execute("SELECT * FROM kargo WHERE sube= '"+sube+"';")
         veriler=imlec.fetchall()
         if sifre==y_pass:
            return render_template("yonetici_panel.html",veriler=veriler)
         else:
            return redirect("/")
      except:
         return "Hata"
   else:
      return render_template("yonetici_giris.html")
@app.route("/yonetici/<sube>",methods=["POST","GET"])
def ekle(sube):
   if request.method=='POST':
      m_id=request.form['musteri_id']
      alici=request.form['alici']
      kurye=request.form["kurye_id"]
      db=sqlite3.connect("kargo.db")
      imlec=db.cursor()
      komut="INSERT INTO kargo Values(NULL,"+m_id+",'Kuryede','"+alici+"','"+sube+"',"+kurye+")"
      imlec.execute(komut)
      db.commit()
      return redirect("/yonetici")
   else:
      return render_template("ekle.html",sube=sube)
if __name__=="__main__":
   app.run(debug=True)
@app.route('/kurye/panel',methods=['POST','GET'])
def kurye():
   return render_template(kurye)