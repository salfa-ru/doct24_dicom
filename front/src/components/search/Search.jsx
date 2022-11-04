import React from "react";
import { Input } from "../ui/input/Input";
import { ReactComponent as Icon_search } from './assets/img/search-ic.svg';
import style from "./search.module.scss";

export const Search = () => {
  return (
    <div className={style.search}>
      <div className={style.search__wrapper}>
        <Icon_search />

        <Input />
      </div>
    </div>
  );
};
