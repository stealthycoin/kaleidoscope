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

File extensions for kaleidoscope file: ```.ks```