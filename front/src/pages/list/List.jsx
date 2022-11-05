import React from "react";
import { ListBox } from "../../components/list/ListBox";
import { Search } from "../../components/search/Search";
import { SendFile } from "../../components/sendFile/SendFile";
import { Button } from "../../components/ui/button/Button";
import { Card } from "../../components/ui/card/Card";
import style from "./list.module.scss";

export const List = ({
  changeLayoutToDvw,
  onSelectPatient
}) => {
  return (
    <div className="wrapper">
      <div className="container">
        <div className={style.list}>
          <div className={style.list__topPanel}>
            <Search />
            <SendFile onSelectPatient={onSelectPatient} />
          </div>

          <ListBox onSelectPatient={onSelectPatient} />

        </div>
      </div>
    </div>
  );
};
