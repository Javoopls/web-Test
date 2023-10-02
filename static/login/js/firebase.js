export const BASE_URL = 'https://http://127.0.0.1:8000/';
export const BASE_URL_API = 'https://us-central1-cl-8pay.cloudfunctions.net/API/';

export const firebaseConfig = {
    apiKey: "AIzaSyB6ej7hmj5hPxYU3qYWF-3JRyPEb6KnR8c",
    authDomain: "cl-8pay.firebaseapp.com",
    databaseURL: "https://cl-8pay-default-rtdb.firebaseio.com",
    projectId: "cl-8pay",
    storageBucket: "cl-8pay.appspot.com",
    messagingSenderId: "98307844586",
    appId: "1:98307844586:web:3d9898d94ad3018c62ea93",
    measurementId: "G-XY6KFJ62JZ"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);
const db = firebaseApp.firestore();
const auth = firebaseApp.auth();


export async function getAuthState(){
    return auth.onAuthStateChanged((user) => {
        if (user) {
            // User is signed in
            var uid = user.uid;
            user = getUserData(uid, data.BASE_URL_API);
            return user;
        }else{
            return false;
        }
    });
}

export async function resetPass(email){
    return firebase.auth().sendPasswordResetEmail(email)
    .then(() => {
        // Password reset email sent!
        console.log('mail sended');
        return true;
    })
    .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        return false;
    });
}

function login(){
    console.log('init login');
}

export async function loginMail(email, password){
    console.log('init login');
    return firebase.auth().signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
        // Signed in
        var user = userCredential.user;
        console.log('¡SESIÓN INICIADA!');
        // Obtener datos del usuario
        // Redireccionar a la vista correspondiente
        return true;
        $.ajax({
        type:'GET',
        url:'/getUser/'+user.uid,
        success: function(data) {
            var d = data.split('/')
            window.location.href = d[0]+"/index/"+user.uid
        }
    });
    })
    .catch((error) => {
        var errorCode = error.code;
        var errorMessage = error.message;
        console.log('ERROR: código: ', errorCode);
        console.log('ERROR: mensaje: ', errorMessage);
        return false;
        // Mostrar mensaje de error de credenciales
        // ...
    });
}

await async function getToken(){
    return firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
        // Send token to your backend via HTTPS
        // ...
        console.log(idToken);
        return idToken;
    }).catch(function(error) {
        // Handle error
        console.log(error);
    });
}