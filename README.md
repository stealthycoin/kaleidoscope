Kaleidoscope
===============

Examples
---------------


```
{
  website : {
    name : "Example_1",
    prettyName: "My most wonderous web-diary"
    author: "Penelopy"
  },
  
  menu: {
    home : { title:"Homepage", link: "/", placement: 1 }
  }   
  
}
```


Usage
----------------

```
python kaleidoscope.py -ps models.ks
```

-p is for parsing
-s is for starting project
-f specifies the ks file to parse 


Grammar
---------------

![Grammar for defining a site](https://github.com/stealthycoin/kaleidoscope/blob/master/grammar.png?raw=true "Grammar")


Documentation
=================

Basic Syntax
-----------------

File extensions for a kaleidoscope file: ```.ks```

Kaleidescope is made up of comma seperated key value pairs as such:

```key : value```

A key must consist of only letters numbers and underscores, and must start with a letter.

A value can be several different things:

1. A number, straightforwardly this is a number, either floating point or integer.
2. A string, Anything encapsulated by quotation marks.
3. Another set of key : value pairs surrounded by curly brackets and of course seperated by commas ``` car: { name: "Lady Cher", capacity: 6, cylinders: 4 }```
4. A f-sigil. An f-sigil is a string with the character f before it like so: ```f"example.txt"``` This will load the file example.txt into a string and replace the f-sigil with that string.


Describing a website
---------------------

Kaleidoscope is used to describe websites, to do so there are keys that have a particular meaning.

For example the key ```website``` is used to define all the most rudimentary components of the website such as its name and author.

Within the ```website``` value another set of key values is used to denote all the parts of the website for example:

```website : { name: "Example_Project", prettyName: "My First Site", author: "me" }```

To describe this structure this I will use the following notation 

+ ```website -> name``` - The folder the project will be stored in and the overall name, cannot contain space characters.
+ ```website -> prettyName``` - This is the name that will appear at the top of every page on the website.
+ ```website -> author``` - This property is used to generate the copyright that appears in the footer of every page.

Describing a menu
------------------

A menu is an element that will appear on every page
To describe a menu you can use the base level key ```menu``` inside that you can add a new key for each menu element you want to generate.

- ```menu -> menuItem -> title``` - This is the display name that will appear on the menu item link.
- ```menu -> menuItem -> link``` - The link property allows you to define where the menu item will take you when it is clicked on.
- ```menu -> menuItem -> placement``` - This property is a number that defines which order the menu is displayed in, smaller numbers are on the left.

example:

```menu : { 

    home: { title: "Home", link: "/", placement: 0}, 

    about: { title: "About Us", link:"/about.html", placement :2 }, 

    contact: { title: "Contact", link:"/contact.html", placement: 3}

}```
