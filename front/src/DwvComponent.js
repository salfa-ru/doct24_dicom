import React from "react";
import PropTypes from "prop-types";
import { withStyles, useTheme } from "@mui/styles";
import Typography from "@mui/material/Typography";

import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import LinearProgress from "@mui/material/LinearProgress";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";

import Link from "@mui/material/Link";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import IconButton from "@mui/material/IconButton";
import CloseIcon from "@mui/icons-material/Close";

import Dialog from "@mui/material/Dialog";
import AppBar from "@mui/material/AppBar";
import Slide from "@mui/material/Slide";
import Toolbar from "@mui/material/Toolbar";

import TagsTable from "./TagsTable";

import "./DwvComponent.css";
import dwv from "dwv";
import style from "./components/layoutDRW/layoutDRW.module.scss";
import { Select } from "./components/ui/select/Select";
import { DrawingKit } from "./components/drawingKit/DrawingKit";
import { TopPanel } from "./components/topPanel/TopPanel";
import { fetchFile } from "./http/sendFile";
import { fetchPatientDicom, fetchSaveData } from "./http/data";
import { $authHost } from "./http";

// Image decoders (for web workers)
dwv.image.decoderScripts = {
  jpeg2000: `${process.env.PUBLIC_URL}/assets/dwv/decoders/pdfjs/decode-jpeg2000.js`,
  "jpeg-lossless": `${process.env.PUBLIC_URL}/assets/dwv/decoders/rii-mango/decode-jpegloss.js`,
  "jpeg-baseline": `${process.env.PUBLIC_URL}/assets/dwv/decoders/pdfjs/decode-jpegbaseline.js`,
  rle: `${process.env.PUBLIC_URL}/assets/dwv/decoders/dwv/decode-rle.js`,
};

const styles = (theme) => ({
  appBar: {
    position: "relative",
  },
  title: {
    flex: "0 0 auto",
  },
  tagsDialog: {
    minHeight: "90vh",
    maxHeight: "90vh",
    minWidth: "90vw",
    maxWidth: "90vw",
  },
  iconSmall: {
    fontSize: 20,
  },
});

export const TransitionUp = React.forwardRef((props, ref) => (
  <Slide direction="up" {...props} ref={ref} />
));

class DwvComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      versions: {
        dwv: dwv.getVersion(),
        react: React.version,
      },
      tools: {
        Scroll: {},
        ZoomAndPan: {},
        WindowLevel: {},
        Draw: {
          options: ["Ruler"],
          type: "factory",
          events: ["drawcreate", "drawchange", "drawmove", "drawdelete"],
        },
      },
      toolNames: [],
      selectedTool: "Select Tool",
      loadProgress: 0,
      dataLoaded: false,
      dwvApp: null,
      modeDrawing: false,
      drawModeCanvas: false,
      drawColor: "red",
      metaData: [],
      showDicomTags: false,
      toolMenuAnchorEl: null,
      dropboxDivId: "dropBox",
      dropboxClassName: "dropBox",
      borderClassName: "dropBoxBorder",
      hoverClassName: "hover",
      ctx: "",
      metaDataDraw: [],
      metaPatology: {},
      metaLocalization: {},
      metaKolvo: {},
      metaDolya: {},
      metaSize: {},
      patientData: this.props.patientData,
      incomingFileFromBack: false,
    };
  }

  render() {
    const { classes, changeLayoutToList } = this.props;
    const {
      versions,
      tools,
      toolNames,
      loadProgress,
      dataLoaded,
      metaData,
      toolMenuAnchorEl,
    } = this.state;

    const toolsMenuItems = toolNames.map((tool) => (
      <MenuItem
        onClick={this.handleMenuItemClick.bind(this, tool)}
        key={tool}
        value={tool}
      >
        {tool}
      </MenuItem>
    ));

    return (
      <div className="wrapper">
        <div className="container">
          <LinearProgress variant="determinate" value={loadProgress} />

          <TopPanel
            onSave={this.toggleButtonSave}
            changeLayoutToList={changeLayoutToList}
            patientData={this.state.patientData}
          />

          {/*<div >
          <div>Разметка Ивановой А.А.</div>
          <div>Разметка Петровой В.С.</div>
          <div>Разметка Соколовой И.Д.</div>
        </div>*/}

          <div className={style.dataMetka__container}>
            <div className={style.dataMetka}>
              {/*<h2>Данные разметки:</h2>*/}

              <div className={style.dataMetka__list}>
                <Select
                  title="Патология:"
                  list={[
                    { id: 1, name: "COVID-19" },
                    { id: 2, name: "Рак лёгкого" },
                    { id: 3, name: "Метастатиче ское поражение лёгких" },
                  ]}
                  item={this.state.metaPatology}
                  update={(data) => this.setState({ metaPatology: data })}
                />

                <Select
                  title="Локализация:"
                  list={[
                    { id: 1, name: "Верхняя доля правого лёгкого" },
                    { id: 2, name: "Средняя доля правого лёгкого" },
                    { id: 3, name: "Нижняя доля правого лёгкого" },
                    { id: 4, name: "Верхняя доля левого лёгкого" },
                    { id: 5, name: "Нижняя доля левого лёгкого" },
                  ]}
                  item={this.state.metaLocalization}
                  update={(data) => this.setState({ metaLocalization: data })}
                />

                <Select title="Доля:" />

                <Select
                  title="Количество:"
                  list={[
                    { id: 1, name: "Единичное (1-3)" },
                    { id: 2, name: "Немногочисленные (4-10)" },
                    { id: 3, name: "Многочисленные (>10)" },
                  ]}
                  item={this.state.metaKolvo}
                  update={(data) => this.setState({ metaKolvo: data })}
                />

                <Select
                  title="Размеры:"
                  list={[
                    { id: 1, name: "5 мм" },
                    { id: 2, name: "5-10 мм" },
                    { id: 3, name: "10-20 мм" },
                    { id: 4, name: ">20 мм" },
                  ]}
                  item={this.state.metaSize}
                  update={(data) => this.setState({ metaSize: data })}
                />

                <Select title="Подлинность:" />
              </div>
            </div>
          </div>
          <a hidden href="#" className="downloadDicomLink hiddenModule">
            скачать
          </a>
          <button
            hidden
            className="save hiddenModule"
            onClick={() => this.onSave()}
          >
            save
          </button>
          <input
            type="file"
            name="file"
            className="downloadFile hiddenModule"
          />

          <div className="workspace">
            <div className="toolbar">
              <DrawingKit onClick={(func) => this.onClickDrawingKit(func)} />
            </div>
            <div id="dwv">
              <div id="layerGroup0" className="layerGroup">
                <div id="dropBox"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  componentDidMount() {
    // create app
    var app = new dwv.App();
    // initialise app
    app.init({
      dataViewConfigs: { "*": [{ divId: "layerGroup0" }] },
      tools: this.state.tools,
    });

    // load events
    let nLoadItem = null;
    let nReceivedError = null;
    let nReceivedAbort = null;
    let isFirstRender = null;
    app.addEventListener("loadstart", (/*event*/) => {
      // reset flags
      nLoadItem = 0;
      nReceivedError = 0;
      nReceivedAbort = 0;
      isFirstRender = true;
      // hide drop box
      this.showDropbox(app, false);
    });
    app.addEventListener("loadprogress", (event) => {
      this.setState({ loadProgress: event.loaded });
    });
    app.addEventListener("renderend", (/*event*/) => {
      if (isFirstRender) {
        isFirstRender = false;
        // available tools
        let names = [];
        for (const key in this.state.tools) {
          if (
            (key === "Scroll" && app.canScroll()) ||
            (key === "WindowLevel" && app.canWindowLevel()) ||
            (key !== "Scroll" && key !== "WindowLevel")
          ) {
            names.push(key);
          }
        }
        this.setState({ toolNames: names });
        this.onChangeTool(names[0]);
      }
    });
    app.addEventListener("load", (/*event*/) => {
      // set dicom tags
      this.setState({ metaData: dwv.utils.objectToArray(app.getMetaData(0)) });
      // set data loaded flag
      this.setState({ dataLoaded: true });
    });
    app.addEventListener("loadend", (/*event*/) => {
      if (nReceivedError) {
        this.setState({ loadProgress: 0 });
        alert("Received errors during load. Check log for details.");
        // show drop box if nothing has been loaded
        if (!nLoadItem) {
          this.showDropbox(app, true);
        }
      }
      if (nReceivedAbort) {
        this.setState({ loadProgress: 0 });
        alert("Load was aborted.");
        this.showDropbox(app, true);
      }
    });
    app.addEventListener("loaditem", (/*event*/) => {
      ++nLoadItem;
    });
    app.addEventListener("error", (event) => {
      console.error(event.error);
      ++nReceivedError;
    });
    app.addEventListener("abort", (/*event*/) => {
      ++nReceivedAbort;
    });

    // handle key events
    app.addEventListener("keydown", (event) => {
      app.defaultOnKeydown(event);
    });
    // handle window resize
    window.addEventListener("resize", app.onResize);

    // store
    this.setState({ dwvApp: app });

    // setup drop box
    this.setupDropbox(app);

    // possible load from location
    dwv.utils.loadFromUri(window.location.href, app);

    if (this.state.patientData?.file) {
      this.onDrop2({
        patient: true,
        fileList: this.state.patientData.fileList,
      });

      //this.downloadDicom(this.state.patientData.file)
    } else if (this.state.patientData?.id && !this.state.patientData.file) {
      this.onDrop2({
        patient: false,
        media_file: this.state.patientData.media_file,
      });
    }
  }

  onClickDrawingKit(func) {
    switch (func) {
      case "pencil":
        this.handleModeDrawing("pencil");
        break;
      case "contrast":
        this.handleModeDrawing("WindowLevel");
        break;
      case "zoom":
        this.handleModeDrawing("ZoomAndPan");
        break;
      case "Scroll":
        this.handleModeDrawing("Scroll");
        break;
      case "colorFill":
        this.onChangeColorFill();
        break;
      default:
        break;
    }
  }

  onChangeColorFill() {
    console.log("colorfill");
  }

  toggleButtonSave() {
    let button = document.querySelector(".save");
    button.click();
  }

  onSave = () => {
    let data = this.createData();

    fetchSaveData(data);
  };

  createData = () => {
    let data = {
      metaPatology: this.state.metaPatology,
      metaLocalization: this.state.metaLocalization,
      metaKolvo: this.state.metaKolvo,
      metaDolya: this.state.metaDolya,
      metaSize: this.state.metaSize,
      metaData: this.state.metaDataDraw,
    };

    return data;
  };

  /**
   * Handle a change tool event.
   * @param {string} tool The new tool name.
   */
  onChangeTool = (tool) => {
    if (this.state.dwvApp) {
      this.setState({ selectedTool: tool });
      this.state.dwvApp.setTool(tool);
      if (tool === "Draw") {
        this.onChangeShape(this.state.tools.Draw.options[0]);
      }
    }
  };

  startDraw() {
    this.setState({ modeDrawing: true });
    this.onChangeTool("Draw");
    this.modeCanvasOn();
  }

  stopDraw(func) {
    this.setState({ modeDrawing: false });
    this.onChangeTool(func);
    this.modeCanvasOff();
  }

  handleModeDrawing = (func) => {
    if (func === "pencil" && this.state.modeDrawing === true) {
      return;
    } else if (func === "pencil" && this.state.modeDrawing === false) {
      this.startDraw();
    } else if (func !== "pencil" && this.state.modeDrawing === true) {
      this.stopDraw(func);
    } else if (func !== "pencil" && this.state.modeDrawing === false) {
      this.onChangeTool(func);
    }
  };

  fillThis = (x, y, sizeX, sizeY) => {
    const canvas = this.getCanvas();
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "red";
    ctx.fillRect(x, y, sizeX, sizeY);
  };

  logsAfterFill = ({ x, y, sizeX, sizeY }) => {
    this.setState({
      metaDataDraw: [
        ...this.state.metaDataDraw,
        {
          element: "0x0000",
          group: "0x0002",
          name: "FileMetaInformationGroupLength",
          x,
          y,
          color: "red",
          size: {
            x: sizeX,
            y: sizeY,
          },
        },
      ],
    });
  };

  getCoords = (e) => {
    //let x = e.clientX - e.target.offsetLeft,
    //    y = e.clientY - e.target.offsetTop;
    let elem = document.querySelector(".canvasDrawElement");
    let ClientRect = elem.getBoundingClientRect();
    let x = e.clientX - ClientRect.left;
    let y = e.clientY - ClientRect.top;

    return { x, y };
  };

  fillFromCoords = (e) => {
    const coords = this.getCoords(e);
    const { x, y } = coords;
    let sizeX = 4,
      sizeY = 4;
    this.fillThis(x, y, sizeX, sizeY);
    this.logsAfterFill({ x, y, sizeX, sizeY });
  };

  onMouseMove = (event) => {
    if (this.state.drawModeCanvas) {
      this.fillFromCoords(event);
    }
  };
  onMouseDown = () => {
    const canvas = this.getCanvas();
    canvas.addEventListener("mousemove", this.onMouseMove);
  };
  onMouseUp = () => {
    const canvas = this.getCanvas();
    canvas.removeEventListener("mousemove", this.onMouseMove);
  };

  modeCanvasOn = async () => {
    await this.initCanvasDraw("layerGroup0");

    this.handleDrawModeCanvas();

    this.drawExistingData();
  };

  modeCanvasOff = () => {
    const canvas = this.getCanvas();
    canvas.removeEventListener("mousemove", this.onMouseMove);
    this.handleDrawModeCanvas();

    this.removeCanvasDrawElement();
  };

  getCanvas = () => {
    let canvas = document.querySelector(".canvasDrawElement");

    return canvas;
  };

  handleDrawModeCanvas = () => {
    this.setState({ drawModeCanvas: !this.state.drawModeCanvas });
  };
  /**
   * Handle a change draw shape event.
   * @param {string} shape The new shape name.
   */
  onChangeShape = (shape) => {
    if (this.state.dwvApp) {
      this.state.dwvApp.setDrawShape(shape);
    }
  };

  onReset = (tool) => {
    if (this.state.dwvApp) {
      this.state.dwvApp.resetDisplay();
    }
  };

  handleTagsDialogOpen = () => {
    this.setState({ showDicomTags: true });
  };

  handleTagsDialogClose = () => {
    this.setState({ showDicomTags: false });
  };

  handleMenuButtonClick = (event) => {
    this.setState({ toolMenuAnchorEl: event.currentTarget });
  };

  handleMenuClose = (event) => {
    this.setState({ toolMenuAnchorEl: null });
  };

  handleMenuItemClick = (tool) => {
    this.setState({ toolMenuAnchorEl: null });
    this.onChangeTool(tool);
  };

  // drag and drop [begin] -----------------------------------------------------

  /**
   * Setup the data load drop box: add event listeners and set initial size.
   */
  setupDropbox = (app) => {
    this.showDropbox(app, true);
  };

  /**
   * Default drag event handling.
   * @param {DragEvent} event The event to handle.
   */
  defaultHandleDragEvent = (event) => {
    // prevent default handling
    event.stopPropagation();
    event.preventDefault();
  };

  /**
   * Handle a drag over.
   * @param {DragEvent} event The event to handle.
   */
  onBoxDragOver = (event) => {
    this.defaultHandleDragEvent(event);
    // update box border
    const box = document.getElementById(this.state.dropboxDivId);
    if (box && box.className.indexOf(this.state.hoverClassName) === -1) {
      box.className += " " + this.state.hoverClassName;
    }
  };

  /**
   * Handle a drag leave.
   * @param {DragEvent} event The event to handle.
   */
  onBoxDragLeave = (event) => {
    this.defaultHandleDragEvent(event);
    // update box class
    const box = document.getElementById(this.state.dropboxDivId);
    if (box && box.className.indexOf(this.state.hoverClassName) !== -1) {
      box.className = box.className.replace(
        " " + this.state.hoverClassName,
        ""
      );
    }
  };

  /**
   * Handle a drop event.
   * @param {DragEvent} event The event to handle.
   */
  fetchImage = async (url) => {
    const data = await fetch(url, {
      mode: "no-cors",
    });
    const token = await localStorage.getItem('token')
    console.log('заливаю файл на сервер');

    const data2 = await $authHost.request({
      method: "get",
      mode: "no-cors",
      headers: {
        //"Access-Control-Allow-Origin" : '*',
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${token}`,
        accept: "application/json",
      },
      url: "http://92.255.110.75:8000/media/0002.DCM",
      onUploadProgress: (res) => {
        console.log("res", res);
      },
    });

    const buffer = await data.arrayBuffer();
    const blob = new Blob([buffer], { type: "application/dicom" });

    return blob;
  };

  fetchDataTranfer = async (info) => {
    let dt = new DataTransfer();
    dt.items.add(new File([info], "file", { type: "text/plain" }));
    let file_list = dt.files;

    return file_list;
  };

  downloadDicom = (link) => {
    let button = document.querySelector(".downloadDicomLink");
    button.href = "http://92.255.110.75:8000/media/0002.DCM";

    button.click();
  };

  onDrop2 = async (event) => {
    if (event.patient) {
      //let formData = new File();
      //formData.append('file', event.fileList)
      //this.defaultHandleDragEvent(event);

      //setTimeout(() => {
      //  this.state.dwvApp.loadFiles(event.fileList);
      //}, 3000)
      this.state.dwvApp.loadFiles(event.fileList);
    } else {
      if (event?.media_file) {
        fetchPatientDicom(event.media_file);
      }
    }
  };

  onDrop = async (event) => {
    console.log("onDrop");
    //this.downloadDicom();
    //console.log('event.dataTransfer.files', event.dataTransfer.files);

    // load files
    let input = document.querySelector('input[type="file"]');

    if (event?.patient && !this.state.incomingFileFromBack) {
      let { file } = event.patient;
      //console.log('пациент есть incomingFileFromBack нет');
      //let formData = new FormData();
      //formData.append('file', event.file)

      //let input = document.querySelector('.downloadFile')
      //const blob = await this.fetchImage('http://92.255.110.75:8000/media/0002.DCM')
      //const dT = new ClipboardEvent('').clipboardData || new DataTransfer()
      //dT.items.add(new File([blob], '0002 (1).DCM'))
      //input.files = dT.files

      //console.log('input', dT.files);

      this.setState({ incomingFileFromBack: true });
      this.startCreateDicom(file);
    }
    if (!event?.patient && !this.state.incomingFileFromBack) {
      //this.defaultHandleDragEvent(event);
      this.state.dwvApp.loadFiles(event.dataTransfer.files);

      //console.log('loadFIle', event.dataTransfer.files);
      //let file = await this.createFormData(event.dataTransfer.files);
    }

    if (this.state.incomingFileFromBack) {
      //console.log('incomingFileFromBack');
      this.state.dwvApp.loadFiles(input.dataTransfer.files);
    }
  };

  startCreateDicom(event) {
    this.state.dwvApp.loadFiles(event[0]);
  }
  createFormData = async (file) => {
    let formdata = new FormData();
    formdata.append("file", file[0]);

    return formdata;
  };

  sendFile = (file) => {
    fetchFile(file);
  };

  initCanvasDraw = async (layer) => {
    const oldCanvas = await document.querySelector(".canvasDrawElement");
    const layer2 = await document.querySelector(".layer2");

    if (oldCanvas) {
      oldCanvas.classList.remove("hidden");
      return false;
    }

    const layerDiv = await document.querySelector(`#${layer}`);
    const someCanvas = await document.querySelector("#dwv");
    //const someCanvasWidth = someCanvas.offsetWidth;
    let width = 900;
    let heigth = 900;

    //if (someCanvasWidth < 975) {
    //  width = someCanvasWidth;
    //}

    const div = document.createElement("div");
    div.classList.add("layer2");

    const canvasDrawElement = document.createElement("canvas");
    canvasDrawElement.classList.add("canvasDrawElement");
    canvasDrawElement.style.zIndex = "500";
    canvasDrawElement.setAttribute("width", width);
    canvasDrawElement.setAttribute("height", heigth);
    canvasDrawElement.setAttribute("drawMode", false);
    canvasDrawElement.style.border = "1px solid red";

    layerDiv.insertAdjacentElement("beforeend", div);
    div.insertAdjacentElement("afterbegin", canvasDrawElement);

    canvasDrawElement.addEventListener("mousedown", this.onMouseDown);
    canvasDrawElement.addEventListener("mouseup", this.onMouseUp);

    return true;
  };

  removeCanvasDrawElement() {
    let div = document.querySelector(".layer2");
    div.remove();
  }

  drawExistingData() {
    let data = this.state.metaDataDraw;

    if (!!data.length) {
      data.forEach((el) => {
        let { x, y, size } = el;
        let sizeX = size.x;
        let sizeY = size.y;
        this.fillThis(x, y, sizeX, sizeY);
      });
    }
  }

  /**
   * Show/hide the data load drop box.
   * @param show True to show the drop box.
   */
  showDropbox = (app, show) => {
    const box = document.getElementById(this.state.dropboxDivId);
    if (!box) {
      return;
    }
    const layerDiv = document.getElementById("layerGroup0");

    if (show) {
      // reset css class
      box.className =
        this.state.dropboxClassName + " " + this.state.borderClassName;
      // check content
      if (box.innerHTML === "") {
        const p = document.createElement("p");
        p.appendChild(
          document.createTextNode("Перетащите сюда скаченный Dicom файлик")
        );
        box.appendChild(p);
      }
      // show box
      box.setAttribute("style", "display:initial");
      // stop layer listening
      if (layerDiv) {
        layerDiv.removeEventListener("dragover", this.defaultHandleDragEvent);
        layerDiv.removeEventListener("dragleave", this.defaultHandleDragEvent);
        layerDiv.removeEventListener("drop", this.onDrop);
      }
      // listen to box events
      box.addEventListener("dragover", this.onBoxDragOver);
      box.addEventListener("dragleave", this.onBoxDragLeave);
      box.addEventListener("drop", this.onDrop);
    } else {
      // remove border css class
      box.className = this.state.dropboxClassName;
      // remove content
      box.innerHTML = "";
      // hide box
      box.setAttribute("style", "display:none");
      // stop box listening
      box.removeEventListener("dragover", this.onBoxDragOver);
      box.removeEventListener("dragleave", this.onBoxDragLeave);
      box.removeEventListener("drop", this.onDrop);
      // listen to layer events
      if (layerDiv) {
        layerDiv.addEventListener("dragover", this.defaultHandleDragEvent);
        layerDiv.addEventListener("dragleave", this.defaultHandleDragEvent);
        layerDiv.addEventListener("drop", this.onDrop);
      }
    }
  };

  // drag and drop [end] -------------------------------------------------------
} // DwvComponent

DwvComponent.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DwvComponent);
