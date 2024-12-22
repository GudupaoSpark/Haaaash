import { defineConfig } from 'vitepress';
import AutoNav from "vite-plugin-vitepress-auto-nav";
import { figure } from '@mdit/plugin-figure'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  markdown: {
    config: (md) => {
      md.use(figure, { figcaption: 'alt', copyAttrs: '^class$', lazy: true })
    }
  },
  ignoreDeadLinks: [
    // ignore exact url "/playground"
    '/playground',
    // ignore all localhost links
    /^https?:\/\/localhost/,
    // ignore all links include "/repl/""
    /\/repl\//,
    // custom function, ignore all links include "ignore"
    (url) => {
      return url.toLowerCase().includes('ignore')
    }
  ],
  vite: {
    plugins: [
      AutoNav({
        itemsSetting: {}
      }),
    ],
    optimizeDeps: {
      exclude: [
        '@nolebase/vitepress-plugin-enhanced-readabilities/client',
        'vitepress',
        '@nolebase/ui',
      ],
    },
    ssr: {
      noExternal: [
        // 如果还有别的依赖需要添加的话，并排填写和配置到这里即可
        '@nolebase/vitepress-plugin-enhanced-readabilities',
        '@nolebase/ui',
      ],
    },
  },
  title: "Haaaash",
  lang: "zh-CN",
  description: "批量哈希工具",
  srcDir: "docs",
  cleanUrls: true,
  themeConfig: {
    langMenuLabel: '切换语言',
    darkModeSwitchLabel: '主题',
    lightModeSwitchTitle: '切换到浅色模式',
    darkModeSwitchTitle: '切换到深色模式',
    sidebarMenuLabel: '菜单',
    outline: { level: [2, 3], label: '目录' },
    returnToTopLabel: '返回顶部',
    // 请将此链接修改为正确的URL，或根据需求删除该配置
    // editLink: { pattern: 'https://github.com/username/repository-name/blame/main/docs/:path', text: '源代码', },
    lastUpdated: { text: '更新于' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    editLink: {
      pattern: 'https://github.com/GudupaoSpark/Haaaash/blob/main/docs/docs/:path',
      text: '在 GitHub 上编辑此页面'
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/GudupaoSpark/Haaaash/' }
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索',
            buttonAriaLabel: '搜索文档'
          },
          modal: {
            noResultsText: '无法找到相关结果',
            resetButtonTitle: '清除查询条件',
            footer: {
              selectText: '选择',
              navigateText: '切换',
              closeText: '关闭'
            }
          }
        }
      }
    },
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2023-present Gudupao'
    }
  }
})