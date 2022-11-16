import axios from 'axios';
import React, { useEffect, useState } from 'react'
import { Modals } from '../../components/ui/modals/Modals';
import DwvComponent from '../../DwvComponent';
import { fetchAuth } from '../../http/auth';
import { List } from '../list/List';

export const Home = () => {

  const [layout, setLayout] = useState('list');
  const [patientData, setPatientData] = useState({});
  const [modals, setModals] = useState(false);

  const onCloseModals = () => {
    setModals(false);
  }

  useEffect(() => {
    let token = localStorage.getItem('token');

    //if (!token) {
      fetchAuth({
        "username": "user1",
        "password": "123"
      })
    //}
    
  }, []);

  const LayoutComponent = () => {
    switch (layout) {
      case 'dvw':
        return <DwvComponent 
                changeLayoutToList={changeLayoutToList} 
                patientData={patientData}
                setModals={setModals}
              />;
        break;
      case 'list':
        return <List 
                changeLayoutToDvw={changeLayoutToDvw} 
                onSelectPatient={onSelectPatient}
                setModals={setModals}
                setPatientData={setPatientData}
              />
        break;
      default:
        return <List 
                changeLayoutToDvw={changeLayoutToDvw} 
                onSelectPatient={onSelectPatient}
                setModals={setModals}
                setPatientData={setPatientData}
              />
    }
  }

  const onSelectPatient = (json) => {
    setPatientData(json);
    setLayout('dvw')
  }

  //const onSelectPatient = (json) => {
  //  let file = 'http://92.255.110.75:8000/media/dicom_lOXB0ms.zip';
  //  downloadFileFromXML(file)
  //}

  const downloadFileFromXML = (url) => {
    var xhr = new XMLHttpRequest()

    xhr.open(
      'GET',
      url,
      true
    )

    xhr.send()

    xhr.onreadystatechange = function () {
      if (xhr.readyState !== 4) {
        return
      }
      console.log('end')
      if (xhr.status === 200) {
        console.log('result', JSON.parse(xhr.responseText))
      } else {
        console.log('err', xhr.responseText)
      }
    }
  }

  const downloadFile = (url) => {

    const config = {
      headers: {
        "Content-type": "multipart/form-data",
        'Access-Control-Allow-Origin' : '*',
        'Access-Control-Allow-Methods':'GET,PUT,POST,DELETE,PATCH,OPTIONS',
      },
      onUploadProgress: progressEvent => {
        //fillProgressBar(progressEvent)
        console.log('progressEvent', progressEvent);

        if (progressEvent.loaded === progressEvent.total) {
          console.log('100%');

          setTimeout(() => {
            console.log('норм', data);
            console.log('progressEvent', progressEvent);
            //setUploaded(true);
            //onSelectPatient(data);
          }, 3000);
        }
      }
    }
  
    axios.get(url, config)
      .then((res) => {
        let { data } = res;
        console.log('data', data);
        //data.file = selectedFile;
        //data.fileList = fileList;
        //console.log('data222', data);
        //setData(data);
        //setUploaded(true);
        //onSelectPatient(data);
      })
      .catch((err) => {
        console.log(err);
        //setModals({
        //  modal: "error",
        //  message: err,
        //});
      });
  }

  const changeLayoutToDvw = () => {
    setLayout('dvw');
  }

  const changeLayoutToList = () => {
    setPatientData({});
    setLayout('list');
  }

  return (
    <>
      <LayoutComponent />
      <Modals 
        modals={modals} 
        onCloseModals={onCloseModals}
        patientData={patientData}
      />
    </>
  )
}
