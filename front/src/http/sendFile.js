import axios from "axios";
import { $authHost, $file } from "."
import { sendFileAPI } from "../utils/API"

export const fetchFile = async (event) => {
  const token = await localStorage.getItem('token')
  let formData = new FormData();
  formData.append('media_file', event.target.files);

  axios
    .post("http://92.255.110.75:8000/api/v1/research/", formData, {
      headers: {
        "Content-type": "multipart/form-data",
        'accept': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    })
    .then((res) => {
      console.log(`Success` + res.data);
    })
    .catch((err) => {
      console.log(err);
    });

  return 'OK'
}