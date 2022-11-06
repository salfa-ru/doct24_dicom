import React from "react";
import { ListBox } from "../../components/list/ListBox";
import { Search } from "../../components/search/Search";
import { SendFile } from "../../components/sendFile/SendFile";
import { Button } from "../../components/ui/button/Button";
import { Card } from "../../components/ui/card/Card";
import style from "./list.module.scss";

export const List = ({
  changeLayoutToDvw,
  onSelectPatient,
  setModals,
  setPatientData
}) => {
  return (
    <div className="wrapper">
      <div className="container">
        <div className={style.list}>
          <div className={style.list__topPanel}>
            <Search />
            <SendFile 
              onSelectPatient={onSelectPatient} 
              setModals={setModals}
            />
          </div>

          <ListBox 
            onSelectPatient={onSelectPatient} 
            setModals={setModals}
            setPatientData={setPatientData}
          />

        </div>
      </div>
    </div>
  );
};
