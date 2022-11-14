import { $authHost, $host } from ".";
import { deleteAPI, getListAPI, sendSaveDataAPI } from "../utils/API";

export const fetchSaveData = async (data) => {
  const res = await $authHost.post(sendSaveDataAPI(), data);

  console.log('res', res);
};

export const fetchList = async () => {
  try {
    const res = await $authHost.get(getListAPI());

    if (res.status === 200) {
      return res.data;
    }

    return res;
  } catch (error) {
    console.log("get list reseach error", error);
  }
};

export const fetchPatientDicom = async (url) => {
  console.log("fetchPatientDicom", url);

  //const response = await fetch(url, {mode: 'no-cors'});
  //const reader = response.body.pipeThrough(new TextDecoderStream()).getReader();
};

export const fetchDeleteReasearch = async (id) => {
  const res = await $authHost.delete(deleteAPI() + id);

  console.log('res', res);
}