Kaleidoscope
===============
What is Kaleidoscope?
----------------
Kaleidoscope is all natrual and grass fed. No perservatives, addatives, smuggling rings, or gamechanging logistics.


Examples
---------------

Basic Blog Example
blog.ks
```
//File: blog.ks
website : {
    name : "Example_1",
    prettyName: "My most wonderous web-diary",
    author: "Penelopy",
    theme: "dreamcloud"
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
        template: "<div class='box'><h2>Welcome to Penelopy Wonderhagan's wonderful blog!</h2><p>Check back here to keep up with Penelopy's most recent projects.</p></div>" 
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
```

aboutPenelopy.html
```
<!-- File aboutPenelopy.html -->
<div class='box'>
<h2>Penelopy!</h2>
<p>Penelopy Wonderhagan is just a smalltown girl from New York. 
She enjoys her quiet life of high volume stock trading and spending time with her three boyfriends.</p>
<p>You can learn all you want to know (and more) about Penelopy by clicking on the Blog link in the menu above!</p>
</div>
```

Usage
----------------

```
kaleidoscope models.ks
```
```-u``` Puts kaleidoscope into update mode where it only tries to make updates to the project rather than generate it from scratch.
```-s``` Speficy a static file directory to be copied into the project. It should contain css/javascript/images subdirectories.

Installation
---------------

``` make ; sudo make install```

To uninstall simply `sudo make uninstall` but why would you ever do that?!

Documentation
=================

Basic Syntax
-----------------

File extensions for a kaleidoscope file: ```.ks```

Kaleidescope is made up of key value pairs as such:

```key : value```

A key must consist of only letters numbers and underscores, and must start with a letter. Multiple key value pairs can be seperated by a comma.

A value can be several different things:

1. A number, straightforwardly this is a number, either floating point or integer.
2. A string, Anything encapsulated by quotation marks.
3. Another set of key : value pairs surrounded by curly brackets and of course seperated by commas ``` car: { name: "Lady Cher", capacity: 6, cylinders: 4 }```
4. An f-sigil. An f-sigil is a string with the character f before it like so: ```f"example.txt"``` This will load the file example.txt into a string and replace the f-sigil with that string.
5. A relational expression, these allow you to express interactions with the database. They can retrive, edit, or create data on the backend. How this data is displayed is defined in the model section below. A simple relation expression that fetches a person named Hank: ```S[name='Hank'](person->Person)``` More about relation expressions below.


Describing a website
---------------------

Kaleidoscope is used to describe websites, to do so there are keys that have a particular meaning.

For example the key ```website``` is used to define all the most rudimentary components of the website such as its name and author.

Within the ```website``` value another set of key values is used to denote all the parts of the website for example:

`website : { name: "Example_Project", prettyName: "My First Site", author: "me" }`

To describe this structure this I will use the following notation 

+ `website -> name` - The folder the project will be stored in and the overall name, cannot contain space characters.
+ `website -> prettyName` - This is the name that will appear at the top of every page on the website.
+ `website -> author` - This property is used to generate the copyright that appears in the footer of every page.

Describing a menu
------------------

A menu is an element that will appear on every page
To describe a menu you can use the base level key `menu` inside that you can add a new key for each menu element you want to generate.

- `menu -> menuItem -> title` - This is the display name that will appear on the menu item link.
- `menu -> menuItem -> link` - The link property allows you to define where the menu item will take you when it is clicked on.
- `menu -> menuItem -> placement` - This property is a number that defines which order the menu is displayed in, smaller numbers are on the left.

example:

```
menu : { 
    home: { title: "Home", link: "index.html", placement: 0}, 
    about: { title: "About Us", link:"about.html", placement :2 }, 
    contact: { title: "Contact", link:"contact.html", placement: 3}
}
```


Describing a page
-----------------

Describing a single web page is similar to describing a menu element. The base level key is simply called `pages`. Within the `pages` there should be one key value pair for each page you wish to define.

