import { initializeApp } from "https://www.gstatic.com/firebasejs/12.12.1/firebase-app.js";
import {
  getDatabase,
  ref,
  onValue,
  set,
  update,
  onDisconnect,
  serverTimestamp
} from "https://www.gstatic.com/firebasejs/12.12.1/firebase-database.js";

const firebaseConfig = {
  apiKey: "AIzaSyDwIgwOWsAz9GI_m588x2_BltisPNpY0Wg",
  authDomain: "lystex-21ee1.firebaseapp.com",
  databaseURL: "https://lystex-21ee1-default-rtdb.firebaseio.com/",
  projectId: "lystex-21ee1",
  storageBucket: "lystex-21ee1.firebasestorage.app",
  messagingSenderId: "111382113577",
  appId: "1:111382113577:web:2fd2856157605dd465db38"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase(app);

export { db, ref, onValue, set, update, onDisconnect, serverTimestamp };