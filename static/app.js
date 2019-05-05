let app = new Vue({
    el: '#app',
    data: {
        currentViewPi: {},
        loadingDevices: false,
        view: 'devices',
        pis: [],
        vf: '',
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