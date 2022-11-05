import React, { useEffect, useState } from 'react'
import { fetchList } from '../../http/data'
import { Card } from '../ui/card/Card'

export const ListBox = ({
  onSelectPatient
}) => {

  const [list, setList] = useState([]);

  const getList = async () => {
    let res = await fetchList();

    console.log('fetchList', res);

    setList(res.results);
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
            />
          ))
        ) : ('нет данных')}
      </div>
    </div>
  )
}
