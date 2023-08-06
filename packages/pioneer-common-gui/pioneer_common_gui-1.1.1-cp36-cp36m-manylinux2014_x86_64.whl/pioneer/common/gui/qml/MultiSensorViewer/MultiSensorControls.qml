import QtQuick 2.9
import QtQuick.Controls 1.4
import QtQuick.Controls 2.4 as Ctrl24
import Leddar 1.0

Column
{
    id: component
    property var model
    property int nIndices : 0
    readonly property int index: slider_.value
    anchors.fill: parent
    Column
    {
    	visible: component.nIndices > 0
	    Slider
	    {
	        id: slider_
	        width: component.parent.width
	        value: 0
	        maximumValue: component.nIndices-1
	        minimumValue: 0
	        stepSize: 1
	        NumberAnimation on value
	        {
	            id: animation_
	            running: false
	            loops: NumberAnimation.Infinite
	            from: slider_.value
	            to: slider_.maximumValue-1
	        }
	    }
	    Row
	    {
	        Button
	        {
	            text: "play/pause"
	            onClicked: animation_.running ? animation_.stop() : animation_.start()
	        }
	        Button
	        {
	            text: "rewind"
	            onClicked:
	            {
	                slider_.value = 0;
	            }
	        }
	    }
    }
    Row
    {
        Repeater
        {
            id: transforms_
            model: component.model.x.length
            Column
            {
                id: transforms_
                readonly property int topIndex : index
				Repeater
				{
				    model: [['x'                , -10              , 10              , 0.01      , 2]
				          , ['y'                , -10              , 10              , 0.01      , 2]
				          , ['z'                , -10              , 10              , 0.01      , 2]
				          , ['rx'               , -10              , 10              , 0.01      , 2]
				          , ['ry'               , -10              , 10              , 0.01      , 2]
				          , ['rz'               , -10              , 10              , 0.01      , 2]
				          , ['frustrumDepth'    , 0                , 250             , 1         , 0]
				          , ['ampMin'           , -Math.pow(2,14)  , Math.pow(2,16)  , 1         , 2]
				          , ['ampMax'           , -Math.pow(2,14)  , Math.pow(2,16)  , 10        , 2]
				          , ['distMin'          , 0                , 300             , .1        , 2]
				          , ['distMax'          , 0                , 500             , 1         , 2]
						  , ['ampMin3d'         , -Math.pow(2,14)  , Math.pow(2,16)  , 1         , 2]
						  , ['ampMax3d'         , -Math.pow(2,14)  , Math.pow(2,16)  , 10        , 2]
		        		  , ['adaptative'       , 0                , 1               , .01       , 2]
				          , ['ampMin2d'         , -Math.pow(2,14)  , Math.pow(2,14)  , .01       , 2]
				          , ['ampMax2d'         , -Math.pow(2,14)  , Math.pow(2,14)  , .01       , 2]
				          , ['distMin2d'        , 0                , 300             , .1        , 2]
				          , ['distMax2d'        , 0                , 300             , 1         , 2]]
				    Row
				    {
				        Text{text: modelData[0]}
				        SpinBox
				        {
				            id: s_
				            minimumValue: modelData[1]
				            maximumValue: modelData[2]
				            stepSize: modelData[3]
				            decimals: modelData[4]
				            Binding on value
				            {
				            	delayed: true
				                value: component.model[modelData[0]][transforms_.topIndex]
				            }
				            onValueChanged:
				            {
				                component.model[modelData[0]][transforms_.topIndex] = s_.value;
				                component.model[modelData[0] + "Changed"]();
				            }
				        }
				    }
				}
                Ctrl24.ComboBox
                {
                	id: ssrMode_
                	model: ['passthrough']//FIXME: ssr is broken, 'Eagle', 'LCA2', 'LCA3']
		            Binding on currentIndex
		            {
		            	delayed: true
		                value: ssrMode_.find(component.model.ssrMode[transforms_.topIndex].trim())
		            }
		            onCurrentIndexChanged:
		            {
		                component.model.ssrMode[transforms_.topIndex] = model[currentIndex];
		                component.model.ssrModeChanged();
		            }
		            Component.onCompleted: currentIndex = ssrMode_.find(component.model.ssrMode[transforms_.topIndex].trim())
                }
				Column
				{
					visible: component.model.hasLCPG[transforms_.topIndex]
					CheckBox
					{
					   text: "animate lcpg";
						Binding on checked
						{
							delayed: true
						    value: component.model.lcpgAnimate[transforms_.topIndex]
					    }
					    onCheckedChanged:
					    {
						component.model.lcpgAnimate[transforms_.topIndex] = checked;
						component.model.lcpgAnimateChanged();
					    }
					}
				Repeater
				{
				    model: [['lcpgIndex'        , 1                , 0x10            , 1         , 0]
				          , ['lcpgAnimTimeMS'   , 0                , 20000           , 100       , 0]
				          , ['lcpgDelay'        , 0                , 5000            , 10       , 0]]
				    Row
				    {
				        Text{text: modelData[0]}
				        SpinBox
				        {
				            id: slcpg_
				            minimumValue: modelData[1]
				            maximumValue: modelData[2]
				            stepSize: modelData[3]
				            decimals: modelData[4]
				            Binding on value
				            {
				            	delayed: true
				                value: component.model[modelData[0]][transforms_.topIndex]
				            }
				            onValueChanged:
				            {
				                component.model[modelData[0]][transforms_.topIndex] = slcpg_.value;
				                component.model[modelData[0] + "Changed"]();
				            }
				            SequentialAnimation
				            {
				            	id: anim_
				            	property int t : component.model.lcpgAnimTimeMS[transforms_.topIndex]
				            	loops: NumberAnimation.Infinite
				                running: modelData[0] == 'lcpgIndex' && component.model.lcpgAnimate[transforms_.topIndex]
				                NumberAnimation { target: slcpg_; property: "value"; from: slcpg_.minimumValue; to: slcpg_.maximumValue-1; duration: anim_.t/2 }
				                NumberAnimation { target: slcpg_; property: "value"; from: slcpg_.maximumValue-1; to: slcpg_.minimumValue; duration: anim_.t/2 }
				            }
				        }
				    }
				}
				}
				CheckBox
				{
					text: "depth image";
					Binding on checked
					{
						delayed: true
					    value: component.model.depthImgVisible[transforms_.topIndex]
				    }
				    onCheckedChanged:
				    {
				        component.model.depthImgVisible[transforms_.topIndex] = checked;
				        component.model.depthImgVisibleChanged();
				    }
				}
				CheckBox
				{
					text: "camera";
					Binding on checked
					{
						delayed: true
					    value: component.model.cameraVisible[transforms_.topIndex]
				    }
				    onCheckedChanged:
				    {
				        component.model.cameraVisible[transforms_.topIndex] = checked;
				        component.model.cameraVisibleChanged();
				    }
				}
    		}
        }
    }
}

