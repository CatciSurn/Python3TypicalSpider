// For http://www.porters.vip/confusion/flight.html
function _x(STR_XPATH,em=document) {
    // 通过Xpath查找元素
    var xresult = em.evaluate(STR_XPATH, em, null, XPathResult.ANY_TYPE, null);
    var xnodes = [];
    var xres;
    while (xres = xresult.iterateNext()) {
        xnodes.push(xres);
    }

    return xnodes;
}

ems=_x("//em[@class='rel']")

ems.forEach(em => {
    html_bs = _x('//b',em)
    html_b_first = html_bs[0]
    base_price =  _x('//i/text()',html_b_first)
    real_prices = []
    html_bs.forEach(html_b_next => {
        location = html_b_next.search(/left:(.*?)px/)
        //...
    })
    //...
});