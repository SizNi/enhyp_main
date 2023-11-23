var e;(0,(e=globalThis.parcelRequireda87).register)("bCUam",function(t,l){Object.defineProperty(t.exports,"__esModule",{value:!0,configurable:!0}),Object.defineProperty(t.exports,"default",{get:()=>o,set:void 0,enumerable:!0,configurable:!0});var a=e("7ZQJ3"),o={template:`
  <dialog class="lstDialog l-scrollbar">
    <div class="lstClose"></div>
    <h2 class="lstDialogHd"></h2>
    <p class="lstDialogTxt"></p>
    <div section="content"></div>
    <div class="l-fx l-jc-end">
      <div class="lstDialogReject"></div>
      <div class="lstDialogAllow"></div>
    </div>
  </dialog>`,props:{params:{cancelable:{},expanded:{},title:{},text:{},allow:{},reject:{}},proxies:{opened:{default:!1}},methods:{onclose:{},allow:{},reject:{}}},handlers:{opened(e){e?this.node.lstDialog.showModal():this.node.lstDialog.close()}},nodes(){return{lstDialog:{_class:{"l-full-screen":()=>this.param.expanded},oncancel:e=>{this.param.cancelable?this.method.onclose():e.preventDefault()}},lstClose:{hidden:!this.param.cancelable,onclick:()=>this.method.onclose()},lstDialogHd:{_text:()=>this.param.title},lstDialogTxt:{_text:()=>this.param.text},lstDialogReject:{component:{induce:()=>this.param.reject,src:a.default,params:{text:()=>this.param.reject.text,type:()=>this.param.reject.type||"text"},methods:{action:()=>{this.method.reject?.(),this.method.onclose()}}}},lstDialogAllow:{component:{induce:()=>this.param.allow,src:a.default,params:{text:()=>this.param.allow.text,type:()=>this.param.allow.type||"text"},methods:{action:()=>{this.method.allow?.(),this.method.onclose()}}}}}},methods:{opened(e){this.proxy.opened=e}},mounted(){this.proxy.opened&&this.node.lstDialog.showModal()}}});