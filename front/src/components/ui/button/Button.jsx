import React from "react";
import { ReactComponent as Icon_save } from './assets/img/save.svg';
import { ReactComponent as Icon_download } from './assets/img/upload-ic.svg';
import style from "./button.module.scss";

export const Button = ({
  main,
  download,
  save,
  title = 'ButtonName',
  click,
}) => {
  return <div 
            className={style.button}
            onClick={() => click()}
        >
          {title} 
          {save && <Icon_save />}
          {download && <Icon_download />}
        </div>;
};
