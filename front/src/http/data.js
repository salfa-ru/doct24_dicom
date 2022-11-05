import { $authHost, $host } from ".";
import { getListAPI, sendSaveDataAPI } from "../utils/API";

export const fetchSaveData = async (data) => {
  const res = await $authHost.put(sendSaveDataAPI() + '/3', data);
};

export const fetchList = async () => {
  const res = await $authHost.get(getListAPI());

  console.log('fetchList', res);

  if (res.status === 200) {
    return res.data;
  }

  return res;
};

export const fetchPatientDicom = async (url) => {
  console.log("fetchPatientDicom", url);

  //const response = await fetch(url, {mode: 'no-cors'});
  //const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
};
