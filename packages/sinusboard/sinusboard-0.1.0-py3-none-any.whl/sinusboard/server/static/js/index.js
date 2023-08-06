var app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {},
    methods: {
        playClip(uuid) {
            fetch("/play/" + uuid).then((response) => {JSON.parse(response)})
        }
    }
});

if ('serviceWorker' in navigator) {
    navigator.serviceWorker
    .register('./service-worker.js')
    .then(function(registration) {
        console.log('Service Worker Registered!');
        return registration;
    })
    .catch(function(err) {
        console.error('Unable to register service worker.', err);
    });
}
