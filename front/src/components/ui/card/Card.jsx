import React from "react";
import { fetchDeleteReasearch } from "../../../http/data";
import { ReactComponent as Icon_trash } from "./assets/img/gg_trash.svg";
import { ReactComponent as Icon_create } from "./assets/img/gridicons_create.svg";
import Icon_cardImage from "./assets/img/Rectangle_35.png";
import style from "./card.module.scss";

export const Card = ({ 
  item, 
  onSelectPatient,
  setModals,
  setPatientData
}) => {
  const { patient_code, updated_at, id } = item;

  const getResearchData = () => {
    return new Date(updated_at).toLocaleDateString();
  }

  const onDeleteResearch = () => {
    fetchDeleteReasearch(item.id);
  }

  const onGenPatology = () => {
    setPatientData(item);

    setModals({
      modal: 'genPatology',
      onSuccess: () => setModals({
        modal: 'success',
        messageSuccess: 'Запрос на обработку исследования успешно отправлен!'
      }),
      onError: () => setModals({
        modal: 'error',
      }),
      
    })
  }

  return (
    <div className={style.card} key={item.id}>
      <div className={style.card__wrapper}>
        <div className={style.card__top}>
          <div className={style.card__top_title}>id{id}</div>
          <div className={style.card__top_icons}>
            <Icon_create 
              onClick={() => onGenPatology()}
            />
            <Icon_trash 
              onClick={() => onDeleteResearch()}
            />
          </div>
        </div>

        <div 
          onClick={() => onSelectPatient(item)}
          className={style.card__touchZone}
        >
          <div className={style.card__imageBlock}>
            <img src={Icon_cardImage} alt="" />
          </div>

          <div className={style.card__info}>
            <div className={style.card__info_title}>DICOM</div>
            <div>{getResearchData()}</div>
          </div>
        </div>

        <div className={style.card__authors}>
          <div className={style.card__authors_title}>Разметка</div>
          <div className={style.card__authors_list}>
            <ul>
              <li>Сидорова С.С</li>
              <li>Иванова А.А.</li>
              <li>Назначить врача</li>
              <li>Авторазметка</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
