import{_ as t,H as s,h as i,c as o}from"./e.03a03bfd.js";import{m as e}from"./c.34cfc96d.js";import{v as n}from"./c.c33059b8.js";import"./c.f58c454b.js";import"./c.ce34ea34.js";import"./c.4b9b528f.js";let a=t([o("hacs-about-dialog")],(function(t,s){return{F:class extends s{constructor(...s){super(...s),t(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?i`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.narrow?"HACS":"Home Assistant Community Store"}
        hideActions
      >
        <div class="content">
          ${e.html(`\n**${this.hacs.localize("dialog_about.integration_version")}:** | ${this.hacs.configuration.version}\n--|--\n**${this.hacs.localize("dialog_about.frontend_version")}:** | ${n}\n**${this.hacs.localize("common.repositories")}:** | ${this.repositories.length}\n**${this.hacs.localize("dialog_about.installed_repositories")}:** | ${this.repositories.filter((t=>t.installed)).length}\n\n**${this.hacs.localize("dialog_about.useful_links")}:**\n\n- [General documentation](https://hacs.xyz/)\n- [Configuration](https://hacs.xyz/docs/configuration/start)\n- [FAQ](https://hacs.xyz/docs/faq/what)\n- [GitHub](https://github.com/hacs)\n- [Discord](https://discord.gg/apgchf8)\n- [Become a GitHub sponsor? ❤️](https://github.com/sponsors/ludeeus)\n- [BuyMe~~Coffee~~Beer? 🍺🙈](https://buymeacoffee.com/ludeeus)\n\n***\n\n_Everything you find in HACS is **not** tested by Home Assistant, that includes HACS itself.\nThe HACS and Home Assistant teams do not support **anything** you find here._\n        `)}
        </div>
      </hacs-dialog>
    `:i``}}]}}),s);export{a as HacsAboutDialog};
