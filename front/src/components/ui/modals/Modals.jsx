import React from "react";
import { Button } from "../button/Button";
import { Select } from "../select/Select";
import { ChangeColor } from "./components/changeColor/ChangeColor";
import { Error } from "./components/error/Error";
import { GenPatology } from "./components/genPatology/GenPatology";
import { Success } from "./components/success/Success";
import style from "./modals.module.scss";

export const Modals = ({ 
  modals, 
  onCloseModals, 
  patientData 
}) => {
  console.log('modals', modals);
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
        return <GenPatology 
                  patientData={patientData} 
                  onCloseModals={onCloseModals}
                  onSuccess={modals.onSuccess}
                  onError={modals.onError}
                  messageSuccess={modals.messageSuccess}
                  modals={modals}
                />;
      case "error":
        return <Error message={modals?.message}/>;
      case "success":
        return <Success messageSuccess={modals.messageSuccess} />;
      case "changeColor":
        return <ChangeColor onSuccess={modals.onSuccess} />;
      default:
        return;
    }
  };

  return <ModalsComponent />;
};
