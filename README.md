Hindi Dialogue System for library related queries
===

Project Source Code Can be Downloaded from the github repository ykaran86/library
---

Author
---

Yogesh Karan

Supervisors:- Shrikant Malviya(Research Scholar, IIIT Allahabad) and Rohit Mishra(Research Scholar, IIIT Allahabad)

**created and tested on Ubuntu 16.04 LTS with Python 3.6**

An Attempt to make a very simple, Library Asssistant that understands speech as well as text input and is capable of providing answers to various types of queries related to a library system. The library database used is IIIT Allahabad library database. This project is based on rule based approach. This is project is in very primitive stage, so various modifications are required. But right now it can work on several types of queries:

	Client: एडवांस बायोलॉजी के लेखक कौन है  
	Computer: Simpkins, J.; Williams, J.I.
	
	Client: उन्होंने कितनी किताबें लिखी हैं  
	Computer: 1.
	
	Client: द लॉर्ड ऑफ द रिंग्स की कितनी किताबें हैं  
	Computer:  5

	Client: उसके लेखक कौन-कौन है  
	Computer: 1) Tolkien, Jrr ;  
   		  2) Tolkien, J. R. R. ;  
   		  3) Tolkien, J. J. J. ;  
   		  4) J.R.R. Tolkien ;  
   		  5) Collins, Harper ;

	Client: Tolkien ने कौन-कौन सी किताबें लिखी हैं  
	Computer: 1) The Lord of the Rings Part-3 = The Return of the    King ;  
		  2) The Lord of the Rings Part-2 = The Two Towers ;  
		  3) The lord of the rings ;  
   	          4) The lord of the rings ;  
		  5) The hobbit ;

	Client: डिजिटल सेटेलाइट कम्युनिकेशंस की कितनी कॉपी अवेलेबल है  
	Computer: 21

	Client: उसके लेखक कौन हैं  
	Computer:  1) Tri T. Ha ;  
     	   2) edited by Giovanni E. Corazza ;

	Client: उसकी इशू डेट क्या है  
	Computer: 1) 04/11/2011 12:00:00 AM ;  
      	  2) 11/13/2013 12:00:00 AM ;

	Client: उसकी कितनी कॉपी रिजर्व नहीं है  
	Computer: 20

	Client: उसे लास्ट यीशु किसने की थी  
	Computer: 1) IEC2006048 ;Prabhat Bharti ;  
     	  2) IEC2010062 ;Harsh Bhardwaj ;


	Client: अलजेब्रा से रिलेटेड 5 किताबों के नाम बताइये  
	Computer: 1) College Algebra = Enhanced with graphing Utilities ;  
		  2) Schaum`s outline of theory and problems of linear algebra ;  
		  3) Complex varibles and applications ;  
		  4) Digital Computer Fundamentals ;  
		  5) Digital Instumentation ;

	Client: लाइब्रेरी में सबसे ज्यादा ड्यूस किस ग्रुप का है  
	Computer: 1) Faculty ;  
    	  2) Ph.D. ;

	CLient: लाइब्रेरी में मेरा कितना ड्यूस है  
	Computer:  आपका नाम क्या है

	Client: Asheesh Kumaar  
	Computer:  4 ;

	Client: मेरी कौन-कौन सी किताबें ड्यूस है  
	Computer: 1) The Seven Habits of Highly Effective People ;  
		  2) English-Hindi dictionary ;  
		  3) Oxford advanced learner`s dictionary (Under Book Bank Scheme only for SC/ST Students) ;  
		  4) Right to information guide : how to use the right to information   act effectively ;

	Client: मेरी English-Hindi dictionary की ड्यू डेट क्या है   
	Computer: 11/11/2013 12:00:00 AM ;

	Client: लाइब्रेरी में सबसे ज्यादा ड्यूस किसका है  
	Computer: 1) Mr. Shashi Kant Rai ;  
     	  2) Dr. Nidhi Mishra ;  
      	  3) Ranjeet Kumar ;

	Client: Dr. Nidhi Mishra का कितना ड्यूस है  
	Computer: 9

	Client: उनका फोन नंबर और ईमेल ID मिल सकता है क्या
	Computer: 9450900033 ;nidhimishra@iiita.ac.in ;
	
	Client: शुक्रिया
	Computer: इस सुविधा का उपयोग करने के लिए धन्यवाद

File List
---

```
.:

index

mysite

README.md

.gitignore

library.db

manage.py

```

```
./index

views.py

models.py

urls.py

static/dialog.js

templates/home.html

migration

__init__.py

admin.py

apps.py

tests.py

```

```

./mysite

urls.py

settings.py

__init__.py

wsgi.py

```

Once you have cloned the directory to your local machine, follow the directions below:
---
Prerequisites:-  
1. python 3.6 as default python version.  
2. google chrome as default browser.  
3. install pip  

The procedure mentioned here is taken from *Django girls tutorial* so you can take the help from
there too.

**Follow These Steps**

1. Download the code from the github repository ykaran86/library and extract it.

