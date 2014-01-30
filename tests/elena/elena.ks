website: {
    name: "elena",
    prettyName: "Elena's Homework Website",
    author: "Lacey B Carlyle", 
    theme: "minecraft",
    hostname: "homework.brilliantsquid.com",
    root: "/home/homework/laceyhw/"
}, 

apps: {
    science: {
	models: {

	    Subject: {
		fields: {
		    title: {type: "CharField", length: 30}
		},
		admin: "%title"
	    },

	    Submission: {
		fields: {
		    date: {type: "DateField", argstring: "auto_now=True", form: "False"},
		    source: {type: "CharField", length: 64},
		    title: {type: "CharField", length: 64},
		    Subject: {type: "ForeignKey", link: "'Subject'"},
		    summary: {type: "TextField"}

		},
		admin: "%title from %source",
		listing: "<h3>%title% - %subject% (%date%)</h3><p>By: %source%</p><p>%summary%</p>",
		display: "<h3>%title% - %subject% (%date%)</h3><p>By: %source%</p><p>%summary%</p>"
	    }
	}
    },

    current_events: {
	models: {
	    Submission: {
		fields: {
		    date: {type: "DateField", argstring: "auto_now=True", form: "False"},
		    source: {type: "CharField", length: 64},
		    title: {type: "CharField", length: 64 },
		    whatDidYouLearn: {type : "TextField", label:"What did you learn?" }
		},
		admin: "%title",
		listing: "<h3>%title% - %source% (%date%)</h3><p>%whatDidYouLearn%</p>",
		display: "<h3>%title% - %source% (%date%)</h3><p>%whatDidYouLearn%</p>"
	    }
	}
    },

    math_history: {
	models: {
	    Submission: {
		fields: {
		    date: {type: "DateField", argstring: "auto_now=True", form: "False"},
		    mainContributor: { type: "CharField", length: 64 },
		    year: {type: "CharField", length: 4 },
		    bigIdea: {type: "TextField", label: "What\\'s the big idea?"},
		    whatDidYouLearn: {type: "TextField", label: "What did you learn?"}
		},
		admin: "%mainContributor - %year",
		listing: "<h3>%mainContributor% - %year% (%date%)</h3><p>%bigIdea%</p><p>%whatDidYouLearn%</p>",
		display: "<h3>%mainContributor% - %year% (%date%)</h3><p>%bigIdea%</p><p>%whatDidYouLearn%</p>"
	    }
	}
    },

    pe: {
	models: {
	    Duration: {
		fields: {
		    time: { type: "SmallIntegerField" }
		},
		admin: "%time min"
	    },
	    
	    Activity:{
		fields: {
		    name: { type: "CharField", length: 64 }
		},
		admin: "%name"
	    },
	    
	    Submission: {
		fields: {
		    date: {type: "DateField", argstring: "auto_now=True", form: "False"},
		    activity: {type: "ForeignKey", link:"'Activity'"},
		    duration: {type: "ForeignKey", link: "'Duration'" },
		    notes: {type: "TextField", label: "What did you do?"}

		},
		admin: "%activity %duration",
		listing: "<h3>%activity% - %duration% (%date%)</h3><p>%notes%</p>",		
		display: "<h3>%activity% - %duration% (%date%)</h3><p>%notes%</p>"

	    }
	}
    },
    
    mathmatics: {
	models: {
	    Submission: {
		fields: {
		    date: {type: "DateField", argstring: "auto_now=True", form: "False"},
		    description: { type: "TextField" },
		    whatDidYouLearn: {type: "TextField" }
		},
		admin: "%description",
		listing: "<h3>%description% - (%date%)</h3><p>%whatDidYouLearn%</p>",
		display: "<h3>%description% - (%date%)</h3><p>%whatDidYouLearn%</p>"
	    }
	}
    }
},




menu: {
    Home:{ title: "Home", link: "/", placement: 0 },
    science: {title: "Science", link: "/science", placement: 1},
    currentEvents: {title: "Current Events", link: "/current", placement: 2},
    mathHistory: {title: "Math History", link: "/mathhistory", placement: 3},
    pe: {title: "P.E.", link: "/pe", placement: 4},
    math: {title: "Mathmatics", link: "/math", placement: 5},
    log: {title: "Logs", link: "/log", placement: 6}
},

pages: {
    Home: {
	title: "Elena Bernard",
	url: "",
	template: "<div class='box'>Click on the links above to go to a topic page.</div>"
    },
    Science:{
	title: "Science",
	url: "science/",
	template: "<h1>Science!</h1><div class='box'>%homework%</div><div class='box'>%addSubject%</div>",
	homework: F[](science->Submission),
	addSubject: F[](science->Subject)
    },
    Current: {
	title: "Current Events",
	url: "current/",
	template: "<h1>Current Events!</h1><div class='box'>%homework%</div>",
	homework: F[](current_events->Submission)
    },
    MathHistory: {
	title: "Math History",
	url: "mathhistory/",
	template: "<h1>Math History!</h1><div class='box'>%homework%</div>",
	homework: F[](math_history->Submission)
    },
    Mathmatics: {
	title: "Mathmatics",
	url: "math/",
	template: "<h1>Mathmatics!</h1><div class='box'>%homework%</div>",
	homework: F[](mathmatics->Submission)
    },
    PE: {
	title: "Physical Education",
	url: "pe/",
	template: "<h1>Physical Education</h1><div class='box'>%homework%</div>",
	homework: F[](pe->Submission)
    },
    log: {
	title: "Log",
	url: "log/",
	template: f"log.html",
	scienceList: S[](science->Submission),
	currentList: S[](current_events->Submission),
	mhList: S[](math_history->Submission),
	peList: S[](pe->Submission),
	mathList: S[](mathmatics->Submission)
    }
},

database: {
    name: "elena.db",
    engine: "django.db.backends.sqlite3"
}
