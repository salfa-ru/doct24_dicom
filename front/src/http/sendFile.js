import { $authHost, $file } from "."
import { sendFileAPI } from "../utils/API"

export const fetchFile = async (data) => {
  let formdata = new FormData();
  formdata.append('media_file', data[0], "0002.DCM");
  formdata.append("type", "application/dicom");


  const res = await fetch(sendFileAPI(), {
    method: "POST",
    mode: "no-cors",
    headers: {
      "Content-Type": "multipart/form-data",
      'Authorization': `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY3NTQ2NTU4LCJpYXQiOjE2Njc0NjAxNTgsImp0aSI6IjcxY2U2NDkwMTE2MjQ4NDhhOTE3NTE4MTc4M2FhZjIxIiwidXNlcl9pZCI6ImQyOWQwNDdjLWM1OWYtNGJiNi05ZGU1LWRkMjZjZjJjMDM1MCJ9.i-imlbd3oRMObW8d_thdJCJYsUoQ6tKRIZU4stvWkAg`,
      'accept': 'application/json',
      //'Access-Control-Allow-Origin': '*',
      //'Connection': 'keep-alive'
      "Referrer-Policy": "origin-when-cross-origin"
    },
    body: formdata
  })

  const result = await res.json();

  console.log('result', result);

  return 'OK'
}