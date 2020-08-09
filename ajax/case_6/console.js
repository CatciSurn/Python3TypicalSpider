// 钩子函数 控制台注入
(function(){
    'use strict'
    function hook(object,attr){
        var func = object[attr]
        object[attr] = function(){
            console.log('hooked',object,attr,arguments)
            var ret=func.apply(object,arguments)
            debugger
            console.log('result:',ret)
            return ret
        }
    }
    hook(window,'btoa')
})()