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
  empty,
  disabled,
  green,
  trash
}) => {
  return <div 
            className={[
              empty ? style.button__empty : style.button,
              green ? style.green : '',
              trash ? style.trash : '',
            ].join(' ')}
            onClick={() => click()}
            disabled={disabled}
        >
          {title} 
          {save && <Icon_save />}
          {download && <Icon_download />}
        </div>;
};
