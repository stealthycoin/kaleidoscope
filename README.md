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
----------------

File extensions for a kaleidoscope file: ```.ks```

Kaleidescope is made up of key value pairs as such:

```key : value```

A key must consist of only letters numbers and underscores, and must start with a letter.

A value can be several differnet things:

1. A number, straightforwardly this is a number, either floating point or integer.
2. A string, Anything encapsulated by quotation marks.
3. Another set of key : value pairs surrounded by curly brackets ``` car: { name: "Lady Cher", capacity: 6, cylinders: 4 }```
4. A f-sigil. An f-sigil is a string with the character f before it like so: ```f"example.txt"``` This will load the file example.txt into a string and replace the f-sigil with that string.
