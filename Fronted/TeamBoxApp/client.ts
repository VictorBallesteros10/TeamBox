import axios from "axios";
import { Platform } from "react-native";

// Ajusta aquí según donde corra tu backend:
// para web -> localhost; para móvil -> la IP de tu máquina (reemplaza 192.168.1.X)
const LOCAL_IP = "192.168.56.1"; // <-- cambia por tu IP de PC
export const API_BASE =
  Platform.OS === "web" ? "http://localhost:8000" : `http://${LOCAL_IP}:8000`;

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 10_000,
});
