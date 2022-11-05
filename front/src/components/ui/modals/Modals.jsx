import React from "react";
import { Button } from "../button/Button";
import { Select } from "../select/Select";
import { Error } from "./components/error/Error";
import { GenPatology } from "./components/genPatology/GenPatology";
import style from "./modals.module.scss";

export const Modals = ({ 
  modals, 
  onCloseModals, 
  patientData 
}) => {
  const ModalsComponent = () =>
    modals ? (
      <div className={style.modals}>
        <div className={style.modals__wrapper}>
          <div className={style.modals__header}>
            <Button title="X" click={onCloseModals} empty />
          </div>
          <div className={style.modals__body}>
            <Switcher />
          </div>
        </div>
      </div>
    ) : (
      ""
    );

  const Switcher = () => {
    if (!modals) {
      return;
    }

    switch (modals?.modal) {
      case "genPatology":
        return <GenPatology patientData={patientData} />;
      case "error":
        return <Error message={modals?.message}/>;
      default:
        return;
    }
  };

  return <ModalsComponent />;
};
