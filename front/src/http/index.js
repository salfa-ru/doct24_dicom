import axios from 'axios';

const $file = axios.create();
const $host = axios.create();
const $authHost = axios.create();

const authInterceptor = async (config) => {
  const token = await localStorage.getItem('token')
  
  config.headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }

  return config;
};

const fileInterceptor = async (config) => {

  config.headers = {
    'Authorization': `Bearer ${token}`,
    "Content-Type": "multipart/form-data",
  }

  return config;
};

$authHost.interceptors.request.use(authInterceptor)
$file.interceptors.request.use(fileInterceptor)

export {
  $host,
  $authHost,
  $file,
};