import { $authHost } from "."
import { generatePatologyAPI } from "../utils/API"

export const fetchGeneratePatology = async (data) => {
  try {
    const res = await $authHost.post(generatePatologyAPI(), data);

    return res;
  } catch (error) {
    console.log('error');
  }
}