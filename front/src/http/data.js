import { $authHost, $host } from "."
import { getListAPI, sendSaveDataAPI } from "../utils/API"

export const fetchSaveData = async (data) => {
  const res = await $authHost.post(sendSaveDataAPI(), data);

  console.log('res', res);
}

export const fetchList = async () => {
  const res = await $authHost.get(getListAPI());

  if (res.status === 200) {
    return res.data
  }
}