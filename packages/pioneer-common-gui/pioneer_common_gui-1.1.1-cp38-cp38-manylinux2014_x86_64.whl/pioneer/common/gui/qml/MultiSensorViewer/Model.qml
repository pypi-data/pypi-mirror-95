import QtQuick 2.9

QtObject
{
    id: component
    property var x:              [0              ]//,1              ]//,2           ]
    property var y:              [0              ]//,0              ]//,0           ]
    property var z:              [0              ]//,0              ]//,0           ]
    property var rx:             [0              ]//,0              ]//,0           ]
    property var ry:             [0              ]//,0              ]//,0           ]
    property var rz:             [0              ]//,0              ]//,0           ]
    property var flip:           [0              ]//,0              ]//,0           ]
    property var frustrumDepth:  [20             ]//,20             ]//,20          ]
    property var ampMin:         [0              ]//,0              ]//,0           ]
    property var ampMax:         [32768          ]//,2000           ]//,1           ]
    property var distMin:        [0              ]//,0              ]//,0           ]
    property var distMax:        [250            ]//,50             ]//,50          ]
    property var flags:          ['eagle'        ]//,None           ]//,None        ]
    property var ampMin3d:       [0              ]//,0              ]//,0           ]
    property var ampMax3d:       [32768          ]//,1              ]//,1           ]
    property var adaptative:     [0.0]
    property var ampMin2d:       [0              ]//,0              ]//,0           ]
    property var ampMax2d:       [1              ]//,1              ]//,1           ]
    property var distMin2d:      [0              ]//,0              ]//,0           ]
    property var distMax2d:      [50             ]//,50             ]//,50          ]
    property var ssrMode:        ['passthrough']
    property var depthImgVisible:[true           ]//,true           ]//,true        ]
    property var cameraVisible:  [true           ]//,true           ]//,true        ]
    property var cloudVisible:   [true           ]//,true           ]//,true        ]
    property var colorMap:       ['gist_earth'   ]//,'gist_earth'   ]//,'gist_earth']
    property var hasLCPG:        [true           ]//false,          ]//,false       ]
    property var lcpgIndex:      [0x08           ]//,-1             ]//,-1          ]
    property var lcpgAnimate:    [true           ]//,false          ]//,false       ]
    property var lcpgAnimTimeMS: [4000           ]//,0              ]//,0           ]
    property var lcpgDelay:      [100           ]//,0              ]//,0           ]


    function makeFilter(i)
    {
    	return ({'ampMin': ampMin[i], 'ampMax': ampMax[i]
    			, 'distMin': distMin[i], 'distMax': distMax[i]
    			, 'flags': flags[i]})
    }

    readonly property var angles : [24.75,21.5,18.3,15.15,12.1,9.05,6,3,0,-3,-6,-9.05,-12.1,-15.15,-18.3,-21.5,-24.75];
	onLcpgIndexChanged:
	{
		for(var i = 0; i < component.x.length; i++)
		{
			if(component.hasLCPG[i])
			{
				var a = angles[component.lcpgIndex[i]] * (Math.PI / 180);
				if(a != component.ry[i])
				{
					var index = i; //take a snapshot of i, as it is captured by reference
					singleShot(component.lcpgDelay[i], function()
					{
						component.ry[index] = a
						component.ryChanged();
					});
				}
			}
		}
	}

	function singleShot( interval, callback) {
	    var timer = Qt.createQmlObject( "import QtQuick 2.9; Timer{}", component);
	    timer.interval = interval;
	    timer.triggered.connect( function () {
	        callback();
	        timer.destroy();
	    } );
	    timer.start();
	}

}




