var app = new Vue({
        el: '#main',
        data: {
            links: []
        },
        methods: {
            setData: function (data) {
                this.links = data;
            },
            openLink: function (link) {
                var win = window.open(link.url, '_blank');
                win.focus();
            },
            hasChildren: function (cat) {
                return cat.hasOwnProperty('children');
            }
        },
        computed: {
            flatLinks: function () {
                var cats = [];
                for (var i in this.links) {
                    var cat = this.links[i];
                    cats.push(cat);
                    if (cat.children) {
                        for (var j in cat.children) {
                            var sub = cat.children[j];
                            cats.push(sub)
                        }
                    }
                }
                return cats;
            }
        },
        updated: function () {
            window.setup_sidebar_menu();
            $('[data-toggle="tooltip"]').tooltip();
        }
    }
);