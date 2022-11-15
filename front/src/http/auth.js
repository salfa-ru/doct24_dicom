import { $host } from ".";
import { authAPI } from "../utils/API";

export const fetchAuth = async (data) => {
  try {
    const res = await $host.post(authAPI(), data);

    if (res.data.access) {
      localStorage.setItem("token", res.data.access);
    }
  } catch (error) {
    console.log("get token error", error);
  }
};
