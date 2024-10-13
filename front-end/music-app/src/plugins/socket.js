import { io } from "socket.io-client";

const socket = io("http://127.0.0.1:5000"); // Flask server 的位址
export default socket;
