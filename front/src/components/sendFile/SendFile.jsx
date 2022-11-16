import axios from "axios";
import React, { useRef, useState } from "react";
import { sendFileAPI } from "../../utils/API";
import { Button } from "../ui/button/Button";
import style from "./sendFile.module.scss";

export const SendFile = ({ onSelectPatient, setModals }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileList, setFileList] = useState(null);
  const [uploaded, setUploaded] = useState(false);
  const buttonRef = useRef();
  const progressBarRef = useRef();
  const [data, setData] = useState({});

  const handleChange = (event) => {
    console.log(event.target.files);
    setSelectedFile(event.target.files[0]);
    setFileList(event.target.files);
  };

  const onClickButton = () => {
    buttonRef.current.click();
  };

  const fillProgressBar = (event) => {
    let progressLine = document.querySelector('.progress');
    let current = event.loaded;
    let total = event.total;
  
    let currentPercent = (current / total) * 100;
    progressLine.style.width = `${currentPercent.toFixed(0)}%`
  }

  const handleUpload = async () => {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("media_file", selectedFile);
    const url = 'http://92.255.110.75:8000/api/v1/research/';

    const config = {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-type": "multipart/form-data",
        accept: "application/json",
      },
      onUploadProgress: progressEvent => {
        fillProgressBar(progressEvent)

        if (progressEvent.loaded === progressEvent.total) {
          console.log('100%');

          //setTimeout(() => {
          //  console.log('норм', data);
          //  console.log('progressEvent', progressEvent);
          //}, 3000);
        }
      }
    }
  
    axios.post(url, formData, config)
      .then((res) => {
        let { data } = res;
        data.file = selectedFile;
        data.fileList = fileList;
        console.log('data222', data);
        setData(data);
        setUploaded(true);
        onSelectPatient(data);
      })
      .catch((err) => {
        console.log(err);
        setModals({
          modal: "error",
          message: err,
        });
      });

    //axios
    //  .post("http://92.255.110.75:8000/api/v1/research/", formData, {
    //    headers: {
    //      "Content-type": "multipart/form-data",
    //      accept: "application/json",
    //      Authorization: `Bearer ${token}`,
    //    },
    //  })
    //  .then((res) => {
    //    let { data } = res;
    //    data.file = selectedFile;
    //    data.fileList = fileList;
    //    setUploaded(true);

    //    onSelectPatient(data);
    //  })
    //  .catch((err) => {
    //    console.log(err);
    //    setModals({
    //      modal: "error",
    //      message: err,
    //    });
    //  });

    //const result = await res.json();
  };

  return (
    <div className={style.SendFile}>
      <div 
        className={[style.progressBar, 'progress'].join(' ')} 
        ref={progressBarRef}
      ></div>
      <input
        type="file"
        onChange={handleChange}
        ref={buttonRef}
        //accept="image/*,.png,.jpg,.gif"
        className={style.hidden}
      />

      {!selectedFile ? (
        <Button title="Загрузить" download={true} click={onClickButton} />
      ) : (
        <Button title="Отправить" download={true} click={handleUpload} />
      )}
    </div>
  );
};
