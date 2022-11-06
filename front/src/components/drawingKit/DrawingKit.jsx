import React, { useState } from "react";
import style from "./drawingKit.module.scss";
import { ReactComponent as Icon_brightness } from "./assets/img/brightness-ic.svg";
import { ReactComponent as Icon_contrast } from "./assets/img/contrast-ic.svg";
import { ReactComponent as Icon_move } from "./assets/img/move-ic.svg";
import { ReactComponent as Icon_pencil } from "./assets/img/pencil-ic.svg";
import { ReactComponent as Icon_zoom } from "./assets/img/scale-ic.svg";
import { ReactComponent as Icon_colorFill } from "./assets/img/bxs_color-fill.svg";
import { ChangeColor } from "../ui/modals/components/changeColor/ChangeColor";

export const DrawingKit = ({ 
  onClick,
  setModals,
  onChangeDrawColor
}) => {
  const [currentItem, setCurrentItem] = useState(null);
  const [popupChangeColor, setPopupChangeColor] = useState(false);

  const handleCurrentItem = (item) => {
    setCurrentItem(item);
    onClick(item);

    if (item === 'colorFill') {
      //setModals({
      //  modal: 'changeColor',
      //  onSuccess: () => onChangeDrawColor()
      //})
      setPopupChangeColor(!popupChangeColor)
    }
  };

  return (
    <div className={style.drawingKit}>
      <div className={style.drawingKit__wrapper}>
        <ul>
          <li onClick={() => handleCurrentItem("zoom")}>
            <Icon_zoom
              className={currentItem === "zoom" ? style.activeKit : ""}
              fill={"black"}
            />
          </li>
          <li onClick={() => handleCurrentItem("contrast")}>
            <Icon_contrast
              className={currentItem === "contrast" ? style.activeKit : ""}
              fill={"black"}
            />
          </li>
          <li onClick={() => handleCurrentItem("Scroll")}>
            <Icon_move
              fill={"black"}
              className={currentItem === "Scroll" ? style.activeKit : ""}
            />
          </li>
          <li onClick={() => handleCurrentItem("pencil")}>
            <Icon_pencil
              fill={"black"}
              className={currentItem === "pencil" ? style.activeKit : ""}
            />
          </li>
          <li onClick={() => handleCurrentItem("colorFill")}>
            <Icon_colorFill
              fill={"black"}
              className={currentItem === "colorFill" ? style.activeKit : ""}
            />
            {popupChangeColor ? (
              <ChangeColor onSuccess={onChangeDrawColor}/>
            ) : ('')}
            
          </li>
        </ul>
      </div>
    </div>
  );
};
