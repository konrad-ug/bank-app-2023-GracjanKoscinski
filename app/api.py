from flask import Flask, request, jsonify
from .RegisterOfAccounts import RegisterOfAccounts
from .KontoOsobiste import KontoOsobiste
from .Konto import Konto
app = Flask(__name__)


@app.route("/api/accounts", methods=['POST'])
def stworz_konto():
   dane = request.get_json()
   print(f"Request o stworzenie konta z danymi: {dane}")
   # jezeli takiego konta nie ma
   czyPeselWykorzystany = RegisterOfAccounts.searchByPesel(dane["pesel"])
   if czyPeselWykorzystany == None:
      konto = KontoOsobiste(dane["imie"], dane["nazwisko"], dane["pesel"])
      RegisterOfAccounts.addToRegister(konto)
      return jsonify({"message": "Konto stworzone"}), 201
   else:
      return jsonify({"message": "Ten numer PESEL został już wykorzystany"}), 409


@app.route("/api/accounts/count", methods=['GET'])
def ile_kont():
   count = RegisterOfAccounts.howManyAccounts()
   return jsonify({"count":count}), 200


@app.route("/api/accounts/<pesel>", methods=['GET'])
def wyszukaj_konto_z_peselem(pesel):
   konto = RegisterOfAccounts.searchByPesel(pesel)
   if konto != None:
      return jsonify(konto.__dict__), 200
   else:
      return jsonify({"message":"Nie ma konta o takim peselu"}), 404


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def usun_konto(pesel):
   konto = RegisterOfAccounts.searchByPesel(pesel)
   if konto is not None:
      RegisterOfAccounts.register.remove(konto)
      return jsonify({"message":"Usunięto konto"}), 200
   else:
      return jsonify({"message":"Brak konta o takim peselu!"}), 404
   

@app.route("/api/accounts/<pesel>", methods=["PATCH"])
def zmodyfikuj_dane(pesel):
   konto = RegisterOfAccounts.searchByPesel(pesel)
   if konto is not None:
      request_data = request.get_json()
      for key, value in request_data.items():
         if hasattr(konto, key):
               setattr(konto, key, value)
      return jsonify({"message": "Dane konta zaktualizowane"}), 200
   else:
        return jsonify({"message": "Brak konta o takim peselu!"}), 404
#przelwy
@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def przelew(pesel):
   konto = RegisterOfAccounts.searchByPesel(pesel)
   dane = request.get_json()
   if konto is None:
       return jsonify({"message":"Nie znaleziono konta docelowego"}), 404
   if dane["type"] == "incoming":
      konto.przelew_przychodzacy(dane["amount"])
   elif dane["type"] =="outgoing":
      konto.przelew_wychodzacy(dane["amount"])  
   return jsonify({"message":"Zlecenie przyjęto do realizacji"}), 200

@app.patch("/api/accounts/save")
def save():
   RegisterOfAccounts.saveToDatabase()
   return jsonify({"message:": "Zapisano konta do bazy danych"}), 200

@app.patch("/api/accounts/load")
def load():
   RegisterOfAccounts.loadFromDatabase()
   return jsonify({"message:": "Załadowano konta z bazy danych"}), 200


if __name__ == '__main__':
   app.run(debug=True)