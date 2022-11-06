import React from "react";
import style from "./changeColor.module.scss";

export const ChangeColor = ({ onSuccess }) => {
  const handleColor = (color) => {
    console.log('dfdfdf');
    onSuccess(color);
  };

  return (
    <div className={style.changeColor}>
      <h1>Выберите цвет маркера</h1>

      <div >
        <div className={style.changeColor__wrapper}>
          <div className={style.changeColor__box}>
            <div
              onClick={() => handleColor("red")}
              className={[style.changeColor__item, style.red].join(" ")}
            ></div>
            <div
              onClick={() => handleColor("blue")}
              className={[style.changeColor__item, style.blue].join(" ")}
            ></div>
            <div
              onClick={() => handleColor("yellow")}
              className={[style.changeColor__item, style.yellow].join(" ")}
            ></div>
            <div
              onClick={() => handleColor("green")}
              className={[style.changeColor__item, style.green].join(" ")}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};
