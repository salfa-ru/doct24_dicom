import React from "react";
import { Button } from "../ui/button/Button";
import { ReactComponent as Logo } from './assets/img/Group 126.svg';

import style from "./topPanel.module.scss";

export const TopPanel = ({
  onSave,
  changeLayoutToList
}) => {

  const onSaveAndReturn = () => {
    console.log('onSaveAndReturn');
    onSave();
    changeLayoutToList();
  }

  return (
    <div className={style.topPanel}>
      <div className={style.topPanel__logoBlock}>
        <Logo />
        <h1>id123456: Covid-19 (подлинная патология)</h1>
      </div>
      <div className={style.topPanel__btns}>
        <Button title="Сохранить и вернуться к списку" click={onSaveAndReturn}/>
        <Button title="Сохранить" click={onSave} save/>
      </div>
    </div>
  );
};
