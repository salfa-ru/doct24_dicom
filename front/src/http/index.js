import axios from 'axios';

const $host = axios.create();
const $authHost = axios.create();

const authInterceptor = async (config) => {
  const token = localStorage.getItem('token')
  
  config.headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
    'accept': 'application/json'
  }

  return config;
};

$authHost.interceptors.request.use(authInterceptor)

export {
  $host,
  $authHost,
};