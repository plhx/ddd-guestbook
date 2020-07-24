'use strict'


!$(function() {
    function Guestbook() {
        this.count = $('#guestbook-count')
        this.name = $('#guestbook-name')
        this.message = $('#guestbook-message')
    }

    function DatetimeFormatter() {
        function zfill(s, digits) {
            s = s + ''
            while(s.length < digits)
                s = '0' + s
            return s
        }
        this.format = function(dt) {
            return zfill(dt.getFullYear(), 4) + '/'
                + zfill(dt.getMonth() + 1, 2) + '/'
                + zfill(dt.getDate(), 2) + ' '
                + zfill(dt.getHours(), 2) + ':'
                + zfill(dt.getMinutes(), 2) + ':'
                + zfill(dt.getSeconds(), 2)
        }
    }

    let guestbookPosts = new Vue({
        el: '.container',
        delimiters: ['[[', ']]'],
        data: {
            guestbook: null,
            formatter: new DatetimeFormatter(),
            posts: []
        },
        mounted: function() {
            this.guestbook = new Guestbook()
            this.guestbook.message.focus()
            this.get()
        },
        methods: {
            toDatetime: function(timestamp) {
                let dt = new Date(timestamp * 1000)
                return this.formatter.format(dt)
            },
            get: function() {
                let self = this
                $.ajax({
                    cache: false,
                    method: 'GET',
                    url: '/guestbook?count=' + (self.guestbook.count.val() | 0),
                    success: function(data, textStatus, jqXHR) {
                        self.posts = data.posts.reverse()
                    }
                })
            },
            post: function() {
                let self = this
                $.ajax({
                    cache: false,
                    method: 'POST',
                    url: '/guestbook?count=' + (self.guestbook.count.val() | 0),
                    data: {
                        name: self.guestbook.name.val(),
                        message: self.guestbook.message.val()
                    },
                    success: function(data, textStatus, jqXHR) {
                        self.posts = data.posts.reverse()
                        self.guestbook.message.val('')
                    }
                })
            }
        }
    })
})
