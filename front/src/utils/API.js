const baseURL = 'http://92.255.110.75:8000/api/v1';
//const baseURL = 'http://localhost:7000';

export const authAPI = () => baseURL + '/authentification/token/';
export const sendFileAPI = () => baseURL + '/research';
export const sendSaveDataAPI = () => baseURL + '/labels/';
export const getListAPI = () => baseURL + '/research?page_size=20';
export const getCurrentMetadataAPI = () => baseURL + '/labels/?research__id=';
export const updateCurrentMetadataAPI = () => baseURL + '/labels/';
export const generatePatologyAPI = () => baseURL + '/ai/processing/';
export const deleteAPI = () => baseURL + '/research/';