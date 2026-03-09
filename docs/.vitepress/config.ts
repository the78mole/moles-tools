import { defineConfig } from "vitepress";

export default defineConfig({
  title: "moles-tools",
  description: "A collection of Python tools from the underground",
  base: "/moles-tools/",

  head: [["link", { rel: "icon", href: "/moles-tools/favicon.ico" }]],

  themeConfig: {
    logo: "/logo.svg",

    nav: [
      { text: "Home", link: "/" },
      { text: "Tools", link: "/tools/env-updater" },
      {
        text: "Changelog",
        link: "https://github.com/the78mole/moles-tools/releases",
      },
    ],

    sidebar: [
      {
        text: "Getting Started",
        items: [
          { text: "Introduction", link: "/" },
          { text: "Installation", link: "/installation" },
          { text: "Contributing", link: "/contributing" },
        ],
      },
      {
        text: "Tools",
        items: [
          { text: "ENV File Updater", link: "/tools/env-updater" },
        ],
      },
    ],

    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/the78mole/moles-tools",
      },
    ],

    footer: {
      message: "Released under the MIT License.",
      copyright: "Copyright © 2024-present the78mole",
    },

    search: {
      provider: "local",
    },

    editLink: {
      pattern:
        "https://github.com/the78mole/moles-tools/edit/main/docs/:path",
      text: "Edit this page on GitHub",
    },
  },
});
