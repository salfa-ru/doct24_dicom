import React, { useState } from "react";
import { useEffect } from "react";
import { ReactComponent as SvgArrow } from './assets/img/arrow.svg';
import style from "./select.module.scss";

export const Select = ({
  title = 'Название',
  list = [],
  item = {},
  update,
}) => {
  const [dropdown, setDropdown] = useState(false);
  const [activeItem, setActiveItem] = useState({});
  const ListComponent = () => (
    <div className={style.dropDown}>
        <ul>
          {list.map(el => (
            <li 
              key={el.id}
              className={el?.id === activeItem?.id ? style['active'] : ''}
              onClick={() => update(el)}
            >{el.name}</li>
          ))}
        </ul>
    </div>
  )

  const ActiveItemComponent = () => {
    if (activeItem?.id) {
      return activeItem.name
    } else {
      return title
    }
  }

  useEffect(() => {
    if (activeItem.id !== item.id) {
      setActiveItem(item); 
    }
  }, [item])



  return (
    <div className={style.select}>
      {/*<div className={style.select__title}>{title}</div>*/}
      <div className={style.select__wrapper} onClick={() => setDropdown(!dropdown)}>
        <div className={style.select__info}>
          <ActiveItemComponent />
        </div>
        <div className={style.select__iconArrow}>
          <SvgArrow />
        </div>

        {dropdown && <ListComponent />}

      </div>
        
    </div>
  );
};
