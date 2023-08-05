(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6668],{96151:(e,t,i)=>{"use strict";i.d(t,{T:()=>r,y:()=>n});const r=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},n=()=>new Promise((e=>{r(e)}))},15327:(e,t,i)=>{"use strict";i.d(t,{eL:()=>r,SN:()=>n,id:()=>a,fg:()=>s,j2:()=>o,JR:()=>l,Y:()=>d,iM:()=>c,Q2:()=>h,Oh:()=>u,vj:()=>m,Gc:()=>p});const r=e=>e.sendMessagePromise({type:"lovelace/resources"}),n=(e,t)=>e.callWS({type:"lovelace/resources/create",...t}),a=(e,t,i)=>e.callWS({type:"lovelace/resources/update",resource_id:t,...i}),s=(e,t)=>e.callWS({type:"lovelace/resources/delete",resource_id:t}),o=e=>e.callWS({type:"lovelace/dashboards/list"}),l=(e,t)=>e.callWS({type:"lovelace/dashboards/create",...t}),d=(e,t,i)=>e.callWS({type:"lovelace/dashboards/update",dashboard_id:t,...i}),c=(e,t)=>e.callWS({type:"lovelace/dashboards/delete",dashboard_id:t}),h=(e,t,i)=>e.sendMessagePromise({type:"lovelace/config",url_path:t,force:i}),u=(e,t,i)=>e.callWS({type:"lovelace/config/save",url_path:t,config:i}),m=(e,t)=>e.callWS({type:"lovelace/config/delete",url_path:t}),p=(e,t,i)=>e.subscribeEvents((e=>{e.data.url_path===t&&i()}),"lovelace_updated")},96491:(e,t,i)=>{"use strict";i.d(t,{$:()=>o});var r=i(15327),n=i(26765),a=i(47512),s=i(4398);const o=async(e,t,i,o)=>{var l,d,c;const h=await(0,r.j2)(t),u=h.filter((e=>"storage"===e.mode)),m=null===(l=t.panels.lovelace)||void 0===l||null===(d=l.config)||void 0===d?void 0:d.mode;if("storage"!==m&&!u.length)return void(0,a.f)(e,{entities:i,yaml:!0});let p,f=null;if("storage"===m)try{p=await(0,r.Q2)(t.connection,null,!1)}catch(e){}if(!p&&u.length)for(const e of u)try{p=await(0,r.Q2)(t.connection,e.url_path,!1),f=e.url_path;break}catch(e){}p?u.length||(null===(c=p.views)||void 0===c?void 0:c.length)?u.length||1!==p.views.length?(0,s.i)(e,{lovelaceConfig:p,urlPath:f,allowDashboardChange:!0,dashboards:h,viewSelectedCallback:(n,s,l)=>{(0,a.f)(e,{lovelaceConfig:s,saveConfig:async e=>{try{await(0,r.Oh)(t,n,e)}catch{alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[l],entities:i,cardConfig:o})}}):(0,a.f)(e,{lovelaceConfig:p,saveConfig:async e=>{try{await(0,r.Oh)(t,null,e)}catch(e){alert(t.localize("ui.panel.config.devices.add_entities.saving_failed"))}},path:[0],entities:i,cardConfig:o}):(0,n.Ys)(e,{text:"You don't have any Lovelace views, first create a view in Lovelace."}):h.length>u.length?(0,a.f)(e,{entities:i,yaml:!0}):(0,n.Ys)(e,{text:"You don't seem to be in control of any dashboard, please take control first."})}},47512:(e,t,i)=>{"use strict";i.d(t,{f:()=>a});var r=i(47181);const n=()=>Promise.all([i.e(5009),i.e(220),i.e(9033),i.e(947),i.e(5829),i.e(1030),i.e(4321),i.e(1123),i.e(8048),i.e(3215),i.e(3822),i.e(2963),i.e(3196),i.e(4608),i.e(9669),i.e(8534),i.e(7757),i.e(2747)]).then(i.bind(i,9444)),a=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-suggest-card",dialogImport:n,dialogParams:t})}},4398:(e,t,i)=>{"use strict";i.d(t,{i:()=>n});var r=i(47181);const n=(e,t)=>{(0,r.B)(e,"show-dialog",{dialogTag:"hui-dialog-select-view",dialogImport:()=>Promise.all([i.e(5009),i.e(8161),i.e(2955),i.e(2762),i.e(1123),i.e(7334),i.e(9700)]).then(i.bind(i,9700)),dialogParams:t})}},85494:(e,t,i)=>{"use strict";i.r(t),i.d(t,{HuiDialogWebBrowserAisEditImage:()=>v});var r=i(15652),n=(i(51095),i(55317)),a=i(47181),s=i(34821),o=(i(319),i(11654)),l=i(96491);i(53822),i(74535),i(81303);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var a="static"===n?e:i;this.defineClassElement(a,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!u(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var a=this.decorateConstructor(i,t);return r.push.apply(r,a.finishers),a.finishers=r,a},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,a=n.length-1;a>=0;a--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var o=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[a])(o)||o);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var d=l.extras;if(d){for(var c=0;c<d.length;c++)this.addElementPlacement(d[c],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),a=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==a.finisher&&i.push(a.finisher),void 0!==a.elements){e=a.elements;for(var s=0;s<e.length-1;s++)for(var o=s+1;o<e.length;o++)if(e[s].key===e[o].key&&e[s].placement===e[o].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&Symbol.iterator in Object(e))return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=f(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var a={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),a.initializer=e.initializer),a},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:p(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=p(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function c(e){var t,i=f(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function p(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}let v=function(e,t,i,r){var n=d();if(r)for(var a=0;a<r.length;a++)n=r[a](n);var s=t((function(e){n.initializeInstanceElements(e,o.elements)}),i),o=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===a.key&&e.placement===a.placement},r=0;r<e.length;r++){var n,a=e[r];if("method"===a.kind&&(n=t.find(i)))if(m(a.descriptor)||m(n.descriptor)){if(u(a)||u(n))throw new ReferenceError("Duplicated methods ("+a.key+") can't be decorated.");n.descriptor=a.descriptor}else{if(u(a)){if(u(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+a.key+").");n.decorators=a.decorators}h(a,n)}else t.push(a)}return t}(s.d.map(c)),e);return n.initializeClassElements(s.F,o.elements),n.runClassFinishers(s.F,o.finishers)}([(0,r.Mo)("hui-dialog-web-browser-ais-edit-image")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.sz)()],key:"codeValue",value:()=>""},{kind:"field",decorators:[(0,r.sz)()],key:"selectedElementType",value:()=>""},{kind:"field",decorators:[(0,r.sz)()],key:"selectedEntityId",value:()=>""},{kind:"field",decorators:[(0,r.sz)()],key:"pictureElements",value:()=>[]},{kind:"field",decorators:[(0,r.sz)()],key:"dragCurrentItemIndex",value:()=>-1},{kind:"field",decorators:[(0,r.sz)()],key:"dragItems",value:()=>[]},{kind:"field",decorators:[(0,r.sz)()],key:"dragItemStyle",value:()=>""},{kind:"field",decorators:[(0,r.sz)()],key:"dragActive",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"_params",value:void 0},{kind:"method",key:"showDialog",value:function(e){this._params=e,this.codeValue="type: picture-elements\nimage: '/local/img/${this._params.title}'\ntitle: ''\nelements: []",this.selectedElementType="",this.selectedEntityId="",this.pictureElements=[]}},{kind:"method",key:"closeDialog",value:function(){this._params=void 0,(0,a.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"_dragStart",value:function(e){isNaN(e.target.id)||void 0!==this.dragItems[e.target.id]&&(this.dragCurrentItemIndex=e.target.id,"touchstart"===e.type?(this.dragItems[this.dragCurrentItemIndex].initialX=e.touches[0].clientX-this.dragItems[this.dragCurrentItemIndex].offsetX,this.dragItems[this.dragCurrentItemIndex].initialY=e.touches[0].clientY-this.dragItems[this.dragCurrentItemIndex].offsetY):(this.dragItems[this.dragCurrentItemIndex].initialX=e.clientX-this.dragItems[this.dragCurrentItemIndex].offsetX,this.dragItems[this.dragCurrentItemIndex].initialY=e.clientY-this.dragItems[this.dragCurrentItemIndex].offsetY),this.dragActive=!0)}},{kind:"method",key:"_dragEnd",value:function(e){this.dragActive&&(this.dragItems[this.dragCurrentItemIndex].initialX=this.dragItems[this.dragCurrentItemIndex].currentX,this.dragItems[this.dragCurrentItemIndex].initialY=this.dragItems[this.dragCurrentItemIndex].currentY,this.dragActive=!1,this.pictureElements[this.dragCurrentItemIndex].style.transform=this.dragItemStyle,this._handleCodeChanged())}},{kind:"method",key:"_getDragStyle",value:function(e){return e===this.dragCurrentItemIndex?"transform: "+this.dragItemStyle:"transform: "+this.dragItems[e].style}},{kind:"method",key:"_drag",value:function(e){if(this.dragActive){let t,i;e.preventDefault(),"touchmove"===e.type?(t=e.touches[0].clientX-this.dragItems[this.dragCurrentItemIndex].initialX,i=e.touches[0].clientY-this.dragItems[this.dragCurrentItemIndex].initialY):(t=e.clientX-this.dragItems[this.dragCurrentItemIndex].initialX,i=e.clientY-this.dragItems[this.dragCurrentItemIndex].initialY),this.dragItemStyle="translate3d("+t+"px, "+i+"px, 0)",this.dragItems[this.dragCurrentItemIndex].currentX=t,this.dragItems[this.dragCurrentItemIndex].currentY=i,this.dragItems[this.dragCurrentItemIndex].offsetX=t,this.dragItems[this.dragCurrentItemIndex].offsetY=i,this.dragItems[this.dragCurrentItemIndex].style="translate3d("+t+"px, "+i+"px, 0)"}}},{kind:"method",key:"_handleAddElement",value:function(){const e={type:this.selectedElementType,entity:this.selectedEntityId,style:{position:"absolute",top:"50%",left:"50%",transform:""}};this.pictureElements.push(e);this.dragItems.push({currentX:0,currentY:0,initialX:0,initialY:0,offsetX:0,offsetY:0,style:""}),this.selectedEntityId="",this.selectedElementType="",this._handleCodeChanged()}},{kind:"method",key:"_handleSelectedElementTypeChanged",value:function(e){const t=e.detail.item.getAttribute("itemid");this.selectedElementType=t}},{kind:"method",key:"_handleSelectedEntityIdChanged",value:function(e){this.selectedEntityId=e.detail.value}},{kind:"method",key:"entityFilter",value:function(e){return!e.entity_id.includes(".ais")}},{kind:"method",key:"_handleCodeChanged",value:function(){this.codeValue="type: picture-elements\nimage: '/local/img/${this._params.title}'\ntitle: ''\nelements: [\n",this.pictureElements.forEach((e=>{this.codeValue+=JSON.stringify(e)+",\n"})),this.codeValue+="]"}},{kind:"method",key:"_addToLovelaceView",value:function(){var e;const t=null===(e=this._params)||void 0===e?void 0:e.sourceUrl.split("?authSig=")[0].replace("/media/galeria/"," /local/img/");(0,l.$)(this,this.hass,[],[{type:"picture-elements",title:"",image:t,elements:this.pictureElements}]),this.closeDialog()}},{kind:"method",key:"render",value:function(){return this._params&&this._params.sourceType&&this._params.sourceUrl?r.dy`
      <ha-dialog
        open
        hideActions
        .heading=${(0,s.i)(this.hass,"Konfiguracja karty elementy obrazu")}
        @closed=${this.closeDialog}
      >
        <div id="outerContainer">
          <div
            id="container"
            style="background-image: url(${this._params.sourceUrl});"
            @touchstart=${this._dragStart}
            @touchend=${this._dragEnd}
            @touchmove=${this._drag}
            @mousedown=${this._dragStart}
            @mouseup=${this._dragEnd}
            @mousemove=${this._drag}
          >
            ${this.pictureElements.map(((e,t)=>r.dy` <div
                .id=${t.toString()}
                class="pictureElementItem"
                .style=${this._getDragStyle(t)}
              >
                ${e.entity}
              </div>`))}
          </div>
        </div>
        <h3>Wybierz element do dodania</h3>
        <ha-paper-dropdown-menu dynamic-align label-float label="Typ">
          <paper-listbox
            slot="dropdown-content"
            attr-for-selected="itemId"
            .selected=${this.selectedElementType}
            @iron-select=${this._handleSelectedElementTypeChanged}
          >
            <paper-item itemid="state-badge">State Badge</paper-item>
            <paper-item itemid="state-icon">State Icon</paper-item>
            <paper-item itemid="state-label">State Label</paper-item>
          </paper-listbox>
        </ha-paper-dropdown-menu>
        <ha-entity-picker
          .hass=${this.hass}
          .value=${this.selectedEntityId}
          @value-changed=${this._handleSelectedEntityIdChanged}
          .configValue=${"entity"}
          .entityFilter=${this.entityFilter}
          allow-custom-entity
        ></ha-entity-picker>
        ${""!==this.selectedEntityId&&""!==this.selectedElementType?r.dy` <mwc-button @click=${this._handleAddElement}>
              <ha-svg-icon .path=${n.qX5}></ha-svg-icon>
              Dodaj element do obrazu
            </mwc-button>`:""}
        <br /><br />
        <ha-code-editor mode="yaml" .value=${this.codeValue}></ha-code-editor>
        <div class="card-actions">
          <mwc-button @click=${this._addToLovelaceView}>
            ${this.hass.localize("ui.panel.config.devices.entities.add_entities_lovelace")||"Dodaj do interfejsu użytkownika"}
          </mwc-button>
        </div>
      </ha-dialog>
    `:r.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[o.yu,r.iv`
        /* @media (min-width: 800px) {
          ha-dialog {
            --mdc-dialog-max-width: 800px;
            --mdc-dialog-min-width: 400px;
            width: 100%;
          }
        } */
        /* make dialog fullscreen */
        ha-dialog {
          --mdc-dialog-min-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          --mdc-dialog-max-width: calc(
            100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
          );
          --mdc-dialog-min-height: 100%;
          --mdc-dialog-max-height: 100%;
          --mdc-shape-medium: 0px;
          --vertial-align-dialog: flex-end;
        }
        #outerContainer {
          height: 50vh;
        }
        #container {
          height: 50vh;
          width: 50vw;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          border-radius: 7px;
          touch-action: none;
          background-size: 50vw 50vh;
          background-repeat: no-repeat;
          background-position: center;
          margin: auto;
        }
        div.pictureElementItem {
          width: 80px;
          height: 80px;
          background-color: rgb(245, 230, 99);
          border: 10px solid rgba(136, 136, 136, 0.5);
          border-radius: 50%;
          touch-action: none;
          user-select: none;
          top: 50%;
          left: 50%;
        }
        div.pictureElementItem:active {
          background-color: rgba(168, 218, 220, 1);
        }
        div.pictureElementItem:hover {
          cursor: pointer;
          /* border-width: 20px; */
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=chunk.dbe111f8c5d1c243cd6e.js.map