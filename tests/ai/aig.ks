website: { 
	 name: "AIG", 
	 prettyName: "Artificial Intelligence Group at UCSC", 
	 author: "John W. Carlyle, Morgan A. McDermott" 
},
pages: {
    home : { title: "Homepage", url: "", template: "Home Page with nothing on it!" },
    signup: { title: "Signup", url:"signup/", template: "%createUser%", createUser: S[](User) }
},
menu: {
    home: { title: "Home", link :"/", placement : 1 },
    signup: { title: "Signup", link: "signup/", placement: 2 }
},
apps: {
    
    login: {
	models: {
	    User : {
		fields: {
		    name: { type: "CharField", length: 32 },
		    password: { type: "CharField", length: 128 },
		    title: { type: "CharField", length: 128 }
		},
		admin: "%name",
		listing: "%name%",
		display: "<h2>%name%</h2>"
	    }
	}
    }
},

database: {
    name: "aig.db",    
    engine: "django.db.backends.sqlite3"
}
