import { $authHost } from "."
import { generatePatologyAPI } from "../utils/API"

export const fetchGeneratePatology = async (data) => {
  const res = await $authHost.post(generatePatologyAPI(), data);

  console.log('res', res);
}