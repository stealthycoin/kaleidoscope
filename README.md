Kaleidoscope
===============

Examples
---------------



{
  website : {
    name : "Example Site 1",
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
