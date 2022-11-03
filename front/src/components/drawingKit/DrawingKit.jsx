import React from 'react'
import style from './drawingKit.module.scss'
import { ReactComponent as Icon_brightness } from './assets/img/brightness-ic.svg';
import { ReactComponent as Icon_contrast } from './assets/img/contrast-ic.svg';
import { ReactComponent as Icon_move } from './assets/img/move-ic.svg';
import { ReactComponent as Icon_pencil } from './assets/img/pencil-ic.svg';
import { ReactComponent as Icon_zoom } from './assets/img/scale-ic.svg';
import { ReactComponent as Icon_colorFill } from './assets/img/bxs_color-fill.svg';

export const DrawingKit = ({
  onClick
}) => {
  return (
    <div className={style.drawingKit}>
      <div className={style.drawingKit__wrapper}>
        <ul>
          <li><Icon_zoom onClick={() => onClick('zoom')}/></li>
          <li><Icon_contrast onClick={() => onClick('contrast')}/></li>
          <li><Icon_move onClick={() => onClick('Scroll')}/></li>
          <li><Icon_pencil onClick={() => onClick('pencil')}/></li>
          <li><Icon_colorFill onClick={() => onClick('colorFill')}/></li>
        </ul>
      </div>
    </div>
  )
}
