
website: { 
	 name: "AIG", 
	 prettyName: "Artificial Intelligence Group at UCSC", 
	 author: "John W. Carlyle, Morgan A. McDermott" 
},

pages: {
    home : { title: "Homepage", url: "", template: "Home Page with nothing on it!" },
    about: { title: "About AIG", url: "about/", template: "AIG is a wonderful bank... I mean group of students interested in AI." },
    signup: { title: "Signup", url: "signup/", template: "%signup%" }
},

menu: {
    home: { title: "Home", link :"/", placement : 1 },
    about: { title: "About", link: "/about", placement: 2},
    signup: { title: "Signup", link: "/signup", placement: 3 }
},

apps: {
    student: {
	models: {
	    StudentInfo: {
		fields: {
		    studentId: { type: "IntegerField" },
		    description: { type: "TextField" },
		    user: { type: "ForeignKey", link: "User" }
		}
	    }
	}
    }
},

database: {
    name: "aig.db",    
    engine: "django.db.backends.sqlite3"
}
