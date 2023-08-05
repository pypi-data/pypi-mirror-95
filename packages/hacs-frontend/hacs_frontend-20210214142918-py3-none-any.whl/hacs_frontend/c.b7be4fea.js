import{_ as o,H as c,h as t,c as e}from"./e.c9b35252.js";import"./c.1e3ec6ed.js";import"./c.f7adccf5.js";let i=o([e("hacs-reload-dialog")],(function(o,c){return{F:class extends c{constructor(...c){super(...c),o(this)}},d:[{kind:"method",key:"render",value:function(){return this.active?t`
      <hacs-dialog .active=${this.active} .hass=${this.hass} title="Reload">
        <div class="content">
          ${this.hacs.localize("dialog.reload.description")}
          </br>
          ${this.hacs.localize("dialog.reload.confirm")}
        </div>
        <mwc-button slot="secondaryaction" @click=${this._close}>
          ${this.hacs.localize("common.cancel")}
        </mwc-button>
        <mwc-button slot="primaryaction" @click=${this._reload}>
          ${this.hacs.localize("common.reload")}
        </mwc-button>
      </hacs-dialog>
    `:t``}},{kind:"method",key:"_reload",value:function(){window.top.location.reload(!0)}},{kind:"method",key:"_close",value:function(){this.active=!1,this.dispatchEvent(new Event("hacs-dialog-closed",{bubbles:!0,composed:!0}))}}]}}),c);export{i as HacsReloadDialog};
