import React, { useEffect, useState } from 'react'
import { fetchList } from '../../http/data'
import { Card } from '../ui/card/Card'

export const ListBox = ({
  onSelectPatient,
  setModals,
  setPatientData
}) => {

  const [list, setList] = useState([]);

  const getList = async () => {
    let res = await fetchList();

    if (res) {
      setList(res.results);
    }
  }

  const filteredList = (id) => {
    setList([...list.filter(el => el.id !== id)]);
  }

  useEffect(() => {
    getList();
  }, [])

  return (
    <div className="listBox">
       <h1>Исследования</h1>

 <div className='flex gap20 wrap'>
        {!!list.length ? (
          list.map(item => (
            <Card 
              item={item} 
              onSelectPatient={onSelectPatient}
              key={item.id}
              setModals={setModals}
              setPatientData={setPatientData}
              filteredList={filteredList}
            />
          ))
        ) : ('нет данных')}
      </div>
    </div>
  )
}
