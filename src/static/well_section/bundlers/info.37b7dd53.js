(0,globalThis.parcelRequireda87.register)("18TX5",function(e,t){Object.defineProperty(e.exports,"__esModule",{value:!0,configurable:!0}),Object.defineProperty(e.exports,"default",{get:()=>o,set:void 0,enumerable:!0,configurable:!0});var o={props:{params:{text:{default:"..."}}},nodes(){return{lstInfoTxt:{_html:this.param.text,onclick:e=>e.target.hidePopover()}}},loaded(){let e=Math.random().toString(16).slice(8);this.options.template=`<button class="lstInfoBtn" popovertarget="${e}">i</button><div class="lstInfoTxt" id="${e}" popover></div>`}}});