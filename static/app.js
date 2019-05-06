let app = new Vue({
    el: '#app',
    data: {
        currentViewPi: {},
        loadingDevices: false,
        view: 'devices',
        pis: [],
        vf: '',
        onion: '',
        onionVf: '',
        shutterLoading: false,
        shutterErrors: [],
        currentSave: '',
    },
    methods: {
        device(uuid) {
            return this.pis.filter((x) => x.uuid == uuid)[0];
        },
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
        },
        rebootDevices: function() {
            axios.get('/api/reboot/all');
        },
        rebootDevice: function(pi) {
            axios.get('/api/' + pi.uuid + '/reboot');
        },
        cpip: function(ip) {
            copyStringToClipboard(ip);
        },
        requestViewFrame() {
            axios.get('/api/' + this.currentViewPi.uuid + '/capture').then((r) => {
                this.vf = r.data.image;
            });

            if (this.onion !== '') {
                axios.get('/api/' + this.onion + '/capture').then((r) => {
                    this.onionVf = r.data.image;
                });
            }
        },
        openShutter() {
            this.shutterLoading = true;
            axios.get('/api/open').then((r) => {
                this.shutterLoading = false;
                this.shutterErrors = r.data.errors;
            });
        },
        closeShutter() {
            this.shutterLoading = true;
            axios.get('/api/close').then((r) => {
                this.shutterLoading = false;
                this.shutterErrors = r.data.errors;
            });
        },
        download() {
            this.shutterLoading = true;
            axios.get('/api/download').then((r) => {
                this.shutterLoading = false;
                this.shutterErrors = r.data.errors;
                this.currentSave = r.data.save_number;
            });
        },
    },
    mounted: function() {
        this.reloadDevices();
    },
});


function copyStringToClipboard(str) {
    // Create new element
    var el = document.createElement('textarea');
    // Set value (string to be copied)
    el.value = str;
    // Set non-editable to avoid focus and move outside of view
    el.setAttribute('readonly', '');
    el.style = {position: 'absolute', left: '-9999px'};
    document.body.appendChild(el);
    // Select text inside element
    el.select();
    // Copy text to clipboard
    document.execCommand('copy');
    // Remove temporary element
    document.body.removeChild(el);
 }