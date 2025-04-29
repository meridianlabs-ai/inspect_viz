import * as PlotlyJS from 'plotly.js';

// Declare the global Plotly object will exist on the window
declare global {
  interface Window {
    Plotly: typeof PlotlyJS;
  }
}
