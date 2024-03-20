Hospital Flask Project

Acest proiect este o aplicație web Flask pentru gestionarea unui spital. Acesta include funcționalități pentru înregistrarea utilizatorilor, autentificare, gestionarea doctorilor, pacienților, asistenților și tratamentelor.

Funcționalități:
- Înregistrarea utilizatorilor cu roluri diferite (Manager General, Doctor, Asistent)
- Autentificarea utilizatorilor folosind JWT (JSON Web Tokens)
- Gestionarea doctorilor (adăugare, vizualizare)
- Gestionarea pacienților (adăugare, vizualizare)
- Gestionarea asistenților (vizualizare)
- Gestionarea tratamentelor (adăugare, vizualizare)

Cerințe rulare proiect local:
- Python 3.x
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- SQLAlchemy-Utils
- Werkzeug 

Configurare:
1. Clonează repository-ul:
	git clone https://github.com/username/hospital-flask-proj.git
2. Instalează dependențele:
	pip install -r requirements.txt
3. Configurează cheia secretă JWT și URI-ul bazei de date în fișierul app.py.
4. Rulează aplicația:
	python app.py

Bug-uri cunoscute:
- Există un bug cu token-urile JWT care poate provoca erori de autentificare în anumite scenarii. Acesta este cauzat de gestionarea incorectă a token-urilor expirate sau invalide. Se lucrează la o soluție pentru rezolvarea acestui bug.

Vulnerabilități:
- Aplicația folosește o cheie secretă JWT hardcoded în codul sursă. Aceasta reprezintă o vulnerabilitate, deoarece oricine are acces la codul sursă poate vedea cheia secretă. Este recomandat să stocați cheia secretă într-un fișier de configurare separat sau într-o variabilă de mediu.

Contribuții:
- Contribuțiile sunt binevenite! Dacă găsiți alte bug-uri, aveți sugestii de îmbunătățire sau doriți să adăugați noi funcționalități, vă rugăm să deschideți un issue sau să trimiteți un pull request.

Vă rugăm să rețineți că acest proiect este în stadiu de dezvoltare și poate conține bug-uri și vulnerabilități. Utilizați-l cu precauție și asigurați-vă că luați măsurile necesare pentru a securiza aplicația înainte de a o implementa într-un mediu de producție.