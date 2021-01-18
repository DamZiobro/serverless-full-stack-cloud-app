/*
 * vue_instance.js
 * Copyright (C) 2021 damian <damian@damian-desktop>
 *
 * Distributed under terms of the MIT license.
 */

var  vm = new Vue({
   el: '#app',
   data() {
      return {
          books : null,
          newBook:{
              title:"",
              description:"",
              author_id:0,
          },
          loading: true,
          errored: false
      }
   },
    methods: {
        addBook:function() {
         axios
          .post(
              'https://xeyvfe7639.execute-api.eu-west-1.amazonaws.com/dev/books/',
              {
                  "title": this.newBook.title,
                  "description": this.newBook.description,
                  "author_id": parseInt(this.newBook.author_id),
              },
              { headers: {"Content-Type": "application/json" } }
          );
          this.newBook.title = "";
          this.newBook.description = "";
          this.newBook.author_id = 0;
        }
    },
   mounted () {
     axios
      .get(
          'https://xeyvfe7639.execute-api.eu-west-1.amazonaws.com/dev/books/',
      )
      .then(response => {this.books = response.data})
      .catch(error => {
        console.log(error)
        this.errored = true
      })
      .finally(() => this.loading = false)
   }
})
