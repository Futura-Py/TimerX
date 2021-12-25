
import { configuration } from '@codedoc/core';

import { theme } from './theme';


export const config = /*#__PURE__*/configuration({
  theme,                                  // --> add the theme. modify `./theme.ts` for changing the theme.
  
  dev: {
    port: 3000                           // --> the port for local dev server
  },
  dest: {                                // @see /docs/config/output
    html: '.',                           // --> the base folder for HTML files
    assets: 'assets',                         // --> the base folder for assets
    bundle: 'docs/assets',               // --> where to store codedoc's bundle (relative to `assets`)
    styles: 'docs/assets',               // --> where to store codedoc's styles (relative to `assets`)
    namespace: '/TimerX',                       // --> project namespace
  },
  page: {
    title: {
      base: 'TimerX'                 // --> the base title of your doc pages
    },
    favicon: '/favicon.ico'
  },
  misc: {
    github: {
      user: 'sumeshir26',                // --> your github username (where your repo is hosted)
      repo: 'TimerX',                // --> your github repo name
      action: 'Star',             // --> action of the GitHub button
      count: true,               // --> whether to show the `count` on the GitHub button
      large: true,                // --> whether to show a `large` GitHub button
      standardIcon: true,        // --> whether to use the GitHub icon on the GitHub button or use an action specific icon
    }
  },
});
