{
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
			name: { type: "CharField", argstring: "max_length=32" },
			home: { type: "ForeignKey", argstring: "'Pad'" },
			homies: { type: "ManyToManyField", argstring: "'Bro'" }
		    }
		},

		Pad: {
		    fields: {
			name: { type: "TextField" },
			stunnerShadeCount: { type: "SmallIntegerField" }
		    }
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
	home: { title: "Homepage!", url: "" , template: "home.html" },
	testimonials: { title: "Testimonials", url: "testimonials", template: "test.html" },
	map: { title: "Site Map", url: "map", template: "map.html" }, 
	about: { title: "About", url: "about", template: "about.html" },
	emacs: { title: "emacs", url: "emacs", template: "emacs.html" }
    }
}