- `pages -> aPage -> title` - The title property will be what is put in the <title></title> tags in the head of the page
- `pages -> aPage -> url` - The url property is what url will load this page, it supports regular expressions, remember to escape backslashes. For example a digit would be \\d not \d
- `pages -> aPage -> template` - The template property is a string that is used as the content for the page. It can either be static or make use of django template tags. Typically these should be defined elsewhere and f-sigil used to load it.
- `pages -> aPage -> otherKey` - Any key that is not one of the three above will be treated as a database query and loaded into the template variable `otherKey` for the template to make use of. The database querys are made using a subset of relational algebra with specific syntax described later in this document.

example:

```
pages: { 
    home: { title: "Homepage!", url: "" , template: f"home.html" },
    testimonials: { title: "Testimonials", url: "testimonials", template: f"test.html" },
    map: { title: "Site Map", url: "map", template: f"map.html" }, 
    about: { title: "About", url: "about", template: f"about.html" }
}
```

Describing an 'App'
-------------------

An app can be described as an aspect of your website. An app can have various models that store things in databases, it can have views and templates for controlling the interaction with those models.

Apps are slightly more complex than the previous keys. The top level key to start defining an app is `apps`. Inside the `apps` key there is one key per app, for example if we wanted to make an app that keeps track of cats we could do this: `apps : { cats : { ... } }` where ... would be used to define what the app was.

On its own this is not very useful, to give the app something to work with we need to give it at least one model, but more than likely multiple models that it can interact with. To define a model inside an app use the `models` key. An example:

```
apps: {
    cats: {
        models: {
            cat :{ ... }
        }
    }
}
```

Where ... would be used to define what the model was. A model needs a list of data storege elements which it does with the `fields` key. Each field needs two properties `type` and `argstring`.

- `apps -> appName -> models -> modelName -> fields -> type` - This property defines what type of data the field can store
- `apps -> appName -> models -> modelName -> fields -> argstring` - This property handles initializing the field
- `apps -> appName -> models -> modelName -> fields -> `optional` - if set to "True" means that this field is not required


Further, each model also needs the ability to draw itself in multiple situations including: admin panel (`admin` key), displayed on a web page (`display` key), and displayed as an element in a list (`listing` key). In any of the below properties the %-sigil can be used to reference a field of the model.

- `apps -> appName -> models -> modelName -> admin` String - Dictating how to draw the model in the admin panel.
- `apps -> appName -> models -> modelName -> display` String - Determines how to render the element on a normal webpage.
- `apps -> appName -> models -> modelName -> listing` String - Determines how to render the element in a list context webpage.

Cat example completed:

```
apps : {
    animals:
        models: {
            cat: {
                fields: {
                    name: { type: "CharField", length: 32 },
                    owner:{ type: "CharField", length: 32 },
                    description: { type: "TextField" } 
                },
                admin: "%name",
                display: "<h1>%name</h1><h4>Owned by: %owner</h4><p>%description</p>",
                listing: "<li>%name<\li>"
            }
        }
    }
}
```

Relation Expressions
--------------------

Relation expressions define a subset of Relational Algebra. Currently only two operations are defined.
The ```S``` and ```F``` operations. 

All relation expressions are made up of three segments like the following example: ```S[name='Fuzzy'](animals->cat)```

The first segment is the operator name for example ```F``` is for form, and ```S``` is for selection.

How the operators work:

```S``` The selection operation. This selects (or tries to select) a set of objects from the database.

```F``` The form operation. This operator will generate a form based on its arguments.

```[name='Fuzzy']``` The second portion of the expression is a list of restrictions enclosed in square brackets. Currently only the equality operator is defined. If the restrictions are left blank (```[]```) then everything from the database is selected. If the ```F``` operator is being used then an empty set of restrictions will make a creation form.

```(animals->cat)``` The third and final section is the set of objects to be selected from. In this case we are searching in the animals app, and searching through the cat models.

The example above Selects a cat from the databased with a name of Fuzzy. If there are multiple cats named Fuzzy it will select multiples and display them using the ```listing``` key. If there is only a single one it will use the ```display``` rule to render it.




