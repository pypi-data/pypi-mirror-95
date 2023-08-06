import QtQuick 2.9
import QtQuick.Window 2.9
import QtQuick.Controls 1.4
import Leddar 1.0
import UI2D 1.0

Rectangle {
	id: component
	anchors.fill: parent
    color: "darkgray"
	property var model
	property var imageArray
	property var packages
	property var specs
	property int sensorIndex
	property string colorMap : 'jet'
	property string fontFamily: 'Helvetica'
	property int fontSize: 14
	property var fontCapitalization: Font.SmallCaps
	Column
	{
		spacing: 5
	    anchors.fill: parent
	    Label
	    {
			anchors.topMargin: component.margin
			anchors.bottomMargin: component.margin
			font.family: component.fontFamily
			font.bold: true
			font.pointSize: component.fontSize
			font.capitalization: component.fontCapitalization
			text: "Intensity Map (2D)"
		}
	    QImagePainter
	    {
	        imageArray: ColorMapFliter
	        {
	            min: component.model.ampMin2d[component.sensorIndex]
	            max: component.model.ampMax2d[component.sensorIndex]
	            adaptative: component.model.adaptative[component.sensorIndex]
	            colorMap: component.colorMap
	            imageArray: ImageArray
	            {
	                specs : component.specs
	                packages: component.packages
	                imageMode: ImageArray.AMPLITUDE | ImageArray.FLOAT | component.model.flip[component.sensorIndex]
	            }
	        }
	        width: component.width
	        height: component.height/4
	    }
	    Column
	    {
	        visible: component.model.depthImgVisible[component.sensorIndex]
	        spacing: parent.spacing
		    Label
		    {
		    	text: "Distance Map (2D)"
				font.family: component.fontFamily
				font.bold: true
				font.pointSize: component.fontSize
				font.capitalization: component.fontCapitalization
		    }
		    QImagePainter
		    {
		        imageArray: ColorMapFliter
		        {
		            min: component.model.distMin2d[component.sensorIndex]
		            max: component.model.distMax2d[component.sensorIndex]
		            colorMap: component.colorMap + "_r" //reversed so we have reds for close, blues for far
		            imageArray: ImageArray
		            {
		                specs : component.specs
		                packages: component.packages
		                imageMode: ImageArray.DISTANCE | ImageArray.FLOAT | component.model.flip[component.sensorIndex]
		            }
		        }
		        width: component.width
		        height: component.height/4
		    }
	    }
	    Column
	    {
	        visible: component.model.cameraVisible[component.sensorIndex]
	        spacing: parent.spacing
	        Label
	        {
	    		text: "Camera View"
    			font.family: component.fontFamily
    			font.bold: true
    			font.pointSize: component.fontSize
    			font.capitalization: component.fontCapitalization
    	    }
	        QImagePainter
	        {
	            imageArray: component.imageArray
	            width: component.width/3
	            height: component.height/4
	        }
	    }
	}
}
