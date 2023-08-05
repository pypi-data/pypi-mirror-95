/*! For license information please see 25.08f05c9e.chunk.js.LICENSE.txt */
(this["webpackJsonpstreamlit-browser"]=this["webpackJsonpstreamlit-browser"]||[]).push([[25],{1176:function(e,t,r){"use strict";r.d(t,"a",(function(){return o})),r.d(t,"b",(function(){return i}));var n=r(7),a=r.n(n),i=a()("label",{target:"effi0qh0"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.bodyText,marginBottom:t.fontSizes.halfSmDefault}}),""),o=a()("div",{target:"effi0qh1"})((function(e){var t=e.theme;return{fontSize:t.fontSizes.smDefault,color:t.colors.gray,margin:t.spacing.none,textAlign:"right",position:"absolute",bottom:0,right:t.fontSizes.halfSmDefault}}),"")},1503:function(e,t,r){"use strict";r.d(t,"a",(function(){return y}));var n=r(6),a=r(1),i=r(141),o=r(0),s=r.n(o),l=r(98),u=r(1729),c=r(7),d=r.n(c),p=r(235),h=r.n(p),f=r(1377);var v=d()("span",{target:"e1sjeeqh0"})({name:"1d0tddh",styles:"overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"}),m=d()(f.e,{shouldForwardProp:h.a,target:"e1sjeeqh1"})((function(e){var t=e.theme,r=e.$isHighlighted;return{display:"flex",alignItems:"center",paddingTop:t.spacing.none,paddingBottom:t.spacing.none,background:r?t.colors.lightestGray:void 0,"&:hover, &:active, &:focus":{background:t.colors.lightestGray}}}),"");function g(e){var t=e.data,r=e.index,o=e.style,s=t[r].props,l=s.item,u=(s.overrides,Object(i.a)(s,["item","overrides"]));return Object(a.jsx)(m,Object(n.a)(Object(n.a)({style:o},u),{},{children:Object(a.jsx)(v,{children:l.label})}),l.value)}var b=s.a.forwardRef((function(e,t){var r=s.a.Children.toArray(e.children);if(!r[0]||!r[0].props.item){var i=r[0]?r[0].props:{};return Object(a.jsx)(l.b,{$style:{height:"".concat(90,"px")},ref:t,children:Object(a.jsx)(l.a,Object(n.a)({},i))})}var o=Math.min(300,40*r.length);return Object(a.jsx)(l.b,{ref:t,children:Object(a.jsx)(u.FixedSizeList,{width:"100%",height:o,itemCount:r.length,itemData:r,itemKey:function(e,t){return t[e].props.item.value},itemSize:40,children:g})})}));b.displayName="VirtualDropdown";var y=b},3856:function(e,t,r){"use strict";r.r(t),r.d(t,"default",(function(){return b}));var n=r(1),a=r(10),i=r(13),o=r(21),s=r(22),l=r(0),u=r.n(l),c=r(2491),d=r.n(c),p=r(37),h=r(3834),f=r(1376),v=r(1503),m=r(1176),g=function(e){Object(o.a)(r,e);var t=Object(s.a)(r);function r(){var e;Object(a.a)(this,r);for(var n=arguments.length,i=new Array(n),o=0;o<n;o++)i[o]=arguments[o];return(e=t.call.apply(t,[this].concat(i))).state={value:e.initialValue},e.setWidgetValue=function(t){var r=e.props.element.id;e.props.widgetMgr.setIntArrayValue(r,e.state.value,t)},e.onChange=function(t){var r=e.generateNewState(t);e.setState(r,(function(){return e.setWidgetValue({fromUi:!0})}))},e}return Object(i.a)(r,[{key:"componentDidMount",value:function(){this.setWidgetValue({fromUi:!1})}},{key:"generateNewState",value:function(e){var t=function(){var t=e.option.value;return parseInt(t,10)};switch(e.type){case"remove":return{value:d()(this.state.value,t())};case"clear":return{value:[]};case"select":return{value:this.state.value.concat([t()])};default:throw new Error("State transition is unkonwn: {data.type}")}}},{key:"render",value:function(){var e=this.props,t=e.element,r=e.theme,a={width:e.width},i=t.options,o=0===i.length||this.props.disabled,s=0===i.length?"No options to select.":"Choose an option",l=i.map((function(e,t){return{label:e,value:t.toString()}}));return Object(n.jsxs)("div",{className:"row-widget stMultiSelect",style:a,children:[Object(n.jsx)(m.b,{children:t.label}),Object(n.jsx)(h.a,{options:l,labelKey:"label",valueKey:"value",placeholder:s,type:f.b.select,multi:!0,onChange:this.onChange,value:this.valueFromState,disabled:o,size:"compact",overrides:{ValueContainer:{style:function(){return{minHeight:"44px"}}},ClearIcon:{style:{color:r.colors.darkGray}},SearchIcon:{style:{color:r.colors.darkGray}},Tag:{props:{overrides:{Root:{style:{borderTopLeftRadius:r.radii.md,borderTopRightRadius:r.radii.md,borderBottomRightRadius:r.radii.md,borderBottomLeftRadius:r.radii.md,fontSize:r.fontSizes.sm,paddingLeft:r.spacing.md}},Action:{style:{paddingLeft:r.spacing.sm}}}}},MultiValue:{props:{overrides:{Root:{style:{fontSize:r.fontSizes.sm}}}}},Dropdown:{component:v.a}}})]})}},{key:"initialValue",get:function(){var e=this.props.element.id,t=this.props.widgetMgr.getIntArrayValue(e);return void 0!==t?t:this.props.element.default}},{key:"valueFromState",get:function(){var e=this;return this.state.value.map((function(t){var r=e.props.element.options[t];return{value:t.toString(),label:r}}))}}]),r}(u.a.PureComponent),b=Object(p.withTheme)(g)}}]);
//# sourceMappingURL=25.08f05c9e.chunk.js.map