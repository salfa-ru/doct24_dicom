import React, { useEffect, useState } from 'react'
import DwvComponent from '../../DwvComponent';
import { List } from '../list/List';

export const Home = () => {

  const [layout, setLayout] = useState('list');
  const [patientData, setPatientData] = useState({});

  useEffect(() => {
    console.log('patientData', patientData);
  }, [patientData])

  const LayoutComponent = () => {
    switch (layout) {
      case 'dvw':
        return <DwvComponent 
                changeLayoutToList={changeLayoutToList} 
                patientData={patientData}
              />;
        break;
      case 'list':
        return <List 
                changeLayoutToDvw={changeLayoutToDvw} 
                onSelectPatient={onSelectPatient}
              />
        break;
      default:
        return <List 
                changeLayoutToDvw={changeLayoutToDvw} 
                onSelectPatient={onSelectPatient}
              />
    }
  }

  const onSelectPatient = (json) => {
    console.log('onSelectPatient');
    setPatientData(json);
    setLayout('dvw')
  }

  const changeLayoutToDvw = () => {
    console.log('changeLayout');
    setLayout('dvw');
  }

  const changeLayoutToList = () => {
    console.log('changeLayout');
    setPatientData({});
    setLayout('list');
  }

  return (
    <LayoutComponent />
  )
}
