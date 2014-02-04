//generate a webular site man
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
		    name: CharField { length: 32 },
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
		    text: TextField,
		    title: CharField { length: 32, label: "Title" },
		    author: ForeignKey { link: "User", label: "Username" }, //user is a built in type
		    subject: ForeignKey { link: "professor->Professor", label: "Professor" }
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
    story: { title: "Write", link: "/write", placement: 4 }
},

pages: {
    loginstripe: {
	template: f"loginstripe.html",
	pages: {
	    
	    home: { title: "Epic Professors", url: "", template: "%1% I'm a homepage and I'm useless %1%" },
	    
	    about: { title: "About Epic Professors", url: "about/", template: f"about.html" },
	    
	    stories: { title: "Epic Professors", url: "stories/", template: "%1% %storiesList% %1%", 
		       storiesList: expr { expr: S[](story->Story) } },

	    create: { title: "Create", url: "create/", template: "%1% Add people and place page!! %createSchool% %createProfessor% %1%", 
		      createSchool: expr { 
			  title: "Add a school", 
			  description: "Is your school missing from our website? Add it so we can tell your stories.", 
			  expr: F[](professor->School) },
		      createProfessor: expr { 
			  title: "Add a new professor", 
			  description: "Don\\'t see your favorite professor here? Add them by filling out the form below!", 
			  expr: F[](professor->Professor) 
		      } 
		    },

	    writeStory: { security: { login: "True",
				      fail: "signup",
				      failmessage: "You are not signed in, please try signing in and realoading the page."
				    },
			  title: "Write a Story", url: "write/", template: "%1% %createStory% %1%", 
			  createStory: expr { title: "Write a story",
					      description: "Share your favorite story about a professor. Fact or Fiction.",
					      expr: F[](story->Story) } },

	    specificStory: { title: "Epic Professors", url: "story/(\\d+)/", template: "%1% %theStory% %1%", 
			     theStory: expr { expr: S[pk="%1"](story->Story) } }
	}
    },

    //this one doesn't have a login stripe on it so its outside the loginstripe page
    signup: { title: "Sign up", url: "signup/", template: f"signup.html" }
}
