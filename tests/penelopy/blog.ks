//File: blog.ks
website : {
    name : "Example_1",
    prettyName: "My most wonderous web-diary",
    author: "Penelopy",
    theme: "lardface"
},

apps: {
    blog: {
        models: {
            Entry: {
                fields: {
                    title: { type: "CharField", length: 64 },
                    body: { type: "TextField" },
                    time: { type: "DateField", argstring: "auto_now=True", form: "False" }
                },
                listing: "<div class='box'><h2>%title%</h2><h7>Posted By Penelopy at %time%</h7><p>%body%<p></div>",
                display: "<div class='box'><h2>%title%</h2><h7>Posted By Penelopy at %time%</h7><p>%body%<p></div>"
            }
        }
    }
},

menu: {
    home: { title:"Homepage", link: "/", placement: 1 },
    about: { title: "About", link: "/about", placement: 2 },
    posts: { title: "Blog", link: "/blog", placement: 3}
},

pages: {
    home: { 
        title: "Penelopy Wonderhagan", 
        url: "", 
        template: "<div class='box'><h2>Welcome to Penelopy Wonderhagan's wonderful blog!</h2><p>Check back here to keep up with Penelopy's most recent projects.</p></div>",
	frp: (@time) -> (L["50*$1"],L["100*$1"])
    },
    about: { 
        title: "About Penelopy Wonderhagan", 
        url: "about/", 
        template: f"aboutPenelopy.html"
    },
    blog: { 
        title: "Penelopy Blog", 
        url:"blog/", 
        template: "%blogPosts%", 
        blogPosts: S[](blog->Entry) 
    },
    superSecretBlogPostMakingPage: { 
        title: "Make a blog post!", 
        url: "ugogurl/", 
        template: "<div class='box'><h4>Write a new blog entry you sexy important lady you. The people want to hear from you!</h4>%newPost%</div>",
        newPost: F[](blog->Entry) 
    }
},

database: {                                                                                                                                                                                                                                 
    name: "penelopy.db",
    engine: "django.db.backends.sqlite3"
}
