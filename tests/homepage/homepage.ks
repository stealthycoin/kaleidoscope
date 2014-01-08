//a comment dude!

website: {
    name: "Homepage_Testing",
    prettyName: "FatShark",
    author: "Brilliant Squid",
    admins: { a: { name: "John Carlyle", email: "john.w.carlyle@gmail.com"}}
},

database: {
    engine: "django.db.backends.sqlite3",
    name: "db.db"
},

apps: {
    Bro: { 
	models: {
	    Bro: { 
		fields: {
		    name: { type: "CharField", argstring: "max_length=32", unique: "True" },
		    home: { type: "ForeignKey", argstring: "'Pad'" },
		    homies: { type: "ManyToManyField", argstring: "'Bro'" }
		},
		admin: "%name - %home",
		display: "<h3>Name: %name</h3><p>Home: %home</p>",
		listing: "<p>{{ o.name }}</p>"
	    },

	    Pad: {
		fields: {
		    name: { type: "CharField", argstring: "max_length=32" },
		    stunnerShadeCount: { type: "SmallIntegerField" }
		},
		admin: "%name",
		display: f"pad.html",
		listing: "<p>{{ o.name }}</p>"
	    }
	}
    }
},

menu: {
    home: { title: "Home", link: "/", placement: 1 },
    testimonials: { title: "Testimonials", link: "testimonials", placement: 2 },
    about: { title: "About", link: "about", placement: 3 },
    map: { title: "Site Map", link: "map", placement: 4 },
    emacs: { title: "emacs", link: "emacs", placement: 5 }
},

pages: { 
    home: { title: "Homepage!", url: "" , template: f"home.html" },
    testimonials: { title: "Testimonials", url: "testimonials", template: f"test.html" },
    map: { title: "Site Map", url: "map", template: f"map.html" }, 
    about: { title: "About", url: "about", template: f"about.html" },
    emacs: { title: "emacs", url: "emacs", template: f"emacs.html" },
    bropage: { title: "Dude shh, theres a bro", url: "bro/(\\d+)", template: f"bropage.html", thebro: "S[pk=%1](Bro->Bro)" },
    padpage: { title: "Padedup", url: "pad/(\\d+)", template: f"padpage.html", thepad: "S[pk=%1](Bro->Pad)" }
}
