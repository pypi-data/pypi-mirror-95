import QtQuick 2.9
import QtQuick.Window 2.9
import QtQuick.Controls 1.4
import Leddar 1.0
import Examples 1.0
import MultiSensorViewer 1.0
import QtQml.Models 2.1
import UI2D 1.0

ApplicationWindow
{
    id: component
    title: "LeddarTech Data Controls"

    width: 800; height: 600


    property var specs : []
    property var cameras : []
    property var packages : []
    property var model
    property alias metaFrustrumVisible : viewport_.metaFrustrumVisible

    // for dataset replay gui only
    property alias nIndices : controls_.nIndices
    readonly property alias cursor : controls_.index


    readonly property var viewportModel:
	{
		var l = [];


		for(var i = 0; i < component.model.x.length; i++)
		{
			l.push({
					   colorMap: component.model.colorMap[i]
					   ,visible: component.model.cloudVisible[i]
					   ,translate: Qt.vector3d(component.model.x[i],component.model.y[i],component.model.z[i])
					   ,euler: [component.model.rx[i],component.model.ry[i],component.model.rz[i]]
					   ,packages: component.packages[i]
					   ,specs: component.specs[i]
					   ,filter: component.model.makeFilter(i)
					   ,frustrumDepth: component.model.frustrumDepth[i]
					   ,ampMin3d: component.model.ampMin3d[i]
					   ,ampMax3d: component.model.ampMax3d[i]
					 });
		}
		return l;
	}

    MultiSensorControls
    {
        id: controls_
        //nIndices: input alias
        model: component.model
    }

    Window
    {
        title: "LeddarTech 3D Data Viewer"
        x: 100; y:100
        width: 800; height: 600
        visibility: component.visibility
        MultiSensorViewport
        {
            id: viewport_
            frustrumColor: Qt.rgba(.3,.3,.3,1)
            backgroundColor: Qt.rgba(.1,.1,.1,1)
            // metaFrustrumVisible: input alias
            model: component.viewportModel
            camera.far: 400
        }
    }


    Instantiator
    {
        model: component.viewportModel.length
        delegate: Window
        {
            id: window_
            title: "LeddarTech 2D Data Viewer, sensor " + index
            visibility: component.visibility
            width: 800; height: 600
            MultiSensor2DViewer
            {
                sensorIndex: index
                model: component.model
                packages: component.viewportModel[index].packages
                specs: component.viewportModel[index].specs
                colorMap: component.viewportModel[index].colorMap
                imageArray: cameras[index]
            }
        }
    }
}
