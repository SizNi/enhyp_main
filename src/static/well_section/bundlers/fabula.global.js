(()=>{function e(e,t,s,a){Object.defineProperty(e,t,{get:s,set:a,enumerable:!0,configurable:!0})}function t(e){Object.defineProperty(e,"__esModule",{value:!0,configurable:!0})}var s=globalThis,a={},o={},r=s.parcelRequireda87;null==r&&((r=function(e){if(e in a)return a[e].exports;if(e in o){var t=o[e];delete o[e];var s={id:e,exports:{}};return a[e]=s,t.call(s.exports,s,s.exports),s.exports}var r=Error("Cannot find module '"+e+"'");throw r.code="MODULE_NOT_FOUND",r}).register=function(e,t){o[e]=t},s.parcelRequireda87=r);var n=r.register;n("juxiN",function(t,s){e(t.exports,"register",()=>a,e=>a=e),e(t.exports,"resolve",()=>o,e=>o=e);var a,o,r=new Map;a=function(e,t){for(var s=0;s<t.length-1;s+=2)r.set(t[s],{baseUrl:e,path:t[s+1]})},o=function(e){var t=r.get(e);if(null==t)throw Error("Could not resolve bundle with id "+e);return new URL(t.path,t.baseUrl).toString()}}),n("4qOVI",function(t,s){e(t.exports,"getBundleURL",()=>a,e=>a=e);var a,o={};a=function(e){var t=o[e];return t||(t=function(){try{throw Error()}catch(t){var e=(""+t.stack).match(/(https?|file|ftp|(chrome|moz|safari-web)-extension):\/\/[^)\n]+/g);if(e)// Use the 3rd one, which will be a runtime in the original bundle.
return(""+e[2]).replace(/^((?:https?|file|ftp|(chrome|moz|safari-web)-extension):\/\/.+)\/[^/]+$/,"$1")+"/"}return"/"}(),o[e]=t),t}}),n("dGgIV",function(t,s){e(t.exports,"default",()=>a);var a={template:'<div><div class="fblBlock"></div></div>',sources:{collection:()=>r("3dQ3h"),standard:()=>r("hWwjJ")},props:{params:{target:{},path:{}}},nodes(){return{fblBlock:{component:{src:this.param.target.collection?this.source.collection:this.source.standard,params:{target:this.param.target,path:[...this.param.path,this.param.target.name]}}}}}}}),n("3dQ3h",function(e,t){e.exports=Promise.all([r("cPcr1")(r("juxiN").resolve("glc1b")),r("hK9Md")(r("juxiN").resolve("2xs4f"))]).then(()=>r("kUkKS"))}),n("cPcr1",function(e,t){var s=r("3AMmx");e.exports=s(function(e){return new Promise(function(t,s){if([].concat(document.getElementsByTagName("link")).some(function(t){return t.href===e&&t.rel.indexOf("stylesheet")>-1})){t();return}var a=document.createElement("link");a.rel="stylesheet",a.href=e,a.onerror=function(e){a.onerror=a.onload=null,a.remove(),s(e)},a.onload=function(){a.onerror=a.onload=null,t()},document.getElementsByTagName("head")[0].appendChild(a)})})}),n("3AMmx",function(e,t){var s={},a={},o={};e.exports=function(e,t){return function(r){var n=function(e){switch(e){case"preload":return a;case"prefetch":return o;default:return s}}(t);return n[r]?n[r]:n[r]=e.apply(null,arguments).catch(function(e){throw delete n[r],e})}}}),n("hK9Md",function(e,t){var s=r("3AMmx");e.exports=s(function(e){return new Promise(function(t,s){if([].concat(document.getElementsByTagName("script")).some(function(t){return t.src===e})){t();return}var a=document.createElement("link");a.href=e,a.rel="preload",a.as="script",document.head.appendChild(a);var o=document.createElement("script");o.async=!0,o.type="text/javascript",o.src=e,o.onerror=function(t){var a=TypeError("Failed to fetch dynamically imported module: ".concat(e,". Error: ").concat(t.message));o.onerror=o.onload=null,o.remove(),s(a)},o.onload=function(){o.onerror=o.onload=null,t()},document.getElementsByTagName("head")[0].appendChild(o)})})}),n("hWwjJ",function(e,t){e.exports=Promise.all([r("cPcr1")(r("juxiN").resolve("glc1b")),r("hK9Md")(r("juxiN").resolve("kp10L"))]).then(()=>r("VUacI"))}),n("bFEhs",function(s,a){t(s.exports),e(s.exports,"default",()=>o);var o={template:`
  <button class="lstBtn l-fx-b l-br">
    <span class="lstBtnIcon"></span>
    <span class="lstBtnText"></span>
  </button>`,directives:{_attr:r("WtULa")._attr},props:{proxies:{value:{},disabled:{}},params:{name:{default:""},type:{default:"button"},size:{default:"small"},text:{},options:{default:{}}},methods:{change:{}}},nodes(){return{lstBtn:{_class:{"l-fx-rev":this.param.options.reverse},_attr:{size:this.param.size},name:this.param.name,type:this.param.type,disabled:()=>this.proxy.disabled,onclick:()=>this.method.change&&this.method.change(this.param.name)},lstBtnIcon:{_html:()=>this.param.options.icon},lstBtnText:{textContent:()=>this.param.text??this.proxy.value}}}}}),n("WtULa",function(t,s){e(t.exports,"_attr",()=>a);let a={update:(e,t,s)=>{let a="function"==typeof t[s]?t[s]():t[s];"boolean"==typeof a?a?e.setAttribute(s,""):e.removeAttribute(s):a&&e.setAttribute(s,a)}}}),n("lWmiX",function(s,a){t(s.exports),e(s.exports,"default",()=>o);var o={template:'<div class="lstLbl l-label"></div><fieldset class="lstBtns l-fx"></fieldset>',props:{proxies:{value:{},disabled:{},error:{}},params:{size:{default:"small"},name:{default:""},type:{type:"string"},text:{},options:{// width: {},
// buttons: {
//   type: 'array',
//   default: []
// }
default:{}}},methods:{change:{}}},nodes(){return{lstLbl:{textContent:()=>this.param.text},lstBtns:{name:this.param.name,_class:{radio:"radio"===this.param.type},_html:()=>this.method.render(),onclick:e=>{if(e.target.closest(".lstBtns > button")){let t=+e.target.dataset.index,s=this.param.options.buttons||this.proxy.value;this.method.change&&this.method.change(s[t],t)}}}}},methods:{render(){let e=this.param.options.buttons||this.proxy.value,t=e=>Array.isArray(this.proxy.value)?this.proxy.value.includes(e):this.proxy.value===e;return e?.reduce((e,s,a)=>e+`
        <button class="${t(s)?" active":""}" data-index="${a}" size="${this.param.size}">${s}</button>`,"")},update(e){this.proxy.value=e}}}}),n("jshus",function(e,t){e.exports=Promise.all([r("cPcr1")(r("juxiN").resolve("jpa6x")),r("hK9Md")(r("juxiN").resolve("20xE6"))]).then(()=>r("i3Sqb"))}),n("fuCbW",function(e,t){e.exports=Promise.all([r("cPcr1")(r("juxiN").resolve("4MNwM")),r("hK9Md")(r("juxiN").resolve("gddAz"))]).then(()=>r("hUm3m"))}),r("juxiN").register(r("4qOVI").getBundleURL("5JBrp"),JSON.parse('["5JBrp","fabula.global.js","2xs4f","collection.51062594.js","glc1b","collection.5fd56b39.css","kp10L","standard.c73549fe.js","20xE6","input.8ad92093.js","jpa6x","input.7f78a140.css","gddAz","nest.6919ac1a.js","bkqLt","popup.e06cdbf2.js","819Ax","popup.39f18e94.css","4MNwM","nest.8cd31f21.css","72QnI","fabula.global.css"]'));var i=r("dGgIV"),l=r("bFEhs"),c={template:`
  <dialog class="lstDialog l-scrollbar">
    <div class="lstClose"></div>
    <div section="content"></div>
  </dialog>`,props:{proxies:{maximize:{},opened:{}},methods:{onclose:{}}},handlers:{opened(e){e?this.node.lstDialog.showModal():this.node.lstDialog.close()}},nodes(){return{lstDialog:{_class:{"l-full-screen":()=>this.proxy.maximize}},lstClose:{onclick:()=>this.method.close()}}},methods:{open(){this.proxy.opened=!0},close(){this.proxy.opened=!1,this.method.onclose&&this.method.onclose()}}},d={template:`
    <div class="lstSidebar">
      <div class="lstClose"></div>
      <div class="lstSidebarWr">
        <div>
          <div section="top"></div>
          <div section="content"></div>
        </div>
        <div section="bottom"></div>
      </div>
    </div>`,props:{params:{tabletWidth:{},scrollContainer:{}},proxies:{opened:{default:!1},minimize:{default:!1}},methods:{onclose:{}}},params:{scrollHandler:()=>{},matchMedia:null},proxies:{tablet:!1},nodes(){return{lstClose:{onclick:()=>this.method.close()},lstSidebar:{_class:{mini:()=>this.proxy.minimize,show:()=>this.proxy.opened,tablet:()=>this.proxy.tablet}}}},methods:{resize(){let e=this.node.lstSidebar.getBoundingClientRect().top;this.node.lstSidebar.style.maxHeight=this.param.scrollContainer.clientHeight-e+"px"},tabletChange(e){this.proxy.tablet=e.matches,this.proxy.tablet&&this.proxy.opened&&this.method.close()},isTablet(){return this.proxy.tablet},open(){this.proxy.opened=!0},close(){this.proxy.opened=!1,this.method.onclose&&this.method.onclose()}},mounted(){this.param.scrollContainer&&(this.method.resize(),this.param.scrollHandler=this.throttling(()=>this.method.resize(),100),this.param.scrollContainer.addEventListener("scroll",this.param.scrollHandler)),this.param.matchMedia=window.matchMedia(`(max-width: ${this.param.tabletWidth||"560px"})`),this.method.tabletChange(this.param.matchMedia),this.param.matchMedia.addListener(this.method.tabletChange)},unmounted(){this.param.scrollContainer&&this.param.scrollContainer.removeEventListener("scroll",this.param.scrollHandler),this.param.matchMedia.removeListener(this.method.tabletChange)}},h=r("lWmiX"),p={template:`<div class="fblNtf">
    <div class="fblNtfCont"></div>
    <div class="fblNtfBtns"></div>
  </div>`,props:{params:{dialog:{}},proxies:{message:{}},methods:{confirm:{}}},nodes(){return{fblNtfCont:{textContent:()=>this.proxy.message},fblNtfBtns:{component:{induce:()=>this.param.dialog,src:h.default,proxies:{value:()=>this.bus.local.cancel,disabled:{},error:{}},params:{options:{buttons:[this.bus.local.cancel||"Cancel",this.bus.local.confirm||"Ok"]}},methods:{change:(e,t)=>{1===t&&this.method.confirm(),this.bus.dialog.method.close()}}}}}}},u={template:`
    <div class="fblWr">
      <div class="fblDialog"></div>
      <div class="fblMain l-container l-content">
        <h2 class="fblMainHead"></h2>
        <div class="fblForm"></div>
        <div class="l-fx l-gap">
            <div class="fblClear"></div>
            <div class="fblSubmit"></div>
        </div>
      </div>
      <div class="fblSidebar"></div>
    </div>`,props:{proxies:{error:{store:"form"}},methods:{submit:{store:"form"},clear:{store:"form"}}},proxies:{message:""},nodes(){return{fblMainHead:{textContent:this.bus.entry.mainHead},fblForm:{component:{src:i.default,params:{target:this.bus.entry.form,path:[]}}},fblSubmit:{component:{src:l.default,params:{text:this.bus.local.submit,size:"normal"},proxies:{disabled:()=>this.proxy.error},methods:{change:async()=>{this.proxy.message=this.bus.entry.local.requestMessage,await this.bus.dialog.section.content.mount({src:p,proxies:{message:()=>this.proxy.message}}),this.bus.dialog.method.open(),this.proxy.message=await this.method.submit()}}}},fblClear:{component:{src:l.default,params:{text:this.bus.local.clear,size:"normal"},methods:{change:async()=>{this.proxy.message=this.bus.entry.local.clearMessage,await this.bus.dialog.section.content.mount({src:p,params:{dialog:!0},proxies:{message:()=>this.proxy.message},methods:{confirm:()=>{this.method.clear()}}}),this.bus.dialog.method.open()}}}},fblDialog:{component:{src:c,sections:{content:{}}}},fblSidebar:{component:{src:d,sections:{content:{}}}}}},mounted(){this.bus.dialog=this.node.fblDialog,this.bus.sidebar=this.node.fblSidebar}},m={input:()=>r("jshus"),button:()=>Promise.resolve(r("bFEhs")),buttons:()=>Promise.resolve(r("lWmiX")),nest:()=>r("fuCbW")};class f{constructor(e){var t;let{lesta:s,root:a,elements:o,onRequest:r,onResponse:n}=e,{createApp:i,deliver:l,replicate:c}=s;a.classList.add("lstUI"),this.element={},this.resetStore=()=>{},this.app=i({root:a,stores:{form:(t=this,{params:{errors:{}},proxies:{_values:{},error:!0},methods:{get({path:e}){l(this.proxy._values,e)},set({path:e,value:t}){l(this.proxy._values,e,t)},add({path:e,value:t}){let s=l(this.proxy._values,e)?.length||0;l(this.proxy._values,[...e,s],t),l(this.proxy._values,[...e,"length"],s+1)},remove({path:e}){let t=l(this.proxy._values,e)?.length||0;l(this.proxy._values,[...e,"length"],t-1)},error({key:e,value:t}){this.param.errors[e]=t,this.proxy.error=Object.values(this.param.errors).includes(!0)},async submit(){let{url:e,method:t,headers:s}=this.bus.entry.server;console.log(e,t,s);try{let a=r?await r(c(this.proxy._values)):JSON.stringify(this.proxy._values),o=await fetch(e,{method:t,headers:s,body:a});return n?await n(o):this.bus.local.sentMessage}catch(e){return this.bus.local.errorMessage}},async clear(){await t.unmount(),await t.mount()}},created(){let{get:e,set:s,add:a,remove:o}=this.method;Object.assign(t.element,{get:e,set:s,add:a,remove:o}),t.resetStore=()=>{this.param.error={},this.proxy._values={},this.proxy.error=!0}}})},plugins:{...s,elements:{...m,...o},bus:{entry:{},local:{}},execute({_values:e,path:t,value:s,direction:a}){let o,r;let n=[...t];"number"==typeof n.at(-1)&&(o=n.pop(),n.push("length"),r=l(e,n));let i={};t.forEach((e,s)=>"number"==typeof e&&(i[t[s-1]]=e));let c=Function("_values","value","index","length","currentIndex","return "+a);return c(e,s,o,r,i)}}})}async create(e,t={}){let s={};if(this.app.root.unmount&&await this.unmount(),"string"==typeof e){let a=await fetch(e,t);s=await a.json()}else s=e;this.app.plugins.bus.entry=s,this.app.plugins.bus.local=s.local,await this.mount()}async mount(){await this.app.mount(u)}async unmount(){await this.app.unmount(),this.resetStore()}}window.fabula={createForm:function(e){let t=new f(e);return{mount:t.create.bind(t),unmount:t.unmount.bind(t),element:t.element}},jsonToFormData:function(e){let t=new FormData;return!function e(t,s,a){if(!s||"object"!=typeof s||s instanceof Date||s instanceof File||s instanceof Blob){let e=null==s?"":s;t.append(a,e)}else Object.keys(s).forEach(o=>{e(t,s[o],a?`${a}[${o}]`:o)})}(t,e),t}}})();