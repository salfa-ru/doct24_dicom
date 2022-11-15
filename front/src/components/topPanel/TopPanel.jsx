import React, { useState } from "react";
import { Button } from "../ui/button/Button";
import { ReactComponent as Logo } from './assets/img/Group 126.svg';

import style from "./topPanel.module.scss";

export const TopPanel = ({
  onSave,
  changeLayoutToList,
  patientData = {},
  getCurrentMetadata,
  sendUpdateCurrentMetadata
}) => {

  const [downloadMetadataStatus, setDownloadMetadataStatus] = useState(false);

  const onSaveAndReturn = () => {
    onSave();
    changeLayoutToList();
  }

  const getMetadata = async () => {
    let res = await getCurrentMetadata();

    if (res.status === 200) {
      setDownloadMetadataStatus(true);
    }
  }

  return (
    <div className={style.topPanel}>
      <div className={style.topPanel__logoBlock}>
        <Logo />
        <h1>id: {patientData.id}</h1>
      </div>
      <div className={style.topPanel__btns}>

        {!downloadMetadataStatus ? (
           <Button title="Получить ранее сохраненную разметку" click={() => getMetadata()}/>
        ) : (
          <Button title="Данные успешно получены" disabled green />
        )}
       
        <Button title="Сохранить и вернуться к списку" click={onSaveAndReturn}/>
        <Button title="Сохранить" click={onSave} save/>
      </div>
    </div>
  );
};
