import DefaultTheme from "vitepress/theme";
import "./style/index.css"; // 引入自定义的样式
import { h } from 'vue';
import {
  NolebaseEnhancedReadabilitiesMenu,
  NolebaseEnhancedReadabilitiesScreenMenu,
} from '@nolebase/vitepress-plugin-enhanced-readabilities/client';
import { HomeFooter } from '@theojs/lumen'
import { HomeUnderline } from '@theojs/lumen'
import { DocVideoLink } from '@theojs/lumen'
import { Footer_Data } from '../data/footerData'
import '@nolebase/vitepress-plugin-enhanced-readabilities/client/style.css';
import Confetti from "./components/Confetti.vue";
export const Theme = {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      'layout-bottom': () => h(HomeFooter, { Footer_Data }),
      // 为较宽的屏幕的导航栏添加阅读增强菜单
      'nav-bar-content-after': () => h(NolebaseEnhancedReadabilitiesMenu),
      // 为较窄的屏幕（通常是小于 iPad Mini）添加阅读增强菜单
      'nav-screen-content-after': () => h(NolebaseEnhancedReadabilitiesScreenMenu),
    });
  },
  enhanceApp({ app, router }) {
    app.component("Confetti", Confetti); //注册全局组件
    app.component('Home', HomeUnderline);
    app.component('Vid', DocVideoLink)
  },
};

export default {
  ...Theme,
};