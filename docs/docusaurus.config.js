// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/github");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "TimerX",
  tagline: "A fluent Timer App, made completely in Python",
  url: "https://timerx.netlify.app",
  baseUrl: "/",
  onBrokenLinks: "warn",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",
  organizationName: "Futura-Py", // Usually your GitHub org/user name.
  projectName: "TimerX", // Usually your repo name.

  presets: [
    [
      "classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          // Please change this to your repo.
          editUrl: "https://github.com/Futura-Py/TimerX/blob/master/docs",
        },
        blog: false,
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],
  customFields: {
    throwIfNamespace: false,
  },
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: "TimerX",
        logo: {
          alt: "TimerX Logo",
          src: "img/logo.svg",
        },

        items: [
          { to: "/docs/intro", label: "Documentation", position: "left" },
          {
            to: "https://github.com/Futura-Py/TimerX/releases",
            label: "Download TimerX",
            position: "left",
          },
          {
            href: "https://github.com/Futura-Py/TimerX",
            label: "GitHub",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Docs",
            items: [
              {
                label: "Documentation",
                to: "/docs/intro",
              },
              {
                label: "Contributing to TimerX",
                to: "/docs/contributing",
              },
              {
                label: "Compiling from source",
                to: "/docs/compile",
              },
            ],
          },

          {
            title: "More",
            items: [
              {
                label: "Blog",
                to: "/blog",
              },
              {
                label: "GitHub",
                href: "https://github.com/Futura-Py/TimerX",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} MIT License by The Futura Team`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
      colorMode: {
        defaultMode: "light",
        disableSwitch: false,
        respectPrefersColorScheme: false,
        switchConfig: {
          darkIcon: "\u263e",
          darkIconStyle: {
            marginLeft: "2px",
          },
          /*
          Unicode icons such as '\u2600' will work
          Unicode with 5 chars require brackets: '\u{1F602}'
          but I don't get the point of unicodes when we have GitHub emojis, right?
          // this is old. lightIcon: '\u{1F602}',
          */
          lightIcon: "\u{1F4A1}",
          lightIconStyle: {
            marginLeft: "1px",
          },
        },
      },
    }),
};

(module.exports = config),
  {
    presets: [
      {
        customCss: [require.resolve("./src/css/custom.css")],
      },
    ],
    themeConfig: {
      announcementBar: {
        id: "v1.1",
        content:
          'v1.1 is released! Get it <a href="https://github.com/Futura-Py/TimerX/releases/latest">here</a>!',
        backgroundColor: "#fafbfc",
        textColor: "#091E42",
        isCloseable: false,
      },
    },
  };
