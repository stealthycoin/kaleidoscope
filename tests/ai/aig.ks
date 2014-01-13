
website: { 
	 name: "AIG", 
	 prettyName: "Artificial Intelligence Group at UCSC", 
	 author: "John Carlyle, Morgan McDermott" 
},
pages: {
    home : { title: "Homepage", url: "", template "Home Page with test form {{ test | safe }}", test: S[](user->User) }
},
menu: {
    home: { title: "", url :"/", placement : 1 }
}
apps: {
    
    user: {
	models: {
	    User : {
		fields: {
		    name: { type: "CharField", argstring: "max_length=32" }
		}
	    },
	    admin: "%name"
	}
    }
    
}
