/*
 * vue_instance.js
 * Copyright (C) 2021 damian <damian@damian-desktop>
 *
 * Distributed under terms of the MIT license.
 */
let config = {
  apiBaseUrl: "https://xeyvfe7639.execute-api.eu-west-1.amazonaws.com/dev",
}

var removeByAttr = function(arr, attr, value){
    var i = arr.length;
    while(i--){
       if( arr[i] 
           && arr[i].hasOwnProperty(attr) 
           && (arguments.length > 2 && arr[i][attr] === value ) ){ 

           arr.splice(i,1);

       }
    }
    return arr;
}

var  vm = new Vue({
   el: '#app',
   data() {
      return {
          books : null,
          newBook:{
              book_id:0,
              title:"",
              description:"",
              author_id:0,
          },
          authors : null,
          newAuthor:{
              author_id:0,
              first_name:"",
              last_name:"",
          },
          loading: true,
          errored_get: false,
          errored_delete: false,
          errored_post: false
      }
   },
    methods: {
        addBook:function() {
         console.log("Adding new book");
         axios
          .post(
              config.apiBaseUrl + '/books/',
              {
                  "title": this.newBook.title,
                  "description": this.newBook.description,
                  "author_id": parseInt(this.newBook.author_id),
              },
              { headers: {"Content-Type": "application/json" } }
          )
          .then(response => {this.books.push(response.data)})
          .catch(error => {
            console.log(error)
            this.errored_post = true
          });

          this.newBook.title = "";
          this.newBook.description = "";
          this.newBook.author_id = 0;

        },
        addAuthor:function() {
         console.log("Adding new author");
         axios
          .post(
              config.apiBaseUrl + '/authors/',
              {
                  "first_name": this.newAuthor.first_name,
                  "last_name": this.newAuthor.last_name,
              },
              { headers: {"Content-Type": "application/json" } }
          )
          .then(response => {this.authors.push(response.data)})
          .catch(error => {
            console.log(error)
            this.errored_post = true
          });

          this.newAuthor.first_name = "";
          this.newAuthor.last_name = "";
        },
        getAuthors:function() {
         console.log("Getting authors");
         axios
          .get(
              config.apiBaseUrl + '/authors/',
          )
          .then(response => {this.authors = response.data})
          .catch(error => {
            console.log(error)
            this.errored_get = true
          })
          .finally(() => this.loading = false);
        },
        getBooks:function() {
         console.log("Getting books");
         axios
          .get(
              config.apiBaseUrl + '/books/',
          )
          .then(response => {this.books = response.data})
          .catch(error => {
            console.log(error)
            this.errored_get = true
          })
          .finally(() => this.loading = false);
        },
        removeBook:function(book) {
         console.log("Remove book with id: " + book.book_id);
         axios
          .delete(
              config.apiBaseUrl + '/books/' + book.book_id,
          )
          .then(response => {removeByAttr(this.books, 'book_id', book.book_id)})
          .catch(error => {
            console.log(error)
            this.errored_delete = true
          })
          .finally(() => this.loading = false);
        }
    },
   mounted () {
       this.getBooks();
       this.getAuthors();
   }
})
