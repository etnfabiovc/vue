import axios from 'axios'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // ajuste se o Django estiver em outro host
  headers: { 'Content-Type': 'application/json' },
})
