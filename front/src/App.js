import React, { Component, useState } from 'react';

import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { indigo, pink } from '@mui/material/colors';

import styleDRW from './components/layoutDRW/layoutDRW.module.scss';
import './App.css';

import DwvComponent from './DwvComponent';
import { List } from './pages/list/List';
import { Home } from './pages/home/Home';



const theme = createTheme({
  typography: {
    useNextVariants: true,
  },
  palette: {
    primary: indigo,
    secondary: pink,
    type: 'light'
  },
  layout: 'list'
});

class App extends Component {
  render() {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="App">
          <Home />
        </div>
      </ThemeProvider>
    );
  }
}

export default App;
