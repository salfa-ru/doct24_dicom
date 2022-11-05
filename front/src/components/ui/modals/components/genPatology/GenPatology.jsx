import React, { useState } from "react";
import { fetchGeneratePatology } from "../../../../../http/generate";
import { Button } from "../../../button/Button";
import { Select } from "../../../select/Select";
import style from './genPatology.module.scss';

export const GenPatology = ({
  patientData
}) => {
  const [patology, setPatology] = useState({ id: 1, name: 'covid' });
  const [localization, setLocalization] = useState({});
  const [segments, setSegments] = useState({});
  const [quantity, setQuantity] = useState({});
  const [size, setSize] = useState({});

  const onSubmitGeneration = () => {
    console.log('patientData', patientData);

    //let data = {
    //  id: 1,
    //  patology: 'covid',
    //  segments: [segments.id],
    //  quantity: 1,
    //  size: 1,
    //}

    let data = {
      "data": {
        "id": 1,
        "patology": "covid",
        "segments": [segments.id],
        "quantity": 1,
        "size": 1
      }
   }

    console.log('data', data);

    fetchGeneratePatology(data);
  }

  return (
    <>
      <h1>Выберите параметры патологии</h1>

      <div className={style.genPatology__headBlock}>
        <div className={style.genPatology__item}>
          <Select
            title="Патология:" 
            list={[
              { id: 1, name: 'covid' },
            ]}
            item={patology}
            update={(data) => setPatology(data)}
          />
        </div>
      </div>

      <div className={style.genPatology__list}>
        <div className={style.genPatology__item}>
          <Select
          title="Локализация:"
            list={[
              { id: 1, name: "Левое легкое" },
              { id: 2, name: "Правое легкое" },
            ]}
            item={localization}
            update={(data) => setLocalization(data)}
          />
        </div>
        <div className={style.genPatology__item}>
        <Select
          title="Доля:" 
          list={[
            { id: 1, name: "Верхняя доля правого лёгкого" },
            { id: 2, name: "Средняя доля правого лёгкого" },
            { id: 3, name: "Нижняя доля правого лёгкого" },
            { id: 4, name: "Верхняя доля левого лёгкого" },
            { id: 5, name: "Нижняя доля левого лёгкого" },
          ]}
          item={segments}
          update={(data) => setSegments(data)}
        />
        </div>
        <div className={style.genPatology__item}>
        <Select
          title="Количество:" 
          list={[
            { id: 1, name: 1 },
          ]}
          item={quantity}
          update={(data) => setQuantity(data)}
        />
        </div>
        <div className={style.genPatology__item}>
        <Select
          title="Размеры:" 
          list={[
            { id: 1, name: 1 },
          ]}
          item={size}
          update={(data) => setSize(data)}
        />
        </div>       
      </div>
      

      <Button 
        title="Сгенерировать"
        click={() => onSubmitGeneration()}
      />
    </>
  );
};