2. Make a new folder/directory and give it a name(for example, library) or run the following
command:-  
	` ~$ mkdir library`  
this is the directory where you are going to add files from the downlaoded code

3. now create a virtual environment(name it as ‘myvenv’) inside that directory  
	` $ cd library `  
	` ~/library$ python3 -m venv myvenv `  
if you get error that virtual environment was not created then run the following command:-  
	` ~/library$ sudo apt-get install python3-venv `  
	 		or  
	` ~/library$ sudo apt install python3-venv `  
if still getting error in creating virtual environment checkout steps from *Django girls Tutorial*  
finally create the virtual environment:  
	` ~/library$ python3 -m venv myvenv `

4. now start the virtual environment:-  
	` ~/library$ source myvenv/bin/activate `

5. installing Django:-  
	` (myvenv) ~/library$ python3 -m pip install --upgrade pip `  
	` (myvenv) ~/library$ pip install django~=1.11.0 `

6. start the project:-  
	` (myvenv) ~/library$ django-admin startproject mysite . `  
	**NOTE:-** “.” at the last is compulsary.

7. now you will have mysite directory inside the library
directory.  
In that you will find **settings.py** file.  
In that you will find **ALLOWED_HOSTS** list.  
Add **'127.0.0.1','localhost'** in that list it will look like:-  
` ALLOWED_HOSTS = ['127.0.0.1','localhost'] `  
make changes in Internationalization as:-  
```

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

```  
and add a line after STATIC_URL  
```

STATIC_URL = '/static/'  
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

```
8. creating database:-  
run the command:  
	` (myvenv) ~/library$ python manage.py migrate `  
if this gives any error like  
    1) No module named *apt_pkg*  
    then run:-  
	` (myvenv)~/library$ sudo apt-get update `  
	` (myvenv)~/library$ sudo apt-get dist-upgrade `  
    this may take a while.  
    In the root directory run the following command:-  
	` ~$ sudo ln -s apt_pkg.cpython-{35m,36m}-x86_64-linux-gnu.so `  
    you can search this solution in the stackOverflow also,i found there.  
    2) if error comes like No module named *django*  
    then run:-  
	` (myvenv)~/library$ python -m pip install django `  
		 or use python3 in place of python  
    now finally run migrate command:-  
	` (myvenv) ~/library$ python manage.py migrate `

Now, you can see a database file **db.sqlite3** in the library directory which is the default database provided by django  
and here it will be used for creating dialogues
 
9. now check whether the website is running  
start the server:-  
	` (myvenv)~/library$ python manage.py runserver `  
if no error shows up and a link(http://127.0.0.1:8000/) is  
provided then open that link in chrome.  
If It worked! is displayed then you are on right track.  

10. creating an application:-  
	` (myvenv)~/library$ python manage.py startapp index `  
add ‘index’ in **INSTALLED_APPS** list in **mysite/settings.py**  
**INSTALLED_APPS** list will look like:-
```

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'index',
]

```

11. now replace the **models.py** in the index directory with the  
**models.py** in the **index directory from the downloaded code**.  
models.py is used to create the dialogue

12. for making changes in the database  
run the following commands:-  
	` (myvenv)~/library$ python manage.py makemigrations index `  
	` (myvenv)~/library$ python manage.py migrate index `  
	` (myvenv)~/library$ python manage.py createsuperuser `  
now provide username,email,password

13. 1)now replace the **mysite/urls.py** with **mysite/urls.py** from
**downloaded code.**  
2)Copy **urls.py** in the **index directory from the downloaded code**
and paste in the **index directory in the library directory**.

14. replace **views.py** in the **index directory** with the **views.py in**
**the index directory from the downloaded code.**  
**Views.py** is the main file which actually takes the query input
and gives the output to a javascript file which displays to HTML
file.

15. copy **static and templates directory in index directory** from
the **downloaded code** and paste in the **index folder of your library**
directory  
**static directory contains dialog.js** which takes input from the
HTML file , sends to views.py and then views.py returns the answer
to dialog.js and it displays it to home.html  
**templates directory contains home.html**

16. now paste **library.db** from the downloaded code in your library
directory.  
This is the library database.

17. installing google translate api  
run the following command:-  
	` (myvenv)~/library$ python -m pip install googletrans `  
			 or  
	` (myvenv)~/library$ python3 -m pip install googletrans `

18. installing speech recoginition:-  
run following commands:-  
1) ` (myvenv)~/library$ sudo apt-get install portaudio19-dev `  
2) ` (myvenv)~/library$ pip install pyaudio `  
3) ` (myvenv)~/library$ sudo pip install SpeechRecognition `

19. now you are all set to use the library dialogue system using
microphone  
start the Server  
	` (myvenv)~/library$ python manage.py runserver `  	
go to the link http://127.0.0.1:8000/

Contribution
---

A lot of improvements can be done with this project. Several issues can be sorted out.  
Pull requests for any such changes are accepted. Feel free to fork this project and make your own changes too.
