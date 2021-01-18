/*
 * vue_instance.js
 * Copyright (C) 2021 damian <damian@damian-desktop>
 *
 * Distributed under terms of the MIT license.
 */

var  vm = new Vue({
   el: '#vue_det',
   data() {
      return {
          books : null,
          loading: true,
          errored: false
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
