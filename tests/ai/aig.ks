
website: { 
	 name: "AIG", 
	 prettyName: "Artificial Intelligence Group at UCSC", 
	 author: "John Carlyle, Morgan McDermott" 
},
pages: {
    home : { title: "Homepage", url: "", template: "Home Page with test form {{ test | safe }}", test: S[](login->User) }
},
menu: {
    home: { title: "", link :"/", placement : 1 }
},
apps: {
    
    login: {
	models: {
	    User : {
		fields: {
		    name: { type: "CharField", argstring: "max_length=32" }
		},
		admin: "%name"
	    }
	}
    }
}
