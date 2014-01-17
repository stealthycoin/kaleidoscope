
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
		    name: { type: "CharField", length: 32 },
		    institute: { type: "ForeignKey", link: "School" }
		},
		admin: "%name"
	    },
	    //represents a single school
	    School: {
		fields: {
		    name: { type: "CharField", length:128 }
		},
		admin: "%name",
		display: "<p>The name of this institution is: %name%</p>"
	    }
	}
    },
    
    story: {
	models: {
	    //represents a single story
	    Story: {
		fields: {
		    text: { type: "TextField" },
		    title: { type: "CharField",  length: 32 },
		    author: { type: "ForeignKey", link: "User" }, //user is a built in type
		    subject: { type: "ForeignKey", link: "professor->Professor" }
		},
		admin: "%title by %author",
		listing: "<a href='/story/%pk% '>%subject% in %title%</a>",
		display: "<h2>%title% starring: %subject%</h2><p><strong>By: %author%</strong></p><p>%text%</p>"
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
    about: { title: "About", link: "/about", placement: 1 },
    stories: { title: "Stories", link: "/stories", placement: 2 },
    create: { title: "Create", link: "/create", placement: 3 },
    story: { title: "Write", link: "/write", placement: 4 },
    signUp: { title: "Signup", link: "/signup", placement: 5 }
},

pages: {
    home: { title: "Epic Professors", url: "", template: "I'm a homepage and I'm useless" },

    about: { title: "About Epic Professors", url: "about/", template: f"about.html" },

    stories: { title: "Epic Professors", url: "stories/", template: "%storiesList%", storiesList: S[](story->Story) },

    create: { title: "Create", url: "create/", template: "Add people and place page!! %createSchool% %createProfessor%", 
	      createSchool: F[](professor->School),
	      createProfessor: F[](professor->Professor) },

    signup: { title: "Sign up", url: "signup/", template: "%newUser%", newUser: F[](Builtin->User) },

    writeStory: { title: "Write a Story", url: "write/", template: "%createStory%", 
		  createStory: F[](story->Story) },

    specificStory: { title: "Epic Professors", url: "story/(\\d+)/", template: "%theStory%", 
		     theStory: S[pk="%1"](story->Story) }
}
