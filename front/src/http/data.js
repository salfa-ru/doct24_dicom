import { $authHost, $host } from ".";
import { deleteAPI, getCurrentMetadataAPI, getListAPI, sendSaveDataAPI, updateCurrentMetadataAPI } from "../utils/API";

export const fetchSaveData = async (data) => {
  const res = await $authHost.post(sendSaveDataAPI(), data);

  if (res.status === 201) {
    return res
  } else {
    console.log('error');
  }
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
};

export const fetchDeleteReasearch = async (id) => {
  const res = await $authHost.delete(deleteAPI() + id);

  console.log('res', res);
}

export const fetchCurrentMetadata = async (id) => {
  try {
    const res = await $authHost.get(getCurrentMetadataAPI() + id + '/')

    if (res.status === 200) {
      return res.data
    }
  } catch (error) {
    console.log('error', error);
  }

}

export const fetchUpdateCurrentMetadata = async (id, data) => {
  try {
    const res = await $authHost.put(updateCurrentMetadataAPI() + id + '/', data)

    if (res.status === 200) {
      return res.data
    }
  } catch (error) {
    console.log('error', error);
    fetchSaveData(data);
  }

}