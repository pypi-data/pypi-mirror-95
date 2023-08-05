(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[4321],{32333:(t,e,s)=>{"use strict";var i=s(15652);class r extends i.oi{static get properties(){return{value:{type:Number},high:{type:Number},low:{type:Number},min:{type:Number},max:{type:Number},step:{type:Number},startAngle:{type:Number},arcLength:{type:Number},handleSize:{type:Number},handleZoom:{type:Number},readonly:{type:Boolean},disabled:{type:Boolean},dragging:{type:Boolean,reflect:!0},rtl:{type:Boolean},_scale:{type:Number},valueLabel:{type:String},lowLabel:{type:String},highLabel:{type:String}}}constructor(){super(),this.min=0,this.max=100,this.step=1,this.startAngle=135,this.arcLength=270,this.handleSize=6,this.handleZoom=1.5,this.readonly=!1,this.disabled=!1,this.dragging=!1,this.rtl=!1,this._scale=1,this.attachedListeners=!1}get _start(){return this.startAngle*Math.PI/180}get _len(){return Math.min(this.arcLength*Math.PI/180,2*Math.PI-.01)}get _end(){return this._start+this._len}get _showHandle(){return!this.readonly&&(null!=this.value||null!=this.high&&null!=this.low)}_angleInside(t){let e=(this.startAngle+this.arcLength/2-t+180+360)%360-180;return e<this.arcLength/2&&e>-this.arcLength/2}_angle2xy(t){return this.rtl?{x:-Math.cos(t),y:Math.sin(t)}:{x:Math.cos(t),y:Math.sin(t)}}_xy2angle(t,e){return this.rtl&&(t=-t),(Math.atan2(e,t)-this._start+2*Math.PI)%(2*Math.PI)}_value2angle(t){const e=((t=Math.min(this.max,Math.max(this.min,t)))-this.min)/(this.max-this.min);return this._start+e*this._len}_angle2value(t){return Math.round((t/this._len*(this.max-this.min)+this.min)/this.step)*this.step}get _boundaries(){const t=this._angle2xy(this._start),e=this._angle2xy(this._end);let s=1;this._angleInside(270)||(s=Math.max(-t.y,-e.y));let i=1;this._angleInside(90)||(i=Math.max(t.y,e.y));let r=1;this._angleInside(180)||(r=Math.max(-t.x,-e.x));let n=1;return this._angleInside(0)||(n=Math.max(t.x,e.x)),{up:s,down:i,left:r,right:n,height:s+i,width:r+n}}_mouse2value(t){const e=t.type.startsWith("touch")?t.touches[0].clientX:t.clientX,s=t.type.startsWith("touch")?t.touches[0].clientY:t.clientY,i=this.shadowRoot.querySelector("svg").getBoundingClientRect(),r=this._boundaries,n=e-(i.left+r.left*i.width/r.width),a=s-(i.top+r.up*i.height/r.height),o=this._xy2angle(n,a);return this._angle2value(o)}dragStart(t){if(!this._showHandle||this.disabled)return;let e=t.target,s=void 0;if(this._rotation&&"focus"!==this._rotation.type)return;if(e.classList.contains("shadowpath"))if("touchstart"===t.type&&(s=window.setTimeout((()=>{this._rotation&&(this._rotation.cooldown=void 0)}),200)),null==this.low)e=this.shadowRoot.querySelector("#value");else{const s=this._mouse2value(t);e=Math.abs(s-this.low)<Math.abs(s-this.high)?this.shadowRoot.querySelector("#low"):this.shadowRoot.querySelector("#high")}if(e.classList.contains("overflow")&&(e=e.nextElementSibling),!e.classList.contains("handle"))return;e.setAttribute("stroke-width",2*this.handleSize*this.handleZoom*this._scale);const i="high"===e.id?this.low:this.min,r="low"===e.id?this.high:this.max;this._rotation={handle:e,min:i,max:r,start:this[e.id],type:t.type,cooldown:s},this.dragging=!0}_cleanupRotation(){const t=this._rotation.handle;t.setAttribute("stroke-width",2*this.handleSize*this._scale),this._rotation=!1,this.dragging=!1,t.blur()}dragEnd(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;this._cleanupRotation();let s=new CustomEvent("value-changed",{detail:{[e.id]:this[e.id]},bubbles:!0,composed:!0});this.dispatchEvent(s),this.low&&this.low>=.99*this.max?this._reverseOrder=!0:this._reverseOrder=!1}drag(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;if(this._rotation.cooldown)return window.clearTimeout(this._rotation.coldown),void this._cleanupRotation();if("focus"===this._rotation.type)return;t.preventDefault();const e=this._mouse2value(t);this._dragpos(e)}_dragpos(t){if(t<this._rotation.min||t>this._rotation.max)return;const e=this._rotation.handle;this[e.id]=t;let s=new CustomEvent("value-changing",{detail:{[e.id]:t},bubbles:!0,composed:!0});this.dispatchEvent(s)}_keyStep(t){if(!this._showHandle||this.disabled)return;if(!this._rotation)return;const e=this._rotation.handle;"ArrowLeft"!==t.key&&"ArrowDown"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]+this.step):this._dragpos(this[e.id]-this.step)),"ArrowRight"!==t.key&&"ArrowUp"!==t.key||(t.preventDefault(),this.rtl?this._dragpos(this[e.id]-this.step):this._dragpos(this[e.id]+this.step)),"Home"===t.key&&(t.preventDefault(),this._dragpos(this.min)),"End"===t.key&&(t.preventDefault(),this._dragpos(this.max))}firstUpdated(){document.addEventListener("mouseup",this.dragEnd.bind(this)),document.addEventListener("touchend",this.dragEnd.bind(this),{passive:!1}),document.addEventListener("mousemove",this.drag.bind(this)),document.addEventListener("touchmove",this.drag.bind(this),{passive:!1}),document.addEventListener("keydown",this._keyStep.bind(this))}updated(t){if(this.shadowRoot.querySelector(".slider")){const t=window.getComputedStyle(this.shadowRoot.querySelector(".slider"));if(t&&t.strokeWidth){const e=parseFloat(t.strokeWidth);if(e>this.handleSize*this.handleZoom){const t=this._boundaries,s=`\n          ${e/2*Math.abs(t.up)}px\n          ${e/2*Math.abs(t.right)}px\n          ${e/2*Math.abs(t.down)}px\n          ${e/2*Math.abs(t.left)}px`;this.shadowRoot.querySelector("svg").style.margin=s}}}if(this.shadowRoot.querySelector("svg")&&void 0===this.shadowRoot.querySelector("svg").style.vectorEffect){t.has("_scale")&&1!=this._scale&&this.shadowRoot.querySelector("svg").querySelectorAll("path").forEach((t=>{if(t.getAttribute("stroke-width"))return;const e=parseFloat(getComputedStyle(t).getPropertyValue("stroke-width"));t.style.strokeWidth=e*this._scale+"px"}));const e=this.shadowRoot.querySelector("svg").getBoundingClientRect(),s=Math.max(e.width,e.height);this._scale=2/s}}_renderArc(t,e){const s=e-t;return t=this._angle2xy(t),e=this._angle2xy(e+.001),`\n      M ${t.x} ${t.y}\n      A 1 1,\n        0,\n        ${s>Math.PI?"1":"0"} ${this.rtl?"0":"1"},\n        ${e.x} ${e.y}\n    `}_renderHandle(t){const e=this._value2angle(this[t]),s=this._angle2xy(e),r={value:this.valueLabel,low:this.lowLabel,high:this.highLabel}[t]||"";return i.YP`
      <g class="${t} handle">
        <path
          id=${t}
          class="overflow"
          d="
          M ${s.x} ${s.y}
          L ${s.x+.001} ${s.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke="rgba(0,0,0,0)"
          stroke-width="${4*this.handleSize*this._scale}"
          />
        <path
          id=${t}
          class="handle"
          d="
          M ${s.x} ${s.y}
          L ${s.x+.001} ${s.y+.001}
          "
          vector-effect="non-scaling-stroke"
          stroke-width="${2*this.handleSize*this._scale}"
          tabindex="0"
          @focus=${this.dragStart}
          @blur=${this.dragEnd}
          role="slider"
          aria-valuemin=${this.min}
          aria-valuemax=${this.max}
          aria-valuenow=${this[t]}
          aria-disabled=${this.disabled}
          aria-label=${r||""}
          />
        </g>
      `}render(){const t=this._boundaries;return i.dy`
      <svg
        @mousedown=${this.dragStart}
        @touchstart=${this.dragStart}
        xmln="http://www.w3.org/2000/svg"
        viewBox="${-t.left} ${-t.up} ${t.width} ${t.height}"
        style="margin: ${this.handleSize*this.handleZoom}px;"
        ?disabled=${this.disabled}
        focusable="false"
      >
        <g class="slider">
          <path
            class="path"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
          />
          <path
            class="bar"
            vector-effect="non-scaling-stroke"
            d=${this._renderArc(this._value2angle(null!=this.low?this.low:this.min),this._value2angle(null!=this.high?this.high:this.value))}
          />
          <path
            class="shadowpath"
            d=${this._renderArc(this._start,this._end)}
            vector-effect="non-scaling-stroke"
            stroke="rgba(0,0,0,0)"
            stroke-width="${3*this.handleSize*this._scale}"
            stroke-linecap="butt"
          />

        </g>

        <g class="handles">
        ${this._showHandle?null!=this.low?this._reverseOrder?i.dy`${this._renderHandle("high")} ${this._renderHandle("low")}`:i.dy`${this._renderHandle("low")} ${this._renderHandle("high")}`:i.dy`${this._renderHandle("value")}`:""}
        </g>
      </svg>
    `}static get styles(){return i.iv`
      :host {
        display: inline-block;
        width: 100%;
      }
      svg {
        overflow: visible;
        display: block;
      }
      path {
        transition: stroke 1s ease-out, stroke-width 200ms ease-out;
      }
      .slider {
        fill: none;
        stroke-width: var(--round-slider-path-width, 3);
        stroke-linecap: var(--round-slider-linecap, round);
      }
      .path {
        stroke: var(--round-slider-path-color, lightgray);
      }
      .bar {
        stroke: var(--round-slider-bar-color, deepskyblue);
      }
      svg[disabled] .bar {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      g.handles {
        stroke: var(--round-slider-handle-color, var(--round-slider-bar-color, deepskyblue));
        stroke-linecap: round;
        cursor: var(--round-slider-handle-cursor, pointer);
      }
      g.low.handle {
        stroke: var(--round-slider-low-handle-color);
      }
      g.high.handle {
        stroke: var(--round-slider-high-handle-color);
      }
      svg[disabled] g.handles {
        stroke: var(--round-slider-disabled-bar-color, darkgray);
      }
      .handle:focus {
        outline: unset;
      }
    `}}customElements.define("round-slider",r)},68928:(t,e,s)=>{"use strict";s.d(e,{WU:()=>x});var i=/d{1,4}|M{1,4}|YY(?:YY)?|S{1,3}|Do|ZZ|Z|([HhMsDm])\1?|[aA]|"[^"]*"|'[^']*'/g,r="[1-9]\\d?",n="\\d\\d",a="[^\\s]+",o=/\[([^]*?)\]/gm;function h(t,e){for(var s=[],i=0,r=t.length;i<r;i++)s.push(t[i].substr(0,e));return s}var l=function(t){return function(e,s){var i=s[t].map((function(t){return t.toLowerCase()})).indexOf(e.toLowerCase());return i>-1?i:null}};function d(t){for(var e=[],s=1;s<arguments.length;s++)e[s-1]=arguments[s];for(var i=0,r=e;i<r.length;i++){var n=r[i];for(var a in n)t[a]=n[a]}return t}var u=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],c=["January","February","March","April","May","June","July","August","September","October","November","December"],g=h(c,3),m={dayNamesShort:h(u,3),dayNames:u,monthNamesShort:g,monthNames:c,amPm:["am","pm"],DoFn:function(t){return t+["th","st","nd","rd"][t%10>3?0:(t-t%10!=10?1:0)*t%10]}},f=d({},m),p=function(t,e){for(void 0===e&&(e=2),t=String(t);t.length<e;)t="0"+t;return t},y={D:function(t){return String(t.getDate())},DD:function(t){return p(t.getDate())},Do:function(t,e){return e.DoFn(t.getDate())},d:function(t){return String(t.getDay())},dd:function(t){return p(t.getDay())},ddd:function(t,e){return e.dayNamesShort[t.getDay()]},dddd:function(t,e){return e.dayNames[t.getDay()]},M:function(t){return String(t.getMonth()+1)},MM:function(t){return p(t.getMonth()+1)},MMM:function(t,e){return e.monthNamesShort[t.getMonth()]},MMMM:function(t,e){return e.monthNames[t.getMonth()]},YY:function(t){return p(String(t.getFullYear()),4).substr(2)},YYYY:function(t){return p(t.getFullYear(),4)},h:function(t){return String(t.getHours()%12||12)},hh:function(t){return p(t.getHours()%12||12)},H:function(t){return String(t.getHours())},HH:function(t){return p(t.getHours())},m:function(t){return String(t.getMinutes())},mm:function(t){return p(t.getMinutes())},s:function(t){return String(t.getSeconds())},ss:function(t){return p(t.getSeconds())},S:function(t){return String(Math.round(t.getMilliseconds()/100))},SS:function(t){return p(Math.round(t.getMilliseconds()/10),2)},SSS:function(t){return p(t.getMilliseconds(),3)},a:function(t,e){return t.getHours()<12?e.amPm[0]:e.amPm[1]},A:function(t,e){return t.getHours()<12?e.amPm[0].toUpperCase():e.amPm[1].toUpperCase()},ZZ:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+p(100*Math.floor(Math.abs(e)/60)+Math.abs(e)%60,4)},Z:function(t){var e=t.getTimezoneOffset();return(e>0?"-":"+")+p(Math.floor(Math.abs(e)/60),2)+":"+p(Math.abs(e)%60,2)}},_=function(t){return+t-1},v=[null,r],b=[null,a],w=["isPm",a,function(t,e){var s=t.toLowerCase();return s===e.amPm[0]?0:s===e.amPm[1]?1:null}],M=["timezoneOffset","[^\\s]*?[\\+\\-]\\d\\d:?\\d\\d|[^\\s]*?Z?",function(t){var e=(t+"").match(/([+-]|\d\d)/gi);if(e){var s=60*+e[1]+parseInt(e[2],10);return"+"===e[0]?s:-s}return 0}],S=(l("monthNamesShort"),l("monthNames"),{default:"ddd MMM DD YYYY HH:mm:ss",shortDate:"M/D/YY",mediumDate:"MMM D, YYYY",longDate:"MMMM D, YYYY",fullDate:"dddd, MMMM D, YYYY",isoDate:"YYYY-MM-DD",isoDateTime:"YYYY-MM-DDTHH:mm:ssZ",shortTime:"HH:mm",mediumTime:"HH:mm:ss",longTime:"HH:mm:ss.SSS"}),x=function(t,e,s){if(void 0===e&&(e=S.default),void 0===s&&(s={}),"number"==typeof t&&(t=new Date(t)),"[object Date]"!==Object.prototype.toString.call(t)||isNaN(t.getTime()))throw new Error("Invalid Date pass to format");var r=[];e=(e=S[e]||e).replace(o,(function(t,e){return r.push(e),"@@@"}));var n=d(d({},f),s);return(e=e.replace(i,(function(e){return y[e](t,n)}))).replace(/@@@/g,(function(){return r.shift()}))}}}]);
//# sourceMappingURL=chunk.a18eefc1ac606672eebf.js.map