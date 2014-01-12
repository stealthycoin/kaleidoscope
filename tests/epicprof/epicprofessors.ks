

website : {
    name: "EpicProfs",
    prettyName: "Epic Professors",
    author: "Brilliant Squid",
    admins: { a : { name : "John Carlyle", email: "john.w.carlyle@gmail.com" },
	     b : { name: "Morgan McDermott", email: "something@gmail.com" }}
},

//some apps all up in this house
apps: {
    professor: { 
	models: {
	    //represents a single professor
	    Professor: {
		fields: {
		    name: { type: "CharField", argstring: "max_length=32" },
		    institute: { type: "ForeignKey", link: "School", noForm: "True" }
		},
		admin: "%name"
	    },
	    //represents a single school
	    School: {
		fields: {
		    name: { type: "CharField", argstring: "max_length=128" }
		},
		admin: "%name",
		display: "<p>The name of this institution is: %name</p>"
	    }
	}
    },
    
    story: {
	models: {
	    //represents a single story
	    Story: {
		fields: {
		    text: { type: "TextField" },
		    title: { type: "CharField", argstring: "max_length=32" },
		    author: { type: "ForeignKey", link: "User" }, //user is a built in type
		    subject: { type: "ForeignKey", link: "professor->Professor" }
		},
		admin: "%title by %author"
	    }
	}
    }  
},

database: {
    name: "profs.db",    
    engine: "django.db.backends.sqlite3"
},

menu: {
    home: { title: "Home", link: "/", placement: 0 },
    search: { title: "Search", link: "/search", placement: 1 },
    random: { title: "Random Story", link: "/random", placement: 2 },
    create: { title: "Create", link: "/create", placement: 3 },
    story: { title: "Write", link: "/write", placement: 4 }
},

pages: {
    home: { title: "Epic Professors", url: "", template: "I'm a homepage" },
    search: { title: "Epic Professors", url: "search/", template: "I'm a search page" },
    random: { title: "Epic Professors", url: "random/", template: "I'm a random story page" },
    create: { title: "Epic Professors", url: "create/", template: "Add people and place page!! {{ createSchool | safe }} {{ createProfessor | safe }}", 
	      createSchool: "F[](professor->School)|Failt Somehow",
	      createProfessor: "F[](professor->Professor)|Failt somehow"},
    writeStory: { title: "Write a Story", url: "write/", template: "{{ createStory | safe }}", 
		  createStory: "F[](story->Story)|Failt"}
}
