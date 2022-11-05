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
    fetchAuth({
      "username": "user1",
      "password": "123"
    })
  }, []);

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
                setModals={setModals}
              />
        break;
      default:
        return <List 
                changeLayoutToDvw={changeLayoutToDvw} 
                onSelectPatient={onSelectPatient}
                setModals={setModals}
              />
    }
  }

  const onSelectPatient = (json) => {
    setPatientData(json);
    setLayout('dvw')
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
