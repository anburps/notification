importScripts('https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/9.6.1/firebase-messaging.js');

const firebaseConfig = {

    apiKey: "AIzaSyDkmg9mZCFrBtOpy7z549yuqaK1jtGb28c",

    authDomain: "hrms-f4dab.firebaseapp.com",

    projectId: "hrms-f4dab",

    storageBucket: "hrms-f4dab.firebasestorage.app",

    messagingSenderId: "341801491085",

    appId: "1:341801491085:web:af8c4da803a609cd3460c4",

    measurementId: "G-DH7BMBMDJD"

};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log("Received background message ", payload);
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: "/static/img/success_icon.png"
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});
