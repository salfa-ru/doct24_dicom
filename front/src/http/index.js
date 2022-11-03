import axios from 'axios';

const $file = axios.create();
const $host = axios.create();
const $authHost = axios.create();
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3NTQ2NTU4LCJpYXQiOjE2Njc0NjAxNTgsImp0aSI6IjcxY2U2NDkwMTE2MjQ4NDhhOTE3NTE4MTc4M2FhZjIxIiwidXNlcl9pZCI6ImQyOWQwNDdjLWM1OWYtNGJiNi05ZGU1LWRkMjZjZjJjMDM1MCJ9.i-imlbd3oRMObW8d_thdJCJYsUoQ6tKRIZU4stvWkAg';


const authInterceptor = async (config) => {
  //const token = await localStorage.getItem('token')
  
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