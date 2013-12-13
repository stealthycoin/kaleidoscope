Kaleidoscope
===============

Examples
---------------


```
{
  website : {
    name : "Example Site 1",
    boilerplate: "bs",
  },
  
  models: {
    user : {
      char: "name",
      email: "email",
      password: "pass",
    },
    post : {
      char: "title",
      date: "posted",
      text: "content",
      user: "author",
    }
  },
  
  permissions: {
  
    user -> post
  
  }
  
  

}
```


Usage
----------------

```
python prep.py -ps models.json
```

p is for parsing
s is for starting project
then a list of json files to parse


Grammar
---------------

![Grammar for defining a site](https://github.com/stealthycoin/kaleidoscope/blob/master/grammar.png "Grammar")
