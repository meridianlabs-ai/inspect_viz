import * as arquero from 'arquero';

declare global {
  interface Window {
    aq: typeof arquero;
  }
}
