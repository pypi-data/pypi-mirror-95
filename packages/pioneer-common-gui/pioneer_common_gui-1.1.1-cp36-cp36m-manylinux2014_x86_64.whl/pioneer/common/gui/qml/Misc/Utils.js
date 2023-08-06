
//.pragma library

function merge(/*variable arguments count*/)
{
    var merged = {};
    for (var i = 0; i < arguments.length; i++) 
    {
        var obj = arguments[i];
        for (var attrname in obj) { merged[attrname] = obj[attrname]; }
    }
    
    return merged;
}

function listOfInstances(instantiator)
{
    var m = {};

    var getter = 'objectAt'
    if('itemAt' in instantiator)
        getter = 'itemAt'

    for(var i = 0; i < instantiator.count; i++)
    {
        
        var w = instantiator[getter](i);
        m[w.dsName] = w;
    }
    return m;
}

function makeVisibilityDict(elements)
{
    var m = {};
    for(var i in elements)
        m[elements[i]] = false
    return m;
}

function makeColorsDict(elements)
{
    var colors = svgColorNames();
    var m = {};
    for(var i in elements)
        m[elements[i]] = colors[i];
    return m
}

function getFromDict(key, dict, alt)
{
    return key in dict ? dict[key] : alt
}

/**Index to the first element in the sorted container that is equal to or above the number being looked up, and -1 if there is no such element.
 * http://thushw.blogspot.com/2010/07/why-am-i-writing-lowerbound-in-java.html
 */
function lowerBound(arr, key) {
    var len = arr.length;
    var lo = 0;
    var hi = len-1;
    var mid = (lo + hi)/2 | 0;
    while (true) {
        if (key <= arr[mid]) {
            hi = mid-1;
            if (hi < lo)
                return mid;
        } else {
            lo = mid+1;
            if (hi < lo)
                return mid<len-1?mid+1:-1;
        }
        mid = (lo + hi)/2 | 0;
    }
}
/**Index to the first element in the sorted container that is above the number being looked up, and -1 if there is no such element.
 * http://thushw.blogspot.com/2010/07/why-am-i-writing-lowerbound-in-java.html
 */
function upperBound(arr, key) {
    var len = arr.length;
    var lo = 0;
    var hi = len-1;
    var mid = (lo + hi)/2 | 0;
    while (true) {
        if (key >= arr[mid]) {
            lo = mid+1;
            if (hi < lo)
                return mid<len-1?mid+1:-1;
        } else {
            hi = mid-1;
            if (hi < lo)
                return mid;
        }
        mid = (lo + hi)/2;
        mid = (lo + hi)/2 | 0;
    }
}

function sort(arr)
{
    arr.sort(function(a, b){return a - b});
}

function svgColorNames()
{
    return[
        'red'
        , 'green'
        , 'blue'
        , 'cyan'
        , 'magenta'
        , 'crimson'
        , 'olive'
        , 'chocolate'             	
        , 'darkblue'          	
        , 'darksalmon'          
        , 'maroon'            	
        , 'darkkhaki'             	
        , 'powderblue'            	
        , 'purple'            	
        , 'yellowgreen'
, 'aliceblue'             	
, 'antiquewhite'          	
, 'aqua'          	
, 'aquamarine'            	
, 'azure'             	
, 'beige'             	
, 'bisque'            	
, 'black'             	
, 'blanchedalmond'            	
, 'blue'          	
, 'blueviolet'            	
, 'brown'             	
, 'burlywood'             	
, 'cadetblue'             	
, 'chartreuse'            	
, 'coral'             	
, 'cornflowerblue'            	
, 'cornsilk'          	
, 'darkcyan'          	
, 'darkgoldenrod'             	
, 'darkgray'          	
, 'darkgreen'             	
, 'darkgrey'          	
, 'darkmagenta'           	
, 'darkolivegreen'            	
, 'darkorange'            	
, 'darkorchid'            	
, 'darkred'           	
, 'darkseagreen'          	
, 'darkslateblue'             	
, 'darkslategray'             	
, 'darkslategrey'             	
, 'darkturquoise'             	
, 'darkviolet'            	
, 'deeppink'          	
, 'deepskyblue'           	
, 'dimgray'           	
, 'dimgrey'           	
, 'dodgerblue'            	
, 'firebrick'             	
, 'floralwhite'           	
, 'forestgreen'           	
, 'fuchsia'           	
, 'gainsboro'             	
, 'ghostwhite'            	
, 'gold'          	
, 'goldenrod'             	
, 'gray'          	
, 'grey'          	
, 'green'             	
, 'greenyellow'           	
, 'honeydew'          	
, 'hotpink'           	
, 'indianred'             	
, 'indigo'            	
, 'ivory'             	
, 'khaki'             	
, 'lavender'          	
, 'lavenderblush'             	
, 'lawngreen'             	
, 'lemonchiffon'          	
, 'lightblue'             	
, 'lightcoral'            	
, 'lightcyan'             	
, 'lightgoldenrodyellow'          	
, 'lightgray'             	
, 'lightgreen'            	
, 'lightgrey'             	
, 'lightpink'             	
, 'lightsalmon'           	
, 'lightseagreen'             	
, 'lightskyblue'          	
, 'lightslategray'            	
, 'lightslategrey'            	
, 'lightsteelblue'            	
, 'lightyellow'           	
, 'lime'          	
, 'limegreen'             	
, 'linen'             	
, 'magenta'           	
, 'mediumaquamarine'          	
, 'mediumblue'            	
, 'mediumorchid'          	
, 'mediumpurple'          	
, 'mediumseagreen'            	
, 'mediumslateblue'           	
, 'mediumspringgreen'             	
, 'mediumturquoise'           	
, 'mediumvioletred'           	
, 'midnightblue'          	
, 'mintcream'             	
, 'mistyrose'             	
, 'moccasin'          	
, 'navajowhite'           	
, 'navy'          	
, 'oldlace'           	
, 'olive'             	
, 'olivedrab'             	
, 'orange'            	
, 'orangered'             	
, 'orchid'            	
, 'palegoldenrod'             	
, 'palegreen'             	
, 'paleturquoise'             	
, 'palevioletred'             	
, 'papayawhip'            	
, 'peachpuff'             	
, 'peru'          	
, 'pink'          	
, 'plum'          	
, 'red'           	
, 'rosybrown'             	
, 'royalblue'             	
, 'saddlebrown'           	
, 'salmon'            	
, 'sandybrown'            	
, 'seagreen'          	
, 'seashell'          	
, 'sienna'            	
, 'silver'            	
, 'skyblue'           	
, 'slateblue'             	
, 'slategray'             	
, 'slategrey'             	
, 'snow'          	
, 'springgreen'           	
, 'steelblue'             	
, 'tan'           	
, 'teal'          	
, 'thistle'           	
, 'tomato'            	
, 'turquoise'             	
, 'violet'            	
, 'wheat'             	
, 'white'             	
, 'whitesmoke'            	
, 'yellow'            	
];
}        