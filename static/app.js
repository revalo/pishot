let app = new Vue({
    el: '#app',
    data: {
        currentViewPi: {},
        loadingDevices: false,
        view: 'devices',
        pis: [],
    },
    methods: {
        reloadDevices: function() {
           this.loadingDevices = true;
           axios.get('/api/refresh').then((r) => {
               this.pis = r.data;
           }).catch(() => { }).then(() => {
               this.loadingDevices = false;
           });
        },
        viewPi: function(pi) {
            this.currentViewPi = pi;
            this.view = 'view';
        }
    },
    mounted: function() {
        this.reloadDevices();
    },
});
